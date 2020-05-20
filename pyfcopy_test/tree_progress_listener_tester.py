
from typing import Set, Optional, List

from pyfcopy import TreeProgressListener


class TreeProgressListenerTester(TreeProgressListener):

    def __init__(self, expected_paths: Optional[Set[str]] = None):

        self._expected_paths = expected_paths

        self.currently_running = False
        self.current_relative_path = None

    def begin(self, relative_paths: List[str]) -> None:

        assert self.currently_running is False
        assert self._expected_paths is None or set(relative_paths) == self._expected_paths

        self.currently_running = True

    def next(self, relative_path: str) -> None:

        assert self.currently_running
        assert self._expected_paths is None or relative_path in self._expected_paths

    def finish(self) -> None:

        assert self.currently_running

        self.currently_running = False
        self.current_relative_path = None

    def assert_consistent_run(self):

        assert self.currently_running is False
