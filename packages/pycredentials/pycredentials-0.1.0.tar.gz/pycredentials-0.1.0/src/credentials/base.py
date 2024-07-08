class CredentialsError(Exception):
    pass


RESERVED_NAMES = ["all"]

type CredentialData = dict[str, str]
