from __future__ import annotations

from statistics import median
from typing import NamedTuple, Tuple, List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from numpy._typing import NDArray


class Region(NamedTuple):
    centroid: Tuple[float, float]
    area: int
    bbox: Tuple[int, int, int, int]


class Image(NamedTuple):
    filename: str
    data: NDArray


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
    def image_data(self) -> NDArray:
        return self.image.data

    @property
    def image_filename(self) -> str:
        return self.image.filename


class LabelingResult(NamedTuple):
    name: str
    automatic_cell_number: int
    corrected_cell_number: Optional[int]
