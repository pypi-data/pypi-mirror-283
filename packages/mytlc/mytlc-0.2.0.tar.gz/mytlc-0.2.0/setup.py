import io
import os.path

from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


def get_data_files():
    data_files = []
    for root, dirs, files in os.walk("mytlc/tests/data"):
        for file in files:
            data_files.append(
                os.path.relpath(os.path.join(root, file), "mytlc/tests/data")
            )
    return data_files


setup(
    name="mytlc",
    version="0.2.0",
    author="Sopra Steria Group",
    author_email="anthony.bervas@soprasteria.com",
    description="Python package to download meteorological data and build FAIR datasets.",
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    license="BSD",
    url="https://github.com/abervas/mytlc",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "mytlc": ["templates/*.json"],
        "": get_data_files(),
    },
    install_requires=[
        # Loading dependencies from requirements.txt
        line.strip()
        for line in open("requirements.txt").readlines()
    ],
    extras_requires={
        "mcapy": ["mcapy"],
    },
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
