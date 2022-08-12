from __future__ import annotations

import argparse

from cell_counter.app import App


def main() -> None:
    parser = argparse.ArgumentParser(description='Automatic cell counter')
    parser.add_argument('--image', default=False)
    args = parser.parse_args()

    app = App()
    app.count_cells(image_path=args.image)


if __name__ == '__main__':
    main()
