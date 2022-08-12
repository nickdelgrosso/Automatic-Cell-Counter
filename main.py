from __future__ import annotations

from cli import get_args
from viewer import count_cells


def main():
    args = get_args()
    count_cells(args)


if __name__ == '__main__':
    main()
