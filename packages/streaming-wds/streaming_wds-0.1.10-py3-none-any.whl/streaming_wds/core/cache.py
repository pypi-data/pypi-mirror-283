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
    def __init__(self, remote: str, worker_rank: int, cache_limit_bytes: int):
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
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            # TODO: replace this by looking up the currently downloaded shards
        else:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_shard_path(self, shard_key: str, check_exists: bool = False) -> str:
        shard_path = self.cache_dir / shard_key.replace(self.key_prefix, "").lstrip("/")
        shard_path.parent.mkdir(parents=True, exist_ok=True)
        if check_exists and not shard_path.exists():
            return None
        return shard_path

    def get_shard(self, shard_key: str) -> Optional[str]:
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
        shard_lock = self.shard_locks.get(shard_key, None)
        if shard_lock is None:
            return False
        shard_lock.acquire(blocking=True)

    def release_shard_lock(self, shard_key: str):
        shard_lock = self.shard_locks.get(shard_key, None)
        if shard_lock is None:
            return False
        shard_lock.release()
        with self.cache_lock:
            self.shard_read_count[shard_key] += 1

    def add_shard(self, shard_key: str, shard_size: int):
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
