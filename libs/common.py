# -*- coding: utf-8 -*-

import glob
from pathlib import Path
import os
import tempfile

def relocate_data(the_data_path):
    safe_place = tempfile.TemporaryDirectory(delete=False)
    scanerella(the_data_path,safe_place.name)

    return safe_place.name+the_data_path

def scanerella(data_path,new_place,depth=0):
    """
    scans the dir
    symlink files
    do recursive if another dir
    """
    Path(new_place+data_path).mkdir(parents=True, exist_ok=True)
    for file in glob.iglob(data_path+"/*", recursive=True):
        if os.path.isdir(file):
            scanerella(file,new_place,depth+1)
        else:
            Path(new_place+file).symlink_to(file)
