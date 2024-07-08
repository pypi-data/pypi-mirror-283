from __future__ import annotations

import os
import shutil

from .exceptions import NotSupportedError
from .utils import (
    SUPPORTED_STRATEGY,
    get_identifier,
    predict_max_depth,
    prevent_indexing,
    split_to_folder,
)


class DirectoryManager:
    def __init__(self, root: str, strategy="SHA-256", files_predict=1_000_000, clear_index=False):
        self.root = root
        if strategy not in SUPPORTED_STRATEGY:
            raise NotSupportedError(f"Unsupported strategy: {strategy}")

        self.strategy = strategy
        self.max_depth = predict_max_depth(files_predict, strategy)
        if clear_index:
            prevent_indexing(root)

    def __recursive_make_folder(self, path):
        """Recursively create directories if they do not exist."""
        if os.path.exists(path):
            return
        parent_dir = os.path.dirname(path)
        if parent_dir and not os.path.exists(parent_dir):
            self.__recursive_make_folder(parent_dir)
        os.makedirs(path)

    def get_base_path(self, file_name) -> str:
        """Get the base path for a file based on the identifier."""
        prefix = get_identifier(file_name, self.strategy)
        paths = split_to_folder(prefix, self.max_depth)
        folder_path = os.path.join(self.root, *paths)
        return folder_path

    def check_file(self, file_name: str) -> str | None:
        """Check for a file by its name and return its path if it exists."""
        target_file = os.path.join(self.get_base_path(file_name), file_name)
        return target_file if os.path.exists(target_file) else None

    def __ensure_folder_exists(self, file_name: str):
        """Ensure that the folder for a given file exists."""
        folder_path = self.get_base_path(file_name)
        if not os.path.exists(folder_path):
            self.__recursive_make_folder(folder_path)

    def __move_or_copy_file(self, file_path: str, operation: str):
        """Move or copy a file to its designated folder based on the operation."""
        _, file_name = os.path.split(file_path)
        self.__ensure_folder_exists(file_name)
        target_folder = self.get_base_path(file_name)
        dst_path = os.path.join(target_folder, file_name)

        if operation == "move":
            shutil.move(file_path, dst_path)
        elif operation == "copy":
            shutil.copy(file_path, dst_path)
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def move_file(self, file_path: str):
        """Move a file to its designated folder."""
        self.__move_or_copy_file(file_path, "move")

    def copy_file(self, file_path: str):
        """Copy a file to its designated folder."""
        self.__move_or_copy_file(file_path, "copy")
