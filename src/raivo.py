import json
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import pyminizip


@dataclass
class RaivoFile:
    file_path: Path
    password: str | None
    services: list

    def __init__(self, file_path: Path, password: str = None, services: list = []):
        self.file_path = (
            self.file_path.joinpath("raivo-otp-export.zip")
            if file_path.is_dir()
            else file_path
        )
        self.password = password
        self.services = services

    def to_camel_case(self, input_str: str) -> str:
        """Convert snake_case string to camelCase"""
        components = input_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def asdict(self) -> dict:
        return {
            self.to_camel_case(field.name): getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def save(self):
        """Write object content to file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            if len(self.file_path.suffix) == 0 or self.file_path.suffix != ".zip":
                self.file_path = self.file_path.with_suffix(".zip")
            json_file = Path(temp_dir).joinpath("raivo-otp-export.json")
            with open(json_file, "w") as f:
                f.write(json.dumps(self.services))
            pyminizip.compress(
                str(json_file), None, str(self.file_path), self.password, 5
            )


@dataclass
class RaivoEntry:
    secret: str
    account: str
    issuer: str
    algorithm: str
    timer: str
    counter: str
    kind: str
    pinned: str
    icon_type: str
    icon_value: str
    digits: str

    def __init__(
        self,
        secret: str,
        account: str = "-",
        issuer: str = "-",
        algorithm: str = "SHA1",
        timer: str = "30",
        counter: str = "0",
        kind: str = "TOTP",
        pinned: str = "false",
        icon_type: str = "",
        icon_value: str = "",
        digits: str = "6",
    ):
        self.secret = secret
        self.account = account
        self.issuer = issuer
        self.algorithm = algorithm
        self.timer = timer
        self.counter = counter
        self.kind = kind
        self.pinned = pinned
        self.icon_type = icon_type
        self.icon_value = icon_value
        self.digits = digits
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if not isinstance(value, str):
                raise TypeError(
                    f"{field} should be a string, but got {type(value).__name__}."
                )

    def to_camel_case(self, input_str: str) -> str:
        """Convert snake_case string to camelCase"""
        components = input_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def asdict(self) -> dict:
        return {
            self.to_camel_case(field.name): getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }
