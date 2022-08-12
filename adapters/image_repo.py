from __future__ import annotations

import glob
import os
from typing import List

import pandas as pd
from numpy.typing import NDArray
from skimage.io import imread

from viewer import ImageRepo, LabelingResult


class OSImageRepo(ImageRepo):

    def get_list_of_files(self, path: str) -> List[str]:
        return glob.glob(os.path.join(path, "**/*.*"), recursive=True) if os.path.isdir(path) else [path]

    def imread(self, path: str) -> NDArray:
        return imread(path)

    def write_counts_to_excel(self, results: List[LabelingResult], filename: str) -> None:
        df = pd.DataFrame(results, columns=['Name', 'Automatic Cell Number', 'Corrected Cell Number'])
        df.to_excel(filename)
