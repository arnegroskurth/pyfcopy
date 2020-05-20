
from pathlib import Path

import pytest

from pyfcopy import copy_tree
from pyfcopy_test.file_progress_listener_tester import FileProgressListenerTester
from pyfcopy_test.tree_equality import assert_equal_trees
from pyfcopy_test.tree_fixture import prepare_tree
from pyfcopy_test.tree_progress_listener_tester import TreeProgressListenerTester


def test_copy_tree(tmp_path):

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
        "empty", "sub1", "sub2", "sub2/sub21",
        "a.ext", "sub1/b.ext", "sub2/sub21/c.ext",
    })
    file_progress_listener = FileProgressListenerTester()

    copy_tree(
        str(source),
        str(target),
        tree_progress_listener=tree_progress_listener,
        file_progress_listener=file_progress_listener
    )

    assert_equal_trees(source, target)

    tree_progress_listener.assert_consistent_run()
    file_progress_listener.assert_consistent_run()


@pytest.mark.parametrize("relative_path", [".", "..", "a-file", "non-existent", "a-file-symlink", "a-dir-symlink"])
def test_invalid_source_path(relative_path: str, tmp_path):

    Path(tmp_path / "a-file").touch()
    Path(tmp_path / "a-dir").mkdir()

    Path(tmp_path / "a-dir-symlink").symlink_to(tmp_path / "a-dir")
    Path(tmp_path / "a-file-symlink").symlink_to(tmp_path / "a-file")

    with pytest.raises(ValueError):

        copy_tree(tmp_path / relative_path, tmp_path / "target")


@pytest.mark.parametrize("relative_path", ["", ".", "..", "non-existent"])
def test_invalid_target_path(relative_path: str, tmp_path):

    with pytest.raises(ValueError):

        copy_tree(tmp_path / relative_path, tmp_path / "target")
