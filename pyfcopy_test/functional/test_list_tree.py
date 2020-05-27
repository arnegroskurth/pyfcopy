
from pathlib import Path

from pyfcopy.list_tree import list_tree, Order
from pyfcopy_test.tree_list_assertions import assert_same_tree_list


def test_empty(tmp_path: Path):

    paths = list_tree(tmp_path)

    assert paths == []


def test_circular_symlink(tmp_path: Path):

    (tmp_path / "a-symlink").symlink_to(tmp_path)

    paths = list_tree(tmp_path)

    assert_same_tree_list(paths, ["a-symlink"])


def test_simple(tmp_path: Path):

    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2/dir3").mkdir()
    (tmp_path / "file1").touch()
    (tmp_path / "dir1/file2").touch()
    (tmp_path / "dir2/dir3/file3").touch()

    paths = list_tree(tmp_path, order=Order.PRE)

    assert_same_tree_list(paths, [
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

    assert_same_tree_list(list_tree(tmp_path, order=Order.PRE), [
        "dir1",
        "dir1/dir2",
        "dir1/dir2/file",
    ])

    assert_same_tree_list(list_tree(tmp_path, order=Order.POST), [
        "dir1/dir2/file",
        "dir1/dir2",
        "dir1",
    ])


def test_absolute_path(tmp_path: Path):

    (tmp_path / "file.ext").touch()

    assert_same_tree_list(list_tree(tmp_path, absolute=False), [
        "file.ext",
    ])

    assert_same_tree_list(list_tree(tmp_path, absolute=True), [
        tmp_path / "file.ext",
    ])
