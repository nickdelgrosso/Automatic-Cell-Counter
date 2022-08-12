from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING, Protocol, List, Tuple

if TYPE_CHECKING:
    from numpy.typing import NDArray

import napari
import numpy as np

import pandas as pd
from skimage.io import imread


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



class ImageRepo(Protocol):
    def get_list_of_files(self, path: str) -> List[str]: ...



def count_cells(args: CountCellArgs, image_processor: ImageProcessor, repo: ImageRepo) -> None:


    path = args.image
    listOfFiles = repo.get_list_of_files(path)
    
    result = []
    # image process
    for image in listOfFiles:
        img = imread(image)  

        final = image_processor.label_image(img)
        median_size = image_processor.find_median_cell_size(final)
        cell_number = len(np.unique(final))-1
        # only apply watershed when the detected cell number is larger than 150
        if cell_number > 150: 
            final = image_processor.apply_watershed(final, median_size)

        # viewer
        points = [] 
        colors = []
        bboxes = []
        i=0
        for region in image_processor.get_region_properties(final):
            y,x = region.centroid
            if region.area >= 2*median_size:       
                #bound
                minr, minc, maxr, maxc = region.bbox
                bbox_rect = np.array([[minr, minc], [maxr, minc], [maxr, maxc], [minr, maxc]])
                colors.append('green') #0.1)
                bboxes.append(bbox_rect)

            elif region.area < median_size/2:
                colors.append('red')
            else:
                colors.append('green')

            points.append([y,x])

        points_array=np.array(points)
        point_properties={
            'point_colors': np.array(colors)
        }
        bboxes_array = np.array(bboxes)
        print('Image name: ',image)
        print('Number of cells detected with automatic method: ', len(points_array))
        result.append([image,len(points_array)])

        #with napari.gui_qt():
        viewer = napari.view_image(img, name='image')
        if len(bboxes_array)>0:
            shapes_layer = viewer.add_shapes(bboxes_array,
                                    face_color='transparent',
                                    edge_color='magenta',
                                    name='bounding box',
                                    edge_width=5)
        if len(points_array)>0:
            points_layer = viewer.add_points(points_array,
                                    properties=point_properties,
                                    face_color='point_colors',
                                    size=20,
                                    name='points')

        @viewer.bind_key('d') # denote done
        def update_cell_numbers(viewer):
            num_cells = viewer.layers['points'].data.shape[0]
            print('Number of cells after manual correction: ', num_cells)
            result[-1].append(num_cells)
            viewer.close()
        
        napari.run()
    
        if len(result[-1]) == 2:
            result[-1].append(None)
            
    df = pd.DataFrame(result, columns =['Name', 'Automatic Cell Number','Corrected Cell Number']) 
    df.to_excel('result.xlsx')
    print('Done! All results are saved in result.xlsx!')






