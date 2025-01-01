import json
import os
from getpass import getpass
from pathlib import Path
from typing import List

import pyminizip

from src.raivo import RaivoEntry, RaivoFile
from src.twofas import TwofasEntry, TwofasFile


def get_2fas_files(src_dir: Path) -> List[Path]:
    """Scan input directory for .2fas files"""

    if not isinstance(src_dir, Path):
        raise TypeError("'src_dir' is not a valid Path object.")

    if not src_dir.is_dir():
        raise ValueError(f"'src_dir' is not a valid directory.")

    return [Path(x) for x in src_dir.glob("*.2fas") if x.is_file()]


def get_file_to_process(files_list: List[Path]) -> Path:
    """Get user-selected file to process"""

    if len(files_list) == 0:
        raise ValueError("'files_list' must contain at least one Path object.")

    selection = -1

    print("--------------------------")
    print("Choose a file to process:\n")

    for item in enumerate(files_list):
        (
            print(f"{item[0]}) {item[1]}")
            if item[0] < len(files_list) - 1
            else print(f"{item[0]}) {item[1]}\n")
        )

    while selection < 0 or selection > len(files_list) -1:
        try:
            selection = int(input("Selection: "))
        except ValueError:
            print("Selection is invalid!")

    print("--------------------------")

    return files_list[selection]


def convert_2fas_to_raivo(src_file: Path, dst_file: Path, password: str = None):
    """Convert .2fas file to Raivo-compatible export"""

    with open(src_file, "r") as f:
        data = json.load(f)

    src = TwofasFile(
        file_path=src_file,
        services_encrypted=(
            data.get("servicesEncrypted") if "servicesEncrypted" in data else None
        ),
        services=data.get("services") if "services" in data else [],
        groups=data.get("groups") if "groups" in data else [],
        reference=data.get("reference") if "reference" in data else None,
        password=password,
    )

    if src.encrypted:
        src.decrypt()

    dst = RaivoFile(file_path=dst_file, password=password)

    for service in src.services:
        r_service = RaivoEntry(
            issuer=service.get("name"),
            account=service.get("otp").get("account"),
            secret=service.get("secret"),
            algorithm=service.get("otp").get("algorithm"),
            timer=str(service.get("otp").get("period")),
            counter=str(service.get("otp").get("counter")),
            kind=service.get("otp").get("tokenType"),
            digits=str(service.get("otp").get("digits")),
        )
        dst.services.append(r_service.asdict())

    dst.save()

    return
