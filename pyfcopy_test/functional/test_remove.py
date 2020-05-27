
from pathlib import Path

import pytest

from pyfcopy.remove import remove
from pyfcopy_test.tree_fixture import prepare_tree
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

    prepare_tree(
        tmp_path,
        directory_map={
            "tree": 0o777,
            "tree/empty": 0o777,
            "tree/sub1": 0o775,
            "tree/sub2": 0o755,
            "tree/sub2/sub21": 0o757,
        },
        file_map={
            "tree/a.ext": 0o777,
            "tree/sub1/b.ext": 0o775,
            "tree/sub2/sub21/c.ext": 0o757,
        }
    )

    path = tmp_path / "tree"

    tree_progress_listener = TreeProgressListenerTester({
        ".", "empty", "sub1", "sub2", "sub2/sub21",
        "a.ext", "sub1/b.ext", "sub2/sub21/c.ext",
    })

    remove(
        path,
        tree_progress_listener=tree_progress_listener
    )

    assert not path.exists()

    tree_progress_listener.assert_consistent_run()
