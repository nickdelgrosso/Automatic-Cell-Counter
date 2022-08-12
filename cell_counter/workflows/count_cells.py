from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING, Protocol, List, Tuple, Optional
from dataclasses import dataclass

if TYPE_CHECKING:
    from numpy.typing import NDArray



class Region(Protocol):
    centroid: Tuple[float, float]
    area: int
    bbox: Tuple[int, int, int, int]


class ImageProcessor(Protocol):
    def imread(self, path: str) -> NDArray: ...
    def label_image(self, img: NDArray) -> NDArray: ...
    def find_median_cell_size(self, labeled_img: NDArray) -> float: ...
    def apply_watershed(self, labeled_img: NDArray, median_size: float) -> NDArray: ...
    def get_regions(self, bin_img: NDArray) -> List[Region]: ...
    def count_regions(self, labeled_image: NDArray) -> int: ...


class LabelingResult(NamedTuple):
    name: str
    automatic_cell_number: int
    corrected_cell_number: Optional[int]


class ImageRepo(Protocol):
    def get_list_of_files(self, path: str) -> List[str]: ...
    def write_counts_to_excel(self, results: List[LabelingResult], filename: str) -> None: ...


class ImageViewer(Protocol):
    def evaluate_labels(self, img: NDArray, median_size: float, regions: List[Region]) -> int: ...



@dataclass
class CountCellsWorkflow:
    image_processor: ImageProcessor
    repo: ImageRepo
    viewer: ImageViewer

    def __call__(self, image_path: str, export_filename: str = 'result.xlsx') -> None:
        results: List[LabelingResult] = []

        for image_filename in self.repo.get_list_of_files(image_path):
            img = self.image_processor.imread(image_filename)
            labeled_image = self.image_processor.label_image(img)
            median_size = self.image_processor.find_median_cell_size(labeled_image)
            cell_number = self.image_processor.count_regions(labeled_image=labeled_image)

            # only apply watershed when the detected cell number is larger than 150
            if cell_number > 150:
                labeled_image = self.image_processor.apply_watershed(labeled_image, median_size)

            regions = self.image_processor.get_regions(labeled_image)
            automatic_cell_count = len(regions)
            print('Number of cells detected with automatic method:', automatic_cell_count)

            corrected_cell_count = self.viewer.evaluate_labels(img=img, median_size=median_size, regions=regions)
            result = LabelingResult(
                name=image_filename,
                automatic_cell_number=automatic_cell_count,
                corrected_cell_number=corrected_cell_count,
            )
            results.append(result)

        self.repo.write_counts_to_excel(results, filename=export_filename)
        print(f'Done! All results are saved in {export_filename}')


