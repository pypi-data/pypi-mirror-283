import base64
import logging
import os
import pickle
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Generator

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .base import CredentialData, CredentialsError


class Credential:
    storage: Path

    def __init__(self, storage: Path):
        if storage is None:
            env_storage = os.environ.get("CREDENTIALS_PATH")
            if env_storage is None:
                raise ValueError("Storage path is not provided and CREDENTIALS_PATH is not set.")
            storage = Path(env_storage)
        self.storage = storage

    def load(self, password: str) -> CredentialData:
        raw_data = self.storage.read_bytes()
        salt, encrypted_data = raw_data[:16], raw_data[16:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        real_password = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        fernet = Fernet(real_password)
        return pickle.loads(fernet.decrypt(encrypted_data))

    def save(self, password: str, data: CredentialData) -> None:
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        real_password = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        fernet = Fernet(real_password)
        encrypted_data = fernet.encrypt(pickle.dumps(data))

        prev_data = self.storage.read_bytes()
        try:
            with open(self.storage, "xb") as f:
                f.write(salt)
                f.write(encrypted_data)
        except BaseException:
            logging.error(f"Failed to write data to {self.storage}. restore...")
            self.storage.write_bytes(prev_data)

    def replace(self, password: str, should_exist: bool = True) -> Generator[CredentialData, CredentialData, None]:
        if self.storage.is_file() and (raw_data := self.storage.read_bytes()):
            salt, encrypted_data = raw_data[:16], raw_data[16:]

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )
            real_password = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
            fernet = Fernet(real_password)
            data = yield pickle.loads(fernet.decrypt(encrypted_data))
        elif should_exist:
            raise CredentialsError(f"File {self.storage} not found.")
        else:
            data = yield {}

        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        real_password = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        fernet = Fernet(real_password)
        encrypted_data = fernet.encrypt(pickle.dumps(data))

        try:
            with open(self.storage, "wb") as f:
                f.write(salt)
                f.write(encrypted_data)
        except BaseException:
            logging.error(f"Failed to write data to {self.storage}. restore...")
            self.storage.write_bytes(raw_data)
