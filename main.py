from __future__ import annotations

from cli import get_args
from viewer import count_cells
from CellCounter import CellCounterImageProcessor
from image_repo import OSImageRepo


def main() -> None:
    args = get_args()
    count_cells(args, image_processor=CellCounterImageProcessor(), repo=OSImageRepo())


if __name__ == '__main__':
    main()
