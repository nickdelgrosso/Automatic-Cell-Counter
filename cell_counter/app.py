from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cell_counter.workflows.count_cells import CountCellsWorkflow

class App:

    @property
    def count_cells(self) -> CountCellsWorkflow:
        from cell_counter.image_processors.image_processor import CellCounterImageProcessor
        from cell_counter.repos.image_repo import OSImageRepo
        from cell_counter.viewers.napari_viewer import NapariImageViewer
        from cell_counter.workflows.count_cells import CountCellsWorkflow
        return CountCellsWorkflow(
            image_processor=CellCounterImageProcessor(),
            repo=OSImageRepo(),
            viewer=NapariImageViewer(),
        )