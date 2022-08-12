from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cell_counter.use_cases.count_cells import CountCellsProgram


def get_cell_counter() -> CountCellsProgram:
    from cell_counter.image_processors.image_processor import CellCounterImageProcessor
    from cell_counter.io.image_repo import OSImageRepo
    from cell_counter.viewers.napari_viewer import NapariImageViewer
    from cell_counter.use_cases.count_cells import CountCellsProgram
    return CountCellsProgram(
        image_processor=CellCounterImageProcessor(),
        repo=OSImageRepo(),
        viewer=NapariImageViewer(),
    )