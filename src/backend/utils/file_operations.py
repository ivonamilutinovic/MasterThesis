import os
from contextlib import suppress


def create_subfolders_to(filename: str):
    """
        Creating (sub)folders to provided filename (path) argument.

        Check if filename argument has actual file name in itself (if filename has any extension in itself, then passed
        filename argument has actual file name in itself) ---> create all folders that are above that actual file
        name in provided path.
        Otherwise, filename argument is actually (sub)folders structure that needs to be created if it doesn't exist.
    """

    with suppress(FileNotFoundError):
        if not os.path.splitext(filename)[1]:
            os.makedirs(os.path.normpath(filename), exist_ok=True)
        else:
            os.makedirs(os.path.dirname(os.path.normpath(filename)), exist_ok=True)