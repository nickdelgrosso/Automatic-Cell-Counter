from __future__ import annotations

import napari
import numpy as np

from cell_counter.workflows.count_cells import ImageViewer
from cell_counter.workflows.models import LabeledImage, LabelingResult


class NapariImageViewer(ImageViewer):
    def evaluate_labels(self, labeled_image: LabeledImage) -> LabelingResult:

        colors, bboxes = [], []
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

        viewer = napari.Viewer()

        @viewer.bind_key('d')  # denote done
        def close_viewer(viewer):
            viewer.close()

        viewer.add_image(
            data=labeled_image.image_data,  # type: ignore
            name='image',
        )

        viewer.add_shapes(
            data=np.array(bboxes),  # type: ignore
            face_color='transparent',
            edge_color='magenta',
            name='bounding box',
            edge_width=5,
        )

        points_layer = viewer.add_points(
            np.array(labeled_image.region_centroids),
            properties={
                'point_colors': np.array(colors)
            },
            face_color='point_colors',
            size=20,
            name='points',
        )

        napari.run()

        corrected_cell_num = points_layer.data.shape[0]
        result = LabelingResult(
            name=labeled_image.image_filename,
            automatic_cell_number=labeled_image.num_regions,
            corrected_cell_number=corrected_cell_num,
        )
        return result
