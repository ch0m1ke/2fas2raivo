import ast
import base64
from dataclasses import dataclass
from datetime import datetime as dt
from pathlib import Path

from src.crypto import decrypt_ciphertext

SERVICES_ENCRYPTED_LENGTH = 3
AUTH_TAG_LENGTH = 16


@dataclass
class TwofasFile:
    file_path: Path
    services_encrypted: str | None
    services: list
    app_version_code: int
    app_version_name: str
    app_origin: str
    schema_version: int
    groups: list
    reference: str | None
    password: str | None

    def __init__(
        self,
        file_path: Path,
        services_encrypted: str | None = None,
        services: list = [],
        app_version_code: int = 50309,
        app_version_name: str = "5.3.9",
        app_origin: str = "ios",
        schema_version: int = 4,
        groups: list = [],
        reference: str | None = None,
        password: str | None = None,
    ):
        self.file_path = file_path
        self.services_encrypted = services_encrypted
        self.services = services
        self.app_version_code = app_version_code
        self.app_version_name = app_version_name
        self.app_origin = app_origin
        self.schema_version = schema_version
        self.groups = groups
        self.reference = reference
        self.password = password

    def to_camel_case(self, input_str: str) -> str:
        """Convert snake_case string to camelCase"""
        components = input_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def asdict(self) -> dict:
        return {
            self.to_camel_case(field.name): getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    @property
    def encrypted(self) -> bool:
        return self._is_file_encrypted()

    def _is_file_encrypted(self) -> bool:
        if (
            self.services_encrypted is None
            or len(self.services_encrypted) == 0
            or len(self.services) > 0
        ):
            return False
        encrypted_fields = self.services_encrypted.split(":")
        if len(encrypted_fields) != SERVICES_ENCRYPTED_LENGTH:
            raise ValueError(
                f"'services_encrypted' is invalid. Length must be: {SERVICES_ENCRYPTED_LENGTH}"
            )
        return True

    def decrypt(self) -> bool:
        if self.password in [None, ""]:
            raise ValueError(f"Password is not a valid string.")
        if not self.encrypted:
            return False

        cipher_text_with_auth_tag, salt, iv = [
            base64.b64decode(x) for x in self.services_encrypted.split(":")
        ]
        if len(cipher_text_with_auth_tag) <= AUTH_TAG_LENGTH:
            raise ValueError(
                f"Cipher text with authentication tag length must be >= {AUTH_TAG_LENGTH}"
            )
        cipher_text = cipher_text_with_auth_tag[:-AUTH_TAG_LENGTH]
        auth_tag = cipher_text_with_auth_tag[-AUTH_TAG_LENGTH:]
        pwd = str(self.password).encode()
        plain_text, _ = decrypt_ciphertext(cipher_text, pwd, salt, iv, auth_tag)
        tmp = ast.literal_eval(plain_text.decode("utf-8").replace("\\", ""))
        # If there is only one service
        if isinstance(tmp, dict):
            self.services.append(tmp)
        else:
            self.services = tmp
        self.services_encrypted = None
        return True


@dataclass
class TwofasEntry:
    name: str
    secret: str
    otp: dict
    updated_at: int
    badge: dict
    icon: dict
    order: dict

    def __init__(
        self,
        name: str,
        secret: str,
        otp: dict = None,
        updated_at: int = None,
        badge: dict = None,
        icon: dict = None,
        order: dict = None,
    ):
        self.name = name
        self.secret = secret
        self.otp = (
            otp
            if otp
            else {
                "account": "-",
                "digits": 6,
                "counter": 0,
                "source": "manual",
                "algorithm": "SHA1",
                "tokenType": "TOTP",
                "period": 30,
            }
        )
        self.updated_at = updated_at = (
            (int)(dt.now().microsecond()) if None else updated_at
        )
        self.badge = badge if badge else {"color": "Default"}
        self.icon = (
            icon
            if icon
            else {
                "iconCollection": {"id": "A5B3FB65-4EC5-43E6-8EC1-49E24CA9E7AD"},
                "selected": "Label",
                "label": {"text": name, "backgroundColor": "Pink"},
            }
        )
        self.order = order if order else {"position": 0}

    def to_camel_case(self, input_str: str) -> str:
        """Convert snake_case string to camelCase"""
        components = input_str.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def asdict(self) -> dict:
        return {
            self.to_camel_case(field.name): getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }
