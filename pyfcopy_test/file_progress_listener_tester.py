
from typing import Optional

from pyfcopy import FileProgressListener


class FileProgressListenerTester(FileProgressListener):

    def __init__(self, expected_count: Optional[int] = None):

        self._expected_count = expected_count
        self._current_count_indicator = 0

        self.current_progress = None
        self.last_size = None

    def start(self, size: int) -> None:

        assert self._current_count_indicator % 2 == 0

        self._current_count_indicator += 1
        self.current_progress = 0
        self.last_size = size

    def progress(self, chunk_size: int) -> None:

        assert self._current_count_indicator % 2 == 1

        self.current_progress += chunk_size

        assert self.current_progress <= self.last_size

    def end(self) -> None:

        assert self._current_count_indicator % 2 == 1
        assert self.current_progress == self.last_size

        self._current_count_indicator += 1

    def assert_consistent_run(self):

        assert self._current_count_indicator % 2 == 0
        assert self._expected_count is None or self._current_count_indicator / 2 == self._expected_count
