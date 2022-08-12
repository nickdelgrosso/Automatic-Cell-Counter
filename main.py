from __future__ import annotations

from adapters.image_processor import CellCounterImageProcessor
from adapters.image_repo import OSImageRepo
from cli import get_args
from viewer import count_cells


def main() -> None:
    args = get_args()
    count_cells(args, image_processor=CellCounterImageProcessor(), repo=OSImageRepo())


if __name__ == '__main__':
    main()
