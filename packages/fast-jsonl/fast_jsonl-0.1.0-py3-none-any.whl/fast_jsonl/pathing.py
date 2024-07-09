import os
import json
import hashlib
from pathlib import Path
from typing import Optional, Union

import fast_jsonl as fj


def get_text_hash(text, algorithm=hashlib.sha256):
    file_hash = algorithm()
    file_hash.update(text.encode())
    return file_hash.hexdigest()


def get_local_path(file_path, dir_name):
    r"""
    Get a cache file path based on the location of the given file path.
    """
    path = Path(file_path)
    target_dir = path.parent / dir_name  # .fj_cache, .locks
    target_dir.mkdir(parents=True, exist_ok=True)
    output = target_dir / path.stem
    output.mkdir(exist_ok=True)
    return output
    return collision_dir / f"{get_text_hash(path.name)}.cache.json"


def get_user_path(file_path):
    r"""
    Get a cache file path based on the user's home directory.
    """
    path = Path(file_path)
    cache_dir = Path.home() / ".local/share/fj_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    # name = path.resolve().as_posix().replace(".", "-").replace("/", "--")
    # return cache_dir / f"{name}.cache.json"
    posix_path = path.resolve().as_posix()
    name = posix_path.replace("/", "--")
    collision_dir = cache_dir / name
    collision_dir.mkdir(exist_ok=True)
    hashed_name = get_text_hash(posix_path)
    return collision_dir / f"{hashed_name}.cache.json"


def filepath_to_cachepath(file_path):
    r"""
    Get an inferred cache path for a given file path.

    The inferred cache path can be controlled using an environment variable.
    If FAST_JSONL_DIR_METHOD is set to "local", the cache path will be in a
    subdirectory in the target file path's directory.
    If it is set to "user", the cache path will be in
    <home>/.local/share/fj_cache/ where <home> is the user's home directory.


    Args:
        file_path (str or pathlike): The path to the target JSONL file.
    """
    if fj.constants.DIR_METHOD == "local":
        return filepath_to_cachepath_local(file_path)
    elif fj.constants.DIR_METHOD == "user":
        return filepath_to_cachepath_user(file_path)
    else:
        message = (
            f"Unknown value for {fj.constants.DIR_METHOD_ENV} environment "
            f'variable: "{fj.constants.DIR_METHOD}".'
        )
        raise NotImplementedError(message)

