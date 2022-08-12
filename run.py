from __future__ import annotations

import argparse

from cell_counter.api import get_cell_counter


def main() -> None:
    parser = argparse.ArgumentParser(description='Automatic cell counter')
    parser.add_argument('--image', default=False)
    args = parser.parse_args()

    count_cells = get_cell_counter()
    count_cells(image_path=args.image)


if __name__ == '__main__':
    main()
