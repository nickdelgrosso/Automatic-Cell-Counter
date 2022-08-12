from __future__ import annotations

import argparse

from viewer import CountCellArgs


def get_args() -> CountCellArgs:
    parser = argparse.ArgumentParser(description='Automatic cell counter')
    parser.add_argument('--image', default=False)
    args = parser.parse_args()
    cell_args = CountCellArgs(image_path=args.image)
    return cell_args
