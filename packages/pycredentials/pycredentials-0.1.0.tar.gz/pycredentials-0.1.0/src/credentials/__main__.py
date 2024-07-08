import argparse
import getpass
import logging
import os
import sys
from contextlib import suppress
from pathlib import Path

from .base import RESERVED_NAMES, CredentialsError
from .credential import Credential

verbose = False

parser = argparse.ArgumentParser(
    "credentials",
    "Store your credentials securely.",
)
parser.add_argument(
    "--verbose",
    "-V",
    action="store_true",
    help="Verbose error message.",
)
parser.add_argument(
    "--yes",
    "-y",
    action="store_true",
    help="'Yes' for all options.",
)
parser.add_argument(
    "--path",
    default=os.environ.get("CREDENTIALS_PATH"),
)
parser.add_argument("--password", default=os.environ.get("CREDENTIALS_PASSWORD"))
parser.add_argument(
    "action",
    choices=["add", "set", "remove", "show"],
)
parser.add_argument("key_name")
parser.add_argument(
    "value",
    nargs="?",
)


def parse(argv=None) -> None:
    args = parser.parse_args(argv)
    if args.verbose:
        print(args)

    global verbose
    verbose = args.verbose

    if args.path is None:
        raise CredentialsError("Storage path is not provided and CREDENTIALS_PATH is not set.")
    else:
        path = Path(args.path)

    if args.password is None:
        password = getpass.getpass("Password for credentials: ")
        if not password:
            raise CredentialsError("Storage password is not provided and CREDENTIALS_PASSWORD is not set.")
    else:
        password = args.password

    key: str = args.key_name
    value: str | None = args.value
    credential = Credential(path)

    match args.action:
        case "add":
            if value is None:
                value = getpass.getpass("Data to add: ")
                if not value:
                    raise CredentialsError("Value is empty. Cannot add value.")
            if key in RESERVED_NAMES:
                raise CredentialsError(f"Cannot set key name as {key}; The name was prohibited by special use.")

            data_gen = credential.replace(password, should_exist=False)
            data = next(data_gen)
            if key in data:
                raise CredentialsError(f"Key `{key}` already defined as {value!r}. Use `set` action to replace")
            data[key] = value
            with suppress(GeneratorExit, StopIteration):
                data_gen.send(data)

        case "set":
            if value is None:
                value = getpass.getpass("Data to add: ")
                if not value:
                    raise CredentialsError("Value is empty. Cannot set value.")
            if key in RESERVED_NAMES:
                raise CredentialsError(f"Cannot set key name as {key}; The name was prohibited by special use.")

            data_gen = credential.replace(password, should_exist=False)
            data = next(data_gen)
            data[key] = value
            with suppress(GeneratorExit, StopIteration):
                data_gen.send(data)

        case "remove":
            if key == "all":
                if args.yes or input("Deleting all keys? y/N ").lower().startswith("y"):
                    data_gen = credential.replace(password, should_exist=False)
                    data = next(data_gen)
                    data.clear()
                    with suppress(GeneratorExit, StopIteration):
                        data_gen.send(data)
                else:
                    print("The action has been revoked by user.")
            else:
                data_gen = credential.replace(password, should_exist=False)
                data = next(data_gen)
                if key not in data:
                    raise CredentialsError(f"Key `{key}` already doesn't exist.")
                del data[key]
                with suppress(GeneratorExit, StopIteration):
                    data_gen.send(data)

        case "show":
            data = credential.load(password)
            if key == "all":
                for stored_key, stored_value in data.items():
                    print(f"{stored_key}={stored_value!r}")
            else:
                if key not in data:
                    raise CredentialsError(f"Key `{key}` doesn't exist.")
                print(data[key])
        case other:
            raise CredentialsError(f"Unknown action: {other}")


def main(argv=None):
    try:
        parse(sys.argv[1:] or ["--help"])
    except SystemExit:
        raise
    except CredentialsError as e:
        if verbose:
            raise
        logging.error(f"{e}")
        return 1
    except BaseException as e:
        if verbose:
            raise
        logging.error(f"{type(e).__name__}: {e}")
        return 2
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
