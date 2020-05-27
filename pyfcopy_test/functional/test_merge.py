
from pathlib import Path

import pytest

from pyfcopy import index
from pyfcopy.merge import merge
from pyfcopy_test.index_assertions import assert_same_index


def test_empty(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "target").mkdir()

    merge(tmp_path / "source", tmp_path / "target")

    assert_same_index(index(tmp_path / "target"), ["."])


@pytest.mark.parametrize("relative_path", ["file", "symlink", "non-existent", "target"])
def test_invalid_source(relative_path: str, tmp_path: Path):

    (tmp_path / "target").mkdir()
    (tmp_path / "file").touch()
    (tmp_path / "symlink").symlink_to(tmp_path / "file")

    with pytest.raises(ValueError):

        merge(tmp_path / relative_path, tmp_path / "target")


@pytest.mark.parametrize("relative_path", ["file", "symlink", "non-existent", "source"])
def test_invalid_target(relative_path: str, tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "file").touch()
    (tmp_path / "symlink").symlink_to(tmp_path / "file")

    with pytest.raises(ValueError):

        merge(tmp_path / "source", tmp_path / relative_path)


def test_collision_detection_file(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/file").touch()
    (tmp_path / "target").mkdir()
    (tmp_path / "target/file").touch()

    with pytest.raises(ValueError):

        merge(tmp_path / "source", tmp_path / "target")


def test_collision_detection_file_and_dir(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/foo").touch()
    (tmp_path / "target").mkdir()
    (tmp_path / "target/foo").mkdir()

    with pytest.raises(ValueError):

        merge(tmp_path / "source", tmp_path / "target")


def test_collision_detection_dir_and_file(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/foo").mkdir()
    (tmp_path / "target").mkdir()
    (tmp_path / "target/foo").touch()

    with pytest.raises(ValueError):

        merge(tmp_path / "source", tmp_path / "target")


def test_dir_replaced_by_file(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/foo").touch()
    (tmp_path / "target").mkdir()
    (tmp_path / "target/foo").mkdir()

    merge(tmp_path / "source", tmp_path / "target", overwrite=True)

    assert (tmp_path / "target/foo").is_file()


def test_file_replaced_by_dir(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/foo").mkdir()
    (tmp_path / "target").mkdir()
    (tmp_path / "target/foo").touch()

    merge(tmp_path / "source", tmp_path / "target", overwrite=True)

    assert (tmp_path / "target/foo").is_dir()


def test_file_replaced_by_file(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/foo").write_text("foo")
    (tmp_path / "target").mkdir()
    (tmp_path / "target/foo").write_text("bar")

    merge(tmp_path / "source", tmp_path / "target", overwrite=True)

    assert (tmp_path / "target/foo").read_text() == "foo"


def test_no_collisions(tmp_path: Path):

    (tmp_path / "source").mkdir()
    (tmp_path / "source/file1").touch()
    (tmp_path / "source/dir1").mkdir()
    (tmp_path / "source/dir1/file2").touch()

    (tmp_path / "target").mkdir()
    (tmp_path / "target/file3").touch()
    (tmp_path / "target/dir1").mkdir()
    (tmp_path / "target/dir1/file4").touch()

    merge(tmp_path / "source", tmp_path / "target")

    assert_same_index(index(tmp_path / "target"), {
        ".", "file1", "file3", "dir1", "dir1/file2", "dir1/file4",
    })
