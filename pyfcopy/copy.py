
import os
from pathlib import Path
from typing import Optional

from pyfcopy.dummy_progress import DummyFileProgressListener
from pyfcopy.progress import FileProgressListener


def copy(
        source_path: str,
        target_path: str,
        *,
        progress_listener: Optional[FileProgressListener] = None,
        block_size: Optional[int] = None,
    ) -> int:

    block_size = pow(2, 16) if block_size is None else block_size
    progress_listener = DummyFileProgressListener() if progress_listener is None else progress_listener

    source = Path(source_path)
    target = Path(target_path)

    if not source.is_file():
        raise ValueError(f"Given source-path is not a file: {source_path}")

    if source.is_symlink():
        raise ValueError(f"Cannot copy symlink: {source_path}")

    if target.exists():
        raise ValueError(f"Given target-path does already exist: {target_path}")

    if block_size < 1:
        raise ValueError(f"Invalid block-size: {block_size}")

    target.touch(mode=source.stat().st_mode)

    file_size = source.stat().st_size

    progress_listener.start(file_size)

    source_fd = os.open(source_path, os.O_RDONLY)
    target_fd = os.open(target_path, os.O_WRONLY | os.O_CREAT)

    current_position: int = 0
    while current_position < file_size:

        chunk_size = os.sendfile(target_fd, source_fd, offset=current_position, count=block_size)

        progress_listener.progress(chunk_size)

        current_position += chunk_size

    os.close(target_fd)
    os.close(source_fd)

    progress_listener.end()

    return current_position
