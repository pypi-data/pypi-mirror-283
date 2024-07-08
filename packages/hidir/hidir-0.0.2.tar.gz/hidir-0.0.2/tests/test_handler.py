import os.path

from hidir.handler import DirectoryManager


def test_get_base_path():
    root_path = ".cache"
    manager = DirectoryManager(root_path, strategy="SHA-256", files_predict=1_000_000)
    assert manager.get_base_path("test.txt") == os.path.join(root_path, "a6", "ed")

    manager = DirectoryManager(root_path, strategy="SHA-256", files_predict=10)
    assert manager.get_base_path("test.txt") == root_path

    manager = DirectoryManager(root_path, strategy="SHA-256", files_predict=1_000)
    assert manager.get_base_path("test.txt") == os.path.join(root_path, "a6")
