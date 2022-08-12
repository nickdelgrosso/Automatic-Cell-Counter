from typing import List

import numpy as np
from numpy.typing import NDArray
from skimage.io import imread
from skimage.measure import label, regionprops

from cell_counter.image_processors.utils import get_binary_map, apply_opening, find_median_cell_size, apply_watershed
from cell_counter.programs.count_cells import ImageProcessor, Region


class CellCounterImageProcessor(ImageProcessor):

    def imread(self, path: str) -> NDArray:
        return imread(path)

    def label_image(self, img: NDArray) -> NDArray:
        return label(apply_opening(binary_img=get_binary_map(img)))

    def find_median_cell_size(self, labeled_img: NDArray) -> float:
        return find_median_cell_size(labeled_img=labeled_img)

    def apply_watershed(self, labeled_img: NDArray, median_size: float) -> NDArray:
        return apply_watershed(labeled_img=labeled_img, median_size=median_size)

    def get_regions(self, bin_img: NDArray) -> List[Region]:
        return regionprops(bin_img)

    def count_regions(self, labeled_image: NDArray) -> int:
        return len(np.unique(labeled_image)) - 1
