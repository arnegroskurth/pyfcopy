
from pathlib import Path

import pytest

from pyfcopy import copy
from pyfcopy_test.file_progress_listener_tester import FileProgressListenerTester
from pyfcopy_test.tree_equality import assert_equal_trees
from pyfcopy_test.tree_fixture import prepare_tree
from pyfcopy_test.tree_progress_listener_tester import TreeProgressListenerTester


def test_copy_file(tmp_path: Path):

    (tmp_path / "file.ext").touch()

    copy(tmp_path / "file.ext", tmp_path / "file2.ext")

    assert (tmp_path / "file2.ext").is_file()


def test_copy_dir(tmp_path: Path):

    (tmp_path / "dir").mkdir()

    copy(tmp_path / "dir", tmp_path / "target")

    assert (tmp_path / "target").is_dir()


def test_copy_tree(tmp_path: Path):

    prepare_tree(
        tmp_path,
        directory_map={
            "src": 0o771,
            "src/empty": 0o777,
            "src/sub1": 0o775,
            "src/sub2": 0o755,
            "src/sub2/sub21": 0o757,
        },
        file_map={
            "src/a.ext": 0o777,
            "src/sub1/b.ext": 0o775,
            "src/sub2/sub21/c.ext": 0o757,
        }
    )

    source = tmp_path / "src"
    target = tmp_path / "target"

    tree_progress_listener = TreeProgressListenerTester({
        ".", "empty", "sub1", "sub2", "sub2/sub21",
        "a.ext", "sub1/b.ext", "sub2/sub21/c.ext",
    })
    file_progress_listener = FileProgressListenerTester()

    copy(
        str(source),
        str(target),
        tree_progress_listener=tree_progress_listener,
        file_progress_listener=file_progress_listener
    )

    assert_equal_trees(source, target)

    tree_progress_listener.assert_consistent_run()
    file_progress_listener.assert_consistent_run()


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
