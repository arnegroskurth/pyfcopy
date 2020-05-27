
import os
from pathlib import Path
from typing import Dict


def prepare_tree(
        base_path: Path,
        *,
        directory_map: Dict[str, int] = None,
        file_map: Dict[str, int] = None,
        empty_files: bool = False
) -> None:

    def normalize_path(path: str) -> str:

        return os.sep.join(path.split("/"))

    directory_map = {} if directory_map is None else directory_map
    file_map = {} if file_map is None else file_map

    assert base_path.is_dir()

    for relative_path, file_permissions in directory_map.items():

        assert file_permissions >= 0o000
        assert file_permissions <= 0o777

        path = base_path / normalize_path(relative_path)
        path.mkdir()
        path.chmod(file_permissions)

    for relative_path, file_permissions in file_map.items():

        path = base_path / normalize_path(relative_path)

        assert not path.exists()
        assert path.parent.is_dir()

        if empty_files:

            path.touch()

        else:

            path.write_text(relative_path)

        path.chmod(file_permissions)
