from __future__ import annotations

from cell_counter.image_processors.image_processor import CellCounterImageProcessor
from cell_counter.io.image_repo import OSImageRepo
from cell_counter.viewers.napari_viewer import NapariImageViewer
from cell_counter.use_cases.count_cells import CountCellsProgram

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
