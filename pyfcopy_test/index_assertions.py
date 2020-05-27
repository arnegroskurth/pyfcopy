
from pathlib import Path
from typing import List, Union


def assert_same_index(actual_index: List[Path], expected_index: Union[List[Path], List[str]]) -> None:

    actual_index = [str(path) for path in actual_index]
    expected_index = [str(path) for path in expected_index]

    assert actual_index == expected_index
