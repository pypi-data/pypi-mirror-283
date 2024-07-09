from setuptools import find_packages, setup

setup(
    name="streaming-wds",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        "pyarrow",
        "boto3",
        "torch",
    ],
)