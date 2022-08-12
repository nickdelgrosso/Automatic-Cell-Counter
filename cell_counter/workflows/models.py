from __future__ import annotations

from statistics import median
from typing import NamedTuple, Tuple, List, TYPE_CHECKING, Optional, Iterator
from enum import Enum


if TYPE_CHECKING:
    from numpy._typing import NDArray


class Region(NamedTuple):
    centroid: Tuple[float, float]
    area: int
    bbox: Tuple[int, int, int, int]


class Image(NamedTuple):
    filename: str
    data: NDArray


class CellSizeEvaluation(Enum):
    SmallOutlier = 1
    AverageSize = 2
    LargeOutlier = 3


class LabeledImage(NamedTuple):
    image: Image
    regions: List[Region]

    @property
    def num_regions(self) -> int:
        return len(self.regions)

    @property
    def median_cell_size(self) -> float:
        return float(median([region.area for region in self.regions]))

    @property
    def cell_size_evaluations(self) -> Iterator[CellSizeEvaluation]:
        median_size = self.median_cell_size
        for region in self.regions:
            if region.area >= 2 * median_size:
                yield CellSizeEvaluation.LargeOutlier
            elif region.area < median_size / 2:
                yield CellSizeEvaluation.SmallOutlier
            else:
                yield CellSizeEvaluation.AverageSize

    @property
    def image_data(self) -> NDArray:
        return self.image.data

    @property
    def image_filename(self) -> str:
        return self.image.filename

    @property
    def region_centroids(self) -> List[Tuple[float, float]]:
        return [region.centroid for region in self.regions]


class LabelingResult(NamedTuple):
    name: str
    automatic_cell_number: int
    corrected_cell_number: Optional[int]
