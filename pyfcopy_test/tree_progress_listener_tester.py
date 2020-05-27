
from pathlib import Path
from typing import Set, Optional, List, Union

from pyfcopy import TreeProgressListener


class TreeProgressListenerTester(TreeProgressListener):

    def __init__(self, expected_paths: Optional[Union[Set[str], List[str]]] = None):

        self._expected_paths = expected_paths

        self.current_step_index = None
        self.current_relative_path = None

    def begin(self, relative_paths: List[Path]) -> None:

        relative_paths = [str(path) for path in relative_paths]

        assert self.current_step_index is None

        if type(self._expected_paths) is list:

            assert self._expected_paths == relative_paths

        elif type(self._expected_paths) is set:

            assert self._expected_paths == set(relative_paths)

        else:

            assert self._expected_paths is None

        self.current_step_index = 0

    def next(self, relative_path: Path) -> None:

        relative_path = str(relative_path)

        assert self.current_step_index is not None
        assert self._expected_paths is None or relative_path in self._expected_paths

        if type(self._expected_paths) is list:

            assert self.current_step_index < len(self._expected_paths)
            assert self._expected_paths[self.current_step_index] == relative_path

        self.current_step_index += 1

    def finish(self) -> None:

        assert self.current_step_index is not None

        self.current_step_index = None
        self.current_relative_path = None

    def assert_consistent_run(self):

        assert self.current_step_index is None
