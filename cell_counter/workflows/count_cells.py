from __future__ import annotations

from typing import NamedTuple, Protocol, List

from cell_counter.workflows.models import Image, LabeledImage, LabelingResult


class ImageProcessor(Protocol):
    def imread(self, path: str) -> Image: ...
    def label_image(self, image: Image) -> LabeledImage: ...


class ImageRepo(Protocol):
    def get_list_of_files(self, path: str) -> List[str]: ...
    def write_counts_to_excel(self, results: List[LabelingResult], filename: str) -> None: ...


class ImageViewer(Protocol):
    def evaluate_labels(self, labeled_image: LabeledImage) -> LabelingResult: ...


class CountCellsWorkflow(NamedTuple):
    image_processor: ImageProcessor
    repo: ImageRepo
    viewer: ImageViewer

    def __call__(self, image_path: str, export_filename: str = 'result.xlsx') -> None:
        results = []
        for image_filename in self.repo.get_list_of_files(image_path):

            image = self.image_processor.imread(image_filename)
            labeled_image = self.image_processor.label_image(image=image)
            print('Number of cells detected with automatic method:', labeled_image.num_regions)

            result = self.viewer.evaluate_labels(labeled_image=labeled_image)
            print('Number of cells after manual correction: ', result.corrected_cell_number)

            results.append(result)

        self.repo.write_counts_to_excel(results, filename=export_filename)
        print(f'Done! All results are saved in {export_filename}')


