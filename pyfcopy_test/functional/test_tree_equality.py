from pathlib import Path

import pytest

from pyfcopy_test.tree_equality import _assert_equal_files, assert_equal_trees
from pyfcopy_test.tree_fixture import prepare_tree


@pytest.mark.dependency(name="test_equal_files")
@pytest.mark.parametrize("path_b", ["a.ext", "b.ext"])
def test_equal_files(path_b: str, tmp_path: Path):

    prepare_tree(
        tmp_path,
        file_map={
            "a.ext": 0o664,
            "b.ext": 0o664,
            "c.ext": 0o644,
        },
        empty_files=True
    )

    (tmp_path / "a.ext").write_text("foo")
    (tmp_path / "b.ext").write_text("foo")

    _assert_equal_files(
        tmp_path / "a.ext",
        tmp_path / path_b
    )


@pytest.mark.dependency(name="test_unequal_files")
@pytest.mark.parametrize("path_b", ["b.ext", "c.ext"])
def test_unequal_files(path_b: str, tmp_path: Path):

    prepare_tree(
        tmp_path,
        file_map={
            "a.ext": 0o664,
            "b.ext": 0o664,
            "c.ext": 0o644,
        },
        empty_files=True
    )

    (tmp_path / "b.ext").write_text("foo")

    with pytest.raises(AssertionError):

        _assert_equal_files(
            tmp_path / "a.ext",
            tmp_path / path_b
        )


@pytest.mark.dependency(depends=["test_equal_files", "test_unequal_files"])
def test_equal_trees(tmp_path: Path):

    prepare_tree(
        tmp_path,
        directory_map={
            "a": 0o777,
            "a/foo": 0o777,
            "a/bar": 0o775,
            "a/bar/baz": 0o755,
            "b": 0o777,
            "b/foo": 0o777,
            "b/bar": 0o775,
            "b/bar/baz": 0o755,
        },
        file_map={
            "a/a.ext": 0o777,
            "a/b.ext": 0o775,
            "a/bar/baz/c.ext": 0o755,
            "b/a.ext": 0o777,
            "b/b.ext": 0o775,
            "b/bar/baz/c.ext": 0o755,
        },
        empty_files=True
    )

    assert_equal_trees(
        tmp_path / "a",
        tmp_path / "b",
    )


@pytest.mark.dependency(depends=["test_equal_files", "test_unequal_files"])
@pytest.mark.parametrize("path_b", ["b", "c", "d", "e"])
def test_unequal_trees(path_b: str, tmp_path: Path):

    prepare_tree(
        tmp_path,
        directory_map={
            "a": 0o777,
            "a/foo": 0o777,
            "b": 0o777,
            "b/foo": 0o775,
            "c": 0o777,
            "c/foo": 0o777,
            "d": 0o777,
            "e": 0o777,
            "e/foo": 0o777,
        },
        file_map={
            "a/file.ext": 0o777,
            "b/file.ext": 0o777,
            "c/file.ext": 0o775,
            "d/file.ext": 0o777,
        },
        empty_files=True
    )

    with pytest.raises(AssertionError):

        assert_equal_trees(
            tmp_path / "a",
            tmp_path / path_b,
        )
