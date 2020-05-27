
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union


class Order(Enum):
    PRE = 1
    POST = 2


def list_tree(
        path: Union[Path, str],
        *,
        absolute: Optional[bool] = None,
        order: Optional[Order] = None,
) -> List[Path]:

    path = Path(path) if not isinstance(path, Path) else path

    absolute = False if absolute is None else absolute
    order = Order.PRE if order is None else order

    if not path.is_dir():
        raise ValueError(f"Given path is not a directory: {path}")

    if order not in [Order.PRE, Order.POST]:
        raise ValueError(f"Invalid order.")

    paths = list(path.rglob("*"))

    if not absolute:

        # trim absolute to relative paths
        paths = [
            absolute_path.relative_to(path)
            for absolute_path in paths
        ]

    if order == Order.PRE:

        paths.sort(reverse=False)

    elif order == Order.POST:

        paths.sort(reverse=True)

    else:

        raise Exception()

    return paths
