
from pathlib import Path

import pytest

from pyfcopy.index import index, Order
from pyfcopy_test.tree_list_assertions import assert_same_tree_list


def test_invalid_path(tmp_path: Path):

    with pytest.raises(ValueError):

        index(tmp_path / "non-existent")


def test_empty(tmp_path: Path):

    paths = index(tmp_path)

    assert_same_tree_list(paths, ["."])


def test_circular_symlink(tmp_path: Path):

    (tmp_path / "a-symlink").symlink_to(tmp_path)

    paths = index(tmp_path)

    assert_same_tree_list(paths, [".", "a-symlink"])


def test_file_path(tmp_path: Path):

    (tmp_path / "file.ext").touch()

    assert_same_tree_list(
        index(tmp_path / "file.ext", absolute=True),
        [tmp_path / "file.ext"]
    )

    assert_same_tree_list(
        index(tmp_path / "file.ext", absolute=False),
        ["."]
    )


def test_simple(tmp_path: Path):

    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2/dir3").mkdir()
    (tmp_path / "file1").touch()
    (tmp_path / "dir1/file2").touch()
    (tmp_path / "dir2/dir3/file3").touch()

    paths = index(tmp_path, order=Order.PRE)

    assert_same_tree_list(paths, [
        ".",
        'dir1',
        'dir1/file2',
        'dir2',
        'dir2/dir3',
        'dir2/dir3/file3',
        'file1',
    ])


def test_order(tmp_path: Path):

    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1/dir2").mkdir()
    (tmp_path / "dir1/dir2/file").touch()

    assert_same_tree_list(index(tmp_path, order=Order.PRE), [
        ".",
        "dir1",
        "dir1/dir2",
        "dir1/dir2/file",
    ])

    assert_same_tree_list(index(tmp_path, order=Order.POST), [
        "dir1/dir2/file",
        "dir1/dir2",
        "dir1",
        ".",
    ])


def test_absolute_path(tmp_path: Path):

    (tmp_path / "file.ext").touch()

    assert_same_tree_list(index(tmp_path, absolute=False), [
        ".",
        "file.ext",
    ])

    assert_same_tree_list(index(tmp_path, absolute=True), [
        tmp_path,
        tmp_path / "file.ext",
    ])


def test_root_exclusion(tmp_path: Path):

    (tmp_path / "some-dir").mkdir()

    assert_same_tree_list(index(tmp_path / "some-dir", include_root=False), [])
    assert_same_tree_list(index(tmp_path / "some-dir", include_root=True), ["."])
