from __future__ import annotations

import os
from typing import List, Tuple, Optional

from numpy.typing import NDArray
from skimage.io import imread
import pandas as pd

from viewer import ImageRepo, LabelingResult


class OSImageRepo(ImageRepo):

    def get_list_of_files(self, path: str) -> List[str]:
        if os.path.isdir(path):
            listOfFiles = list()
            for (dirpath, dirnames, filenames) in os.walk(path):
                filenames = [f for f in filenames if not f[0] == '.']
                dirnames[:] = [d for d in dirnames if not d[0] == '.']
                print(dirpath)
                filenames.sort()  # key=lambda x: int(x.split(".")[0]))
                listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        else:
            listOfFiles = [path]
        return listOfFiles

    def imread(self, path: str) -> NDArray:
        return imread(path)

    def write_counts_to_excel(self, results: List[LabelingResult], filename: str) -> None:
        df = pd.DataFrame(results, columns=['Name', 'Automatic Cell Number', 'Corrected Cell Number'])
        df.to_excel(filename)