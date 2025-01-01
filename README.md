# 2fas2raivo

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/LICENSE-MIT-GREEN?style=for-the-badge)](LICENSE)

A CLI tool to convert [2FAS](https://2fas.com/) backups into [Raivo](https://raivo-otp.com/)-compatible ones.

## Requirements

* Python >= 3.10

## Installation

To install the tool, run the following commands:

```shell
git clone https://github.com/ch0m1ke/2fas2raivo.git && cd 2fas2raivo/
pip install .
```

## Usage

The snippet below shows the tool's helper.

```
❯ twofas2raivo --help

usage: twofas2raivo [-h] [-s SOURCE_FILE] [-d DESTINATION_FILE] [--encrypted]

A CLI tool to convert 2FAS backups into Raivo-compatible ones.

options:
  -h, --help                                show this help message and exit
  -s, --source_file SOURCE_FILE             2FAS Auth backup file path.
  -d, --destination_file DESTINATION_FILE   Raivo backup file path.
  --encrypted                               Specify if 2FAS backup is encrypted.
```

Here instead, is an example on how to convert an encrypted backup.

```shell
❯ twofas2raivo -s ~/Downloads/example.2fas -d ~/Downloads/converted.zip --encrypted
Enter password: 
2025-01-01 18:56:51.226 | INFO     | src.main:main:87 - Source file: [/Users/test/Downloads/example.2fas]
2025-01-01 18:56:51.227 | INFO     | src.main:main:88 - Destination file: [/Users/test/Downloads/converted.zip]
2025-01-01 18:56:51.247 | INFO     | src.main:main:96 - File converted successfully!
```