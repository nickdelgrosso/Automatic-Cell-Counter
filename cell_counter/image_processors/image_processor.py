from typing import List

import numpy as np
from numpy.typing import NDArray
from skimage.io import imread
from skimage.measure import label, regionprops

from cell_counter.image_processors.utils import get_binary_map, apply_opening, find_median_cell_size, apply_watershed
from cell_counter.workflows.count_cells import ImageProcessor, Region


class CellCounterImageProcessor(ImageProcessor):

    def imread(self, path: str) -> NDArray:
        return imread(path)

    def get_regions(self, img: NDArray, watershed_threshold=150) -> List[Region]:
        labeled_image = label(apply_opening(binary_img=get_binary_map(img)))

        # only apply watershed when the detected cell number is larger than 150
        cell_number = len(np.unique(labeled_image)) - 1
        if cell_number > watershed_threshold:
            median_size = find_median_cell_size(labeled_img=labeled_image)
            labeled_image = apply_watershed(labeled_img=labeled_image, median_size=median_size)

        # Extract Region Info
        regions_skimage = regionprops(labeled_image)
        regions = [Region(centroid=r.centroid, area=r.area, bbox=r.bbox) for r in regions_skimage]
        return regions

    def get_median_cell_size(self, regions: List[Region]) -> float:
        return float(np.median([region.area for region in regions]))
