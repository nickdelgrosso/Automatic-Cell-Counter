from __future__ import annotations

from typing import Tuple

import napari
import numpy as np

from cell_counter.workflows.count_cells import ImageViewer
from cell_counter.workflows.models import LabeledImage, LabelingResult, CellSizeEvaluation


class NapariImageViewer(ImageViewer):
    def evaluate_labels(self, labeled_image: LabeledImage) -> LabelingResult:

        viewer = napari.Viewer()

        @viewer.bind_key('d')  # denote done
        def close_viewer(viewer):
            viewer.close()

        self._show_image(labeled_image, viewer)
        self._show_region_bboxes(labeled_image, viewer)
        points_layer = self._show_cell_centroids(labeled_image, viewer)

        napari.run()

        corrected_cell_num = points_layer.data.shape[0]
        result = LabelingResult(
            name=labeled_image.image_filename,
            automatic_cell_number=labeled_image.num_regions,
            corrected_cell_number=corrected_cell_num,
        )
        return result

    def _show_cell_centroids(self, labeled_image, viewer):
        color_map = {
            CellSizeEvaluation.LargeOutlier: 'green',
            CellSizeEvaluation.AverageSize: 'green',
            CellSizeEvaluation.SmallOutlier: 'red',
        }
        colors = [color_map[size] for size in labeled_image.cell_size_evaluations]
        points_layer = viewer.add_points(
            np.array(labeled_image.region_centroids),
            properties={
                'point_colors': np.array(colors)
            },
            face_color='point_colors',
            size=20,
            name='points',
        )
        return points_layer

    def _show_region_bboxes(self, labeled_image, viewer):
        bboxes = []
        for region, size in zip(labeled_image.regions, labeled_image.cell_size_evaluations):
            if size == CellSizeEvaluation.LargeOutlier:
                bbox_rect = rect_from_bbox(*region.bbox)
                bboxes.append(bbox_rect)

        viewer.add_shapes(
            data=np.array(bboxes),  # type: ignore
            face_color='transparent',
            edge_color='magenta',
            name='bounding box',
            edge_width=5,
        )

    def _show_image(self, labeled_image, viewer):
        viewer.add_image(
            data=labeled_image.image_data,  # type: ignore
            name='image',
        )


def rect_from_bbox(minr: int, minc: int, maxr: int, maxc: int) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    return (minr, minc), (maxr, minc), (maxr, maxc), (minr, maxc)
