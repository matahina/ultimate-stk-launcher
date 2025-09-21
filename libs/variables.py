# -*- coding: utf-8 -*-

# Main variables

from configparser import ConfigParser
import libs.common
import libs.assets
import os
import logging
import datetime
from pathlib import Path



def init():
    global ustkl_config
    global orig_directory
    global de_name
    global assets_data
    global recipes_lib
    global addon_lib
    global lock
    global data_relocation
    global assets_relocation
    global online_db
    global is_asset
    global version
    global mylog
    global mylogfile

    ustkl_config = ConfigParser()
    ustkl_config.read("magic_config.ini")
    orig_directory = str(Path.cwd())
    de_name = os.getenv("XDG_CURRENT_DESKTOP")
    assets_data = libs.assets.AssetDict()
    recipes_lib = libs.assets.RecipeDict()
    addon_lib = libs.common.AddonLibrary()
    online_db = libs.common.OnlineDatabase()
    lock = 0
    data_relocation = ""
    assets_relocation = ""
    is_asset = ["editor",
         "karts",
        "library",
        "models",
        "music",
        "sfx",
        "textures",
        "tracks",
        "wip-karts",
        "wip-library",
        "wip-tracks"]
    version = "2025.09.beta3"
    mylog = logging.getLogger("ustkl")
    mylogfile = libs.common.pathery(["logs",datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.log'])
    logging.basicConfig(filename=mylogfile, encoding='utf-8', level=logging.DEBUG, format="%(asctime)s | %(message)s")
