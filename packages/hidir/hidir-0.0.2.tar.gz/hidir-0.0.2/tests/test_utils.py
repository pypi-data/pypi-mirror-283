import pytest

from hidir.utils import cal_sha256, predict_max_depth, split_to_folder


def test_cal_sha256():
    input_string = "Hello, World!"
    expected_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    assert cal_sha256(input_string) == expected_hash

    input_string = ""
    expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert cal_sha256(input_string) == expected_hash

    input_string = "!@#$%^&*()_+-="
    expected_hash = "7d5daf1d509aa928eb1dd4ce91e6d799f1ebbd9bb26f4ed35f3370a6e4095946"
    assert cal_sha256(input_string) == expected_hash

    input_string = "你好，世界"
    expected_hash = "46932f1e6ea5216e77f58b1908d72ec9322ed129318c6d4bd4450b5eaab9d7e7"
    assert cal_sha256(input_string) == expected_hash

    input_string = "a" * 10
    expected_hash = "bf2cb58a68f684d95a3b78ef8f661c9a4e5b09e82cc8f9cc88cce90528caeb27"
    assert cal_sha256(input_string) == expected_hash


def test_predict_max_depth():
    assert predict_max_depth(100, "SHA-256") == 0
    assert predict_max_depth(101, "SHA-256") == 1
    assert predict_max_depth(1000, "SHA-256") == 1
    assert predict_max_depth(1000000, "SHA-256") == 2
    assert predict_max_depth(0, "SHA-256") == 0


def test_split_to_folder():
    indentifier = "abcdefgxxxxxxxxxxx"
    assert split_to_folder(indentifier, 2) == ["ab", "cd"]
    assert split_to_folder(indentifier, 0) == []
    assert split_to_folder(indentifier, 1) == ["ab"]
    assert split_to_folder("", 0) == []
    with pytest.raises(ValueError, match="Identifier length is not enough for the depth."):
        split_to_folder("", 1)
