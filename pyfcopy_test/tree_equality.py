
from pathlib import Path


def assert_equal_trees(a: Path, b: Path) -> None:

    _assert_tree_is_contained_in(a, b)
    _assert_tree_is_contained_in(b, a)


def _assert_tree_is_contained_in(a: Path, b: Path) -> None:

    assert a.is_dir()
    assert b.is_dir()

    children = [
        path.name
        for path in a.glob("*")
    ]

    for child_name in children:

        child_a = Path(a / child_name)
        child_b = Path(b / child_name)

        assert child_a.exists()
        assert child_b.exists()

        a_stat = child_a.stat()
        b_stat = child_b.stat()

        assert a_stat.st_mode == b_stat.st_mode

        if child_a.is_file() and child_b.is_file():

            _assert_equal_files(child_a, child_b)

        elif child_a.is_dir() and child_b.is_dir():

            assert_equal_trees(child_a, child_b)

        else:

            assert False


def _assert_equal_files(a: Path, b: Path) -> None:

    assert a.exists()
    assert b.exists()

    a_stat = a.stat()
    b_stat = b.stat()

    assert a_stat.st_mode == b_stat.st_mode
    assert a_stat.st_size == b_stat.st_size
    assert a.read_bytes() == b.read_bytes()
