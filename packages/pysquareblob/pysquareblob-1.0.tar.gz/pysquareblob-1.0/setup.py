from setuptools import setup
import os


README = os.path.join(os.path.dirname(__file__), "README.md")

setup(
    name="pysquareblob",
    version="1.0",
    description="This project is just a simple way to interact with Square Cloud Blob service",
    long_description=open(README).read(), long_description_content_type="text/markdown",
    author="Jhonatan Jeferson", author_email="jhonatanjefersonoliveira@gmail.com",
    license="MIT",
    keywords=["square cloud", "squareblob", "tool"],
    install_requires=["aiohttp"],
    requires=["aiohttp"],
    package_dir={"pysquareblob": "pysquareblob"},
    include_package_data=True,
    platforms="any",
    url="https://github.com/Jhonatan-Jeferson/pySquareBlob"
)