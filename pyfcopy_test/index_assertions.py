
from pathlib import Path
from typing import List, Union, Set


def assert_same_index(actual_index: List[Path], expected_index: Union[List[Path], List[str], Set[Path], Set[str]]) -> None:

    if type(expected_index) is list:

        actual_index = [str(path) for path in actual_index]
        expected_index = [str(path) for path in expected_index]

    elif type(expected_index) is set:

        actual_index = {str(path) for path in actual_index}
        expected_index = {str(path) for path in expected_index}

    else:
        raise ValueError()

    assert actual_index == expected_index
