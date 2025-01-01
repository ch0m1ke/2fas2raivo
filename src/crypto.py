import json
import os
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 10000
KEY_LENGTH = 256
HASH = hashes.SHA256()
ENCRYPTION_CIPHER = algorithms.AES


def derive_key(password: bytes, salt: bytes) -> bytes:
    """Derive a key from the given password and salt using PBKDF2-HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=HASH,
        length=KEY_LENGTH // 8,  # Output length in bytes
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(password)


def aes_gcm(
    text: bytes, master_key: bytes, iv: bytes, encrypt: bool, auth_tag: bytes = None
) -> tuple:
    """Perform AES-GCM encryption/decryption."""
    cipher = Cipher(
        ENCRYPTION_CIPHER(master_key),
        modes.GCM(iv, auth_tag) if not encrypt else modes.GCM(iv),
        backend=default_backend(),
    )
    encryptor = cipher.encryptor() if encrypt else cipher.decryptor()
    encryptor.authenticate_additional_data(b"")
    if encrypt:
        ciphertext = encryptor.update(text) + encryptor.finalize()
        return ciphertext, encryptor.tag
    try:
        plaintext = encryptor.update(text) + encryptor.finalize()
        return plaintext, auth_tag
    except Exception as exc:
        raise ValueError("Decryption failed") from exc


def decrypt_ciphertext(
    cipher_text: bytes, password: bytes, salt: bytes, iv: bytes, auth_tag: bytes
) -> tuple:
    """Decrypt 'cipher_text' and return its plaintext and authentication tag."""
    try:
        master_key = derive_key(password, salt)
        return aes_gcm(cipher_text, master_key, iv, encrypt=False, auth_tag=auth_tag)
    except Exception as exc:
        raise ValueError(f"Failed to derive cipher key. {str(exc)}")


def encrypt_ciphertext(
    plain_text: bytes, password: bytes, salt: bytes, iv: bytes
) -> tuple:
    """Encrypt 'encrypt_ciphertext' and return its cipher_text and authentication tag."""
    try:
        master_key = derive_key(password, salt)
        return aes_gcm(plain_text, master_key, iv, encrypt=True)
    except Exception as exc:
        raise ValueError(f"Failed to derive cipher key. {str(exc)}")
