from __future__ import annotations

from typing import List, Optional

import napari
import numpy as np
from numpy.typing import NDArray

from viewer import Region, LabelingResult, ImageViewer


class NapariImageViewer(ImageViewer):
    def evaluate_labels(self, filename: str, img: NDArray, median_size: float, regions: List[Region]) -> LabelingResult:
        points_array = np.array([region.centroid for region in regions])
        colors = []
        bboxes = []
        for region in regions:
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
        point_properties = {
            'point_colors': np.array(colors)
        }
        bboxes_array = np.array(bboxes)
        print('Image name: ', filename)
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
            name=filename,
            automatic_cell_number=len(points_array),
            corrected_cell_number=corrected_cell_num,
        )
        return result


