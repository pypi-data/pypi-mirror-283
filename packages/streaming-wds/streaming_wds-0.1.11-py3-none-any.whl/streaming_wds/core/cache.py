import logging
import os
import shutil
import threading
import time
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class LocalShardLRUCache:
    """
    A local cache for shards using a Least Recently Used (LRU) eviction policy.

    This class manages a local cache of shards, handling their storage, retrieval,
    and eviction based on a size limit and access patterns.

    Attributes:
        remote (str): The remote uri of the dataset.
        bucket (str): The bucket name extracted from the remote uri.
        key_prefix (str): The key prefix extracted from the remote uri.
        cache_dir (Path): The local directory where shards are cached.
        cache_limit_bytes (int): The maximum size of the cache in bytes.
        current_cache_size (int): The current size of the cache in bytes.
        cache_lock (threading.Lock): A lock for thread-safe cache operations.
        shard_locks (Dict[str, threading.Lock]): Locks for individual shards.
        shard_access_times (Dict[str, int]): Last access times for shards.
        shard_read_count (Dict[str, int]): Read counts for shards.
    """

    def __init__(self, remote: str, worker_rank: int, cache_limit_bytes: int):
        """
        Initialize the LocalShardLRUCache.

        Args:
            remote (str): The remote URL of the dataset.
            worker_rank (int): The rank of the worker using this cache.
            cache_limit_bytes (int): The maximum size of the cache in bytes.
        """
        self.remote = remote
        parsed_uri = urlparse(self.remote)
        self.bucket = parsed_uri.netloc
        self.key_prefix = parsed_uri.path.lstrip("/")

        self.cache_dir = Path(
            "/tmp/streaming_wds", self.bucket, self.key_prefix, str(worker_rank)
        )
        self.cache_limit_bytes = cache_limit_bytes
        self.current_cache_size = 0

        self.cache_lock = threading.Lock()

        self.shard_locks: Dict[str, threading.Lock] = {}
        self.shard_access_times: Dict[str, int] = {}
        self.shard_read_count: Dict[str, int] = {}

        self.load_cache()

    def load_cache(self) -> None:
        """
        Load the cache, clearing existing content if present.

        This method ensures the cache directory exists and is empty.
        """
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            # TODO: replace this by looking up the currently downloaded shards
        else:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_shard_path(self, shard_key: str, check_exists: bool = False) -> str:
        """
        Get the local path for a shard.

        Args:
            shard_key (str): The key of the shard.
            check_exists (bool): If True, return None if the shard doesn't exist.

        Returns:
            str: The local path of the shard, or None if check_exists is True and the shard doesn't exist.
        """
        shard_path = self.cache_dir / shard_key.replace(self.key_prefix, "").lstrip("/")
        shard_path.parent.mkdir(parents=True, exist_ok=True)
        if check_exists and not shard_path.exists():
            return None
        return str(shard_path)

    def get_shard(self, shard_key: str) -> Optional[str]:
        """
        Get a shard from the cache.

        This method updates the access time and read count for the shard.

        Args:
            shard_key (str): The key of the shard to retrieve.

        Returns:
            Optional[str]: The path to the shard if it exists in the cache, None otherwise.
        """
        with self.cache_lock:
            shard_path = self.get_shard_path(shard_key)
            if shard_path.exists():
                self.shard_access_times[shard_key] = time.time()

                if shard_key not in self.shard_locks:
                    self.shard_locks[shard_key] = threading.Lock()

                if shard_key not in self.shard_access_times:
                    self.shard_access_times[shard_key] = time.time()

                if shard_key not in self.shard_read_count:
                    self.shard_read_count[shard_key] = 0
                return str(shard_path)
            return None

    def acquire_shard_lock(self, shard_key: str) -> bool:
        """
        Acquire the lock for a specific shard.

        Args:
            shard_key (str): The key of the shard to lock.

        Returns:
            bool: True if the lock was acquired, False if the shard doesn't exist.
        """
        shard_lock = self.shard_locks.get(shard_key, None)
        if shard_lock is None:
            return False
        shard_lock.acquire(blocking=True)
        return True

    def release_shard_lock(self, shard_key: str):
        """
        Release the lock for a specific shard and increment its read count.

        Args:
            shard_key (str): The key of the shard to unlock.

        Returns:
            bool: False if the shard doesn't exist, None otherwise.
        """
        shard_lock = self.shard_locks.get(shard_key, None)
        if shard_lock is None:
            return False
        shard_lock.release()
        with self.cache_lock:
            self.shard_read_count[shard_key] += 1

    def add_shard(self, shard_key: str, shard_size: int):
        """
        Add a new shard to the cache.

        If there's not enough space, this method will evict old shards until there's room.

        Args:
            shard_key (str): The key of the shard to add.
            shard_size (int): The size of the shard in bytes.

        Returns:
            str: The path where the shard should be stored.
        """
        while True:
            with self.cache_lock:
                if self.current_cache_size + shard_size <= self.cache_limit_bytes:
                    self.current_cache_size += shard_size
                    self.shard_access_times[shard_key] = time.time()
                    self.shard_locks[shard_key] = threading.Lock()
                    self.shard_read_count[shard_key] = 0  # Initialize read count
                    return self.get_shard_path(shard_key)

            self._evict_oldest_shard()

    def _evict_oldest_shard(self) -> None:
        """
        Evict the oldest shard from the cache.

        This method removes the least recently used shard that has been read more than once.
        If no such shard exists, it waits and tries again.
        """
        logger.debug("Evicting oldest shard from cache")
        while True:
            eligible_shards = [
                shard
                for shard in self.shard_access_times
                if self.shard_read_count.get(shard, 0) > 1
            ]

            if not eligible_shards:
                time.sleep(0.1)
                continue

            oldest_shard = min(eligible_shards, key=self.shard_access_times.get)
            shard_path = self.get_shard_path(oldest_shard)
            shard_size = shard_path.stat().st_size

            self.acquire_shard_lock(oldest_shard)
            with self.cache_lock:
                self.current_cache_size -= shard_size
                del self.shard_access_times[oldest_shard]
                del self.shard_locks[oldest_shard]
                del self.shard_read_count[oldest_shard]

            logger.debug(f"Evicting shard {oldest_shard} from cache")
            os.remove(shard_path)
            return
