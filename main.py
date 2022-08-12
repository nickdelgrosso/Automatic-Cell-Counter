from __future__ import annotations

from adapters.image_processor import CellCounterImageProcessor
from adapters.image_repo import OSImageRepo
from adapters.viewer import NapariImageViewer
from viewer import CountCellsProgram

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description='Automatic cell counter')
    parser.add_argument('--image', default=False)
    args = parser.parse_args()

    count_cells = CountCellsProgram(
        image_processor=CellCounterImageProcessor(),
        repo=OSImageRepo(),
        viewer=NapariImageViewer(),
    )
    count_cells(image_path=args.image)


if __name__ == '__main__':
    main()
