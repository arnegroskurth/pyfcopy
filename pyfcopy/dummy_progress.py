
from typing import List

from pyfcopy.progress import TreeProgressListener, FileProgressListener


class DummyFileProgressListener(FileProgressListener):

    def start(self, size: int) -> None:
        pass

    def progress(self, chunk_size: int) -> None:
        pass

    def end(self) -> None:
        pass


class DummyTreeProgressListener(TreeProgressListener):

    def begin(self, relative_paths: List[str]) -> None:
        pass

    def next(self, relative_path: str) -> None:
        pass

    def finish(self) -> None:
        pass