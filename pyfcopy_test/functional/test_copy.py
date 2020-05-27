
from pathlib import Path

import pytest

from pyfcopy import copy


def test_copy_file(tmp_path: Path):

    (tmp_path / "file.ext").touch()

    copy(tmp_path / "file.ext", tmp_path / "file2.ext")

    assert (tmp_path / "file2.ext").is_file()


def test_copy_dir(tmp_path: Path):

    (tmp_path / "dir").mkdir()

    copy(tmp_path / "dir", tmp_path / "target")

    assert (tmp_path / "target").is_dir()


def test_copy_tree(tmp_path: Path):

    (tmp_path / "dir").mkdir()
    (tmp_path / "dir/file1").touch()
    (tmp_path / "dir/subdir1").mkdir()
    (tmp_path / "dir/subdir1/file2").touch()
    (tmp_path / "dir/subdir1/file3").touch()
    (tmp_path / "dir/subdir2").mkdir()

    copy(tmp_path / "dir", tmp_path / "target")

    assert (tmp_path / "target").is_dir()
    assert (tmp_path / "target/file1").is_file()
    assert (tmp_path / "target/subdir1").is_dir()
    assert (tmp_path / "target/subdir1/file2").is_file()
    assert (tmp_path / "target/subdir1/file3").is_file()
    assert (tmp_path / "target/subdir2").is_dir()


@pytest.mark.parametrize("relative_path", [".", "..", "non-existent", "a-file-symlink", "a-dir-symlink"])
def test_invalid_source_path(relative_path: str, tmp_path: Path):

    (tmp_path / "a-file").touch()
    (tmp_path / "a-dir").mkdir()

    (tmp_path / "a-dir-symlink").symlink_to(tmp_path / "a-dir")
    (tmp_path / "a-file-symlink").symlink_to(tmp_path / "a-file")

    with pytest.raises(ValueError):

        copy(tmp_path / relative_path, tmp_path / "target")


@pytest.mark.parametrize("relative_path", ["", ".", ".."])
def test_invalid_target_path(relative_path: str, tmp_path: Path):

    (tmp_path / "source").touch()

    with pytest.raises(ValueError):

        copy(tmp_path / "source", tmp_path / relative_path)
