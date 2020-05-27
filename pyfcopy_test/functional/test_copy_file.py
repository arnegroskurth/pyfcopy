
from pathlib import Path

import pytest

from pyfcopy import copy_file
from pyfcopy_test.file_progress_listener_tester import FileProgressListenerTester


@pytest.mark.parametrize("data", [b"", b"Hello World"])
@pytest.mark.parametrize("block_size", [1, 5, 10])
def test_copy(data: bytes, block_size: int, tmp_path: Path):

    source = tmp_path / "file.ext"
    target = tmp_path / "target.ext"

    source.write_bytes(data)

    progress_listener = FileProgressListenerTester(1)

    copied_byte_count = copy_file(source, target, block_size=block_size, progress_listener=progress_listener)

    progress_listener.assert_consistent_run()

    assert target.read_bytes() == data
    assert copied_byte_count == len(data)
    assert progress_listener.last_size == len(data)


@pytest.mark.parametrize("relative_path", ["", ".", "..", "non-existent", "a-dir", "a-dir-symlink", "a-file-symlink"])
def test_invalid_source_path(relative_path: str, tmp_path: Path):

    (tmp_path / "a-file").touch()
    (tmp_path / "a-dir").mkdir()

    (tmp_path / "a-dir-symlink").symlink_to(tmp_path / "a-dir")
    (tmp_path / "a-file-symlink").symlink_to(tmp_path / "a-file")

    with pytest.raises(ValueError):

        copy_file(tmp_path / relative_path, tmp_path / "target")


def test_already_existing_target_path(tmp_path: Path):

    source = tmp_path / "file.ext"
    target = tmp_path / "target.ext"

    source.touch()
    target.touch()

    with pytest.raises(ValueError):

        copy_file(source, target)


@pytest.mark.parametrize("block_size", [0, -1, -5])
def test_invalid_block_size(block_size: int, tmp_path: Path):

    source = tmp_path / "file.ext"
    target = tmp_path / "target.ext"

    source.touch()

    with pytest.raises(ValueError):

        copy_file(source, target, block_size=block_size)
