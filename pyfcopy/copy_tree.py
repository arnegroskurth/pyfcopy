
from pathlib import Path
from typing import Optional

from pyfcopy import copy
from pyfcopy.dummy_progress import DummyTreeProgressListener
from pyfcopy.progress import TreeProgressListener, FileProgressListener


def copy_tree(
        source_path: str,
        target_path: str,
        *,
        tree_progress_listener: Optional[TreeProgressListener] = None,
        file_progress_listener: Optional[FileProgressListener] = None,
        block_size: Optional[int] = None,
) -> int:

    tree_progress_listener = DummyTreeProgressListener() if tree_progress_listener is None else tree_progress_listener

    source = Path(source_path)
    target = Path(target_path)

    if not source.is_dir():
        raise ValueError(f"Given source-path is not a directory: {source_path}")

    if source.is_symlink():
        raise ValueError(f"Given source-path is a symlink: {source_path}")

    if target.exists():
        raise ValueError(f"Given target-path does already exist: {target_path}")

    if str(target.resolve()).startswith(str(source.resolve())):
        raise ValueError("Cannot copy tree into itself.")

    relative_paths = [
        str(absolute_path)[len(source_path) + 1:]
        for absolute_path in source.rglob("*")
    ]

    tree_progress_listener.begin(relative_paths)

    target.mkdir()
    target.chmod(source.stat().st_mode)

    for current_relative_path in relative_paths:

        tree_progress_listener.next(current_relative_path)

        current_source_path = source / current_relative_path
        current_target_path = target / current_relative_path

        if current_source_path.is_file():

            copy(current_source_path, current_target_path,
                 progress_listener=file_progress_listener, block_size=block_size)

        elif current_source_path.is_dir():

            current_target_path.mkdir()
            current_target_path.chmod(current_source_path.stat().st_mode)

        else:

            raise Exception()

    tree_progress_listener.finish()

    return len(relative_paths)
