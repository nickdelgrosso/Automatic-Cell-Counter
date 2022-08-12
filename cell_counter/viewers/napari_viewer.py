from __future__ import annotations

import napari
import numpy as np

from cell_counter.workflows.count_cells import ImageViewer
from cell_counter.workflows.models import LabeledImage, LabelingResult


class NapariImageViewer(ImageViewer):
    def evaluate_labels(self, labeled_image: LabeledImage) -> LabelingResult:
        points_array = np.array([region.centroid for region in labeled_image.regions])
        colors = []
        bboxes = []
        for region in labeled_image.regions:
            median_size = labeled_image.median_cell_size
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

        # with napari.gui_qt():
        viewer = napari.view_image(labeled_image.image_data, name='image')  # type: ignore
        if len(bboxes_array) > 0:
            viewer.add_shapes(
                bboxes_array,
                face_color='transparent',
                edge_color='magenta',
                name='bounding box',
                edge_width=5,
            )
        if len(points_array) > 0:
            viewer.add_points(
                points_array,
                properties=point_properties,
                face_color='point_colors',
                size=20,
                name='points',
            )

        corrected_cell_num: int = labeled_image.num_regions
        @viewer.bind_key('d')  # denote done
        def update_cell_numbers(viewer):
            num_cells = viewer.layers['points'].data.shape[0]
            print('Number of cells after manual correction: ', num_cells)
            nonlocal corrected_cell_num
            corrected_cell_num = num_cells
            viewer.close()

        napari.run()

        result = LabelingResult(
            name=labeled_image.image_filename,
            automatic_cell_number=labeled_image.num_regions,
            corrected_cell_number=corrected_cell_num,
        )
        return result
