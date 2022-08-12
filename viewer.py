from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING, Protocol, List, Tuple, Optional

if TYPE_CHECKING:
    from numpy.typing import NDArray


class CountCellArgs(NamedTuple):
    image: str
    export_filename: str = 'result.xlsx'


class Region(Protocol):
    centroid: Tuple[float, float]
    area: int
    bbox: Tuple[int, int, int, int]


class ImageProcessor(Protocol):
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
    def imread(self, path: str) -> NDArray: ...
    def write_counts_to_excel(self, results: List[LabelingResult], filename: str) -> None: ...


class ImageViewer(Protocol):
    def evaluate_labels(self, filename: str, img: NDArray, median_size: float, regions: List[Region]) -> LabelingResult: ...


def count_cells(args: CountCellArgs, image_processor: ImageProcessor, repo: ImageRepo, viewer: ImageViewer) -> None:
    path = args.image
    results: List[LabelingResult] = []

    for image in repo.get_list_of_files(path):
        img = repo.imread(image)
        labeled_image = image_processor.label_image(img)
        median_size = image_processor.find_median_cell_size(labeled_image)
        cell_number = image_processor.count_regions(labeled_image=labeled_image)

        # only apply watershed when the detected cell number is larger than 150
        if cell_number > 150:
            labeled_image = image_processor.apply_watershed(labeled_image, median_size)

        regions = image_processor.get_regions(labeled_image)
        result = viewer.evaluate_labels(filename=image, img=img, median_size=median_size, regions=regions)
        results.append(result)

    repo.write_counts_to_excel(results, filename=args.export_filename)
    print(f'Done! All results are saved in {args.export_filename}')


