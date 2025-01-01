from setuptools import setup, find_packages

setup(
    name="2fas2raivo",
    version="0.1.0",
    author="Michele Chiarello",
    author_email="",
    description="A CLI tool to convert 2FAS backups into Raivo-compatible ones.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ch0m1ke/2fas2raivo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "cryptography==44.0.0",
        "loguru==0.7.3",
        "pyminizip==0.2.6",
        "pytest==8.3.4",
        "pytest-cov==6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "twofas2raivo=src.main:main",
        ],
    },
)
