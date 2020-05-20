from pathlib import Path

from pyfcopy_test.tree_fixture import prepare_tree


def test_empty(tmp_path):

    prepare_tree(tmp_path, directory_map={}, file_map={})

    assert list(Path(tmp_path).glob("*")) == []


def test_simple(tmp_path):

    prepare_tree(
        tmp_path,
        directory_map={
            "foo": 0o777,
            "bar": 0o775,
            "foo/baz": 0o755,
        },
        file_map={
            "a.ext": 0o777,
            "bar/b.ext": 0o775,
            "foo/baz/c.ext": 0o755,
        }
    )

    assert Path(tmp_path / "foo").is_dir()
    assert Path(tmp_path / "foo").stat().st_mode & 0o777 == 0o777
    assert Path(tmp_path / "bar").is_dir()
    assert Path(tmp_path / "bar").stat().st_mode & 0o777 == 0o775
    assert Path(tmp_path / "foo/baz").is_dir()
    assert Path(tmp_path / "foo/baz").stat().st_mode & 0o777 == 0o755

    assert Path(tmp_path / "a.ext").is_file()
    assert Path(tmp_path / "a.ext").stat().st_mode & 0o777 == 0o777
    assert Path(tmp_path / "a.ext").read_text() == "a.ext"
    assert Path(tmp_path / "bar/b.ext").is_file()
    assert Path(tmp_path / "bar/b.ext").stat().st_mode & 0o777 == 0o775
    assert Path(tmp_path / "bar/b.ext").read_text() == "bar/b.ext"
    assert Path(tmp_path / "foo/baz/c.ext").is_file()
    assert Path(tmp_path / "foo/baz/c.ext").stat().st_mode & 0o777 == 0o755
    assert Path(tmp_path / "foo/baz/c.ext").read_text() == "foo/baz/c.ext"


def test_empty_files(tmp_path):

    prepare_tree(
        tmp_path,
        file_map={
            "file.ext": 0o777,
        },
        empty_files=True
    )

    assert Path(tmp_path / "file.ext").read_text() == ""
