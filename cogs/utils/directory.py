import os
from os import listdir
from os.path import isfile, join


def touch(directory: str):
    """Creates the specified directory if it doesn't exist."""

    if not os.path.exists(directory):
        os.makedirs(directory)


def list_files(directory: str):
    """List all files within directory."""

    return [os.path.splitext(filename)[0] for filename in os.listdir(directory)]


def get_extension_from_filename(directory: str, filename: str):
    """get file from directory."""

    _dir = [f for f in listdir(directory) if isfile(join(directory, f))]
    for f in _dir:
        fn, ext = os.path.splitext(f)
        if fn == filename:
            return ext


def remove_file(directory: str):
    """Remove file."""

    os.remove(directory)