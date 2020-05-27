
from pathlib import Path

import pytest

from pyfcopy.remove import remove
from pyfcopy_test.tree_progress_listener_tester import TreeProgressListenerTester


def test_invalid_path(tmp_path: Path):

    with pytest.raises(ValueError):

        remove(tmp_path / "non-existent")


def test_remove_file(tmp_path: Path):

    path = tmp_path / "file.ext"

    path.touch()

    remove(path)

    assert not path.exists()


def test_remove_dir(tmp_path: Path):

    path = tmp_path / "some-dir"

    path.mkdir()

    remove(path)

    assert not path.exists()


def test_remove_tree(tmp_path: Path):

    (tmp_path / "dir").mkdir()
    (tmp_path / "dir/a.ext").touch()
    (tmp_path / "dir/empty").mkdir()
    (tmp_path / "dir/sub1").mkdir()
    (tmp_path / "dir/sub1/b.ext").mkdir()
    (tmp_path / "dir/sub2").mkdir()
    (tmp_path / "dir/sub2/sub21").mkdir()
    (tmp_path / "dir/sub2/sub21/c.ext").touch()

    path = tmp_path / "dir"

    tree_progress_listener = TreeProgressListenerTester({
        ".", "empty", "sub1", "sub2", "sub2/sub21",
        "a.ext", "sub1/b.ext", "sub2/sub21/c.ext",
    })

    remove(path, tree_progress_listener=tree_progress_listener)

    assert not path.exists()

    tree_progress_listener.assert_consistent_run()
