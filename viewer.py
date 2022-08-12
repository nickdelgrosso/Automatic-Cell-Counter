from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING, Protocol, List, Tuple, Optional

if TYPE_CHECKING:
    from numpy.typing import NDArray

import napari
import numpy as np


class CountCellArgs(NamedTuple):
    image: str


class Region(Protocol):
    centroid: Tuple[float, float]
    area: int
    bbox: Tuple[int, int, int, int]


class ImageProcessor(Protocol):
    def label_image(self, img: NDArray) -> NDArray: ...
    def find_median_cell_size(self, labeled_img: NDArray) -> float: ...
    def apply_watershed(self, labeled_img: NDArray, median_size: float) -> NDArray: ...
    def get_region_properties(self, bin_img: NDArray) -> List[Region]: ...


class LabelingResult(NamedTuple):
    name: str
    automatic_cell_number: int
    corrected_cell_number: Optional[int]


class ImageRepo(Protocol):
    def get_list_of_files(self, path: str) -> List[str]: ...
    def imread(self, path: str) -> NDArray: ...
    def write_counts_to_excel(self, results: List[LabelingResult], filename: str) -> None: ...


def count_cells(args: CountCellArgs, image_processor: ImageProcessor, repo: ImageRepo) -> None:
    path = args.image
    listOfFiles = repo.get_list_of_files(path)

    results: List[LabelingResult] = []
    # image process
    for image in listOfFiles:

        img = repo.imread(image)

        final = image_processor.label_image(img)
        median_size = image_processor.find_median_cell_size(final)
        cell_number = len(np.unique(final)) - 1
        # only apply watershed when the detected cell number is larger than 150
        if cell_number > 150:
            final = image_processor.apply_watershed(final, median_size)

        # viewer
        points = []
        colors = []
        bboxes = []
        i = 0
        for region in image_processor.get_region_properties(final):
            y, x = region.centroid
            if region.area >= 2 * median_size:
                # bound
                minr, minc, maxr, maxc = region.bbox
                bbox_rect = np.array([[minr, minc], [maxr, minc], [maxr, maxc], [minr, maxc]])
                colors.append('green')  # 0.1)
                bboxes.append(bbox_rect)

            elif region.area < median_size / 2:
                colors.append('red')
            else:
                colors.append('green')

            points.append([y, x])

        points_array = np.array(points)
        point_properties = {
            'point_colors': np.array(colors)
        }
        bboxes_array = np.array(bboxes)
        print('Image name: ', image)
        print('Number of cells detected with automatic method: ', len(points_array))

        # with napari.gui_qt():
        viewer = napari.view_image(img, name='image')
        if len(bboxes_array) > 0:
            shapes_layer = viewer.add_shapes(bboxes_array,
                                             face_color='transparent',
                                             edge_color='magenta',
                                             name='bounding box',
                                             edge_width=5)
        if len(points_array) > 0:
            points_layer = viewer.add_points(points_array,
                                             properties=point_properties,
                                             face_color='point_colors',
                                             size=20,
                                             name='points')

        corrected_cell_num: Optional[int] = None

        @viewer.bind_key('d')  # denote done
        def update_cell_numbers(viewer):
            num_cells = viewer.layers['points'].data.shape[0]
            print('Number of cells after manual correction: ', num_cells)
            nonlocal corrected_cell_num
            corrected_cell_num = num_cells
            viewer.close()

        napari.run()

        result = LabelingResult(
            name=image,
            automatic_cell_number=len(points_array),
            corrected_cell_number=corrected_cell_num,
        )
        results.append(result)

    export_filename = 'result.xlsx'
    repo.write_counts_to_excel(results, filename=export_filename)
    print(f'Done! All results are saved in {export_filename}')
