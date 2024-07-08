import hashlib
import math
import os
import platform

from .exceptions import NotSupportedError

SUPPORTED_STRATEGY = ["SHA-256", "DCC"]

SUPPORTED_FORMAT = ["name"]


def _prevent_indexing_windows(folder_path: str):
    desktop_ini_path = os.path.join(folder_path, "desktop.ini")
    with open(desktop_ini_path, "w") as f:
        f.write("[.ShellClassInfo]\nNoIndex=1\n")
    os.system(f'attrib +h +s "{desktop_ini_path}"')


def _prevent_indexing_unix(folder_path: str):
    metadata_never_index_path = os.path.join(folder_path, ".metadata_never_index")
    with open(metadata_never_index_path, "w") as f:
        f.write("")


def prevent_indexing(folder_path: str):
    system = platform.system()
    if system == "Windows":
        _prevent_indexing_windows(folder_path)
    elif system == "Darwin" or system == "Linux":
        _prevent_indexing_unix(folder_path)
    else:
        raise NotImplementedError(f"Indexing prevention not implemented for {system}")


def cal_sha256(input_str: str) -> str:
    sha256_hash = hashlib.sha256()
    input_bytes = input_str.encode("utf-8")
    sha256_hash.update(input_bytes)

    return sha256_hash.hexdigest()


def get_identifier(input_str: str, strategy: str) -> str:
    if strategy not in SUPPORTED_STRATEGY:
        raise NotSupportedError(f"Unsupported strategy: {strategy}")

    if strategy == "SHA-256":
        return cal_sha256(input_str)
    return ""


def predict_max_depth(file_count, strategy) -> int:
    max_files_per_folder = 100
    if strategy not in SUPPORTED_STRATEGY:
        raise NotSupportedError(f"Unsupported strategy: {strategy}")

    if strategy == "SHA-256":
        max_subfolders_per_folder = 16 * 16
        if file_count <= max_files_per_folder:
            return 0

        depth = math.ceil(
            math.log(file_count / max_files_per_folder) / math.log(max_subfolders_per_folder)
        )
        return depth
    return 0


def split_to_folder(indentifier: str, depth: int) -> list:
    if depth == 0:
        return []
    if len(indentifier) < depth * 2:
        raise ValueError("Identifier length is not enough for the depth.")

    folder_name = indentifier[:2]
    return [folder_name] + split_to_folder(indentifier[2:], depth - 1)
