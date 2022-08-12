from __future__ import annotations

import os
from typing import List

from viewer import ImageRepo


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
