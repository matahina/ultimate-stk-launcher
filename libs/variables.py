# -*- coding: utf-8 -*-

# Main variables

from configparser import ConfigParser
import pandas as pd
import libs.common
import os



def init():
    global ustkl_config
    global orig_directory
    global de_name
    global assets_data
    global addon_lib
    global lock
    global data_relocation
    global assets_relocation
    global online_db
    global issvn
    global version

    ustkl_config = ConfigParser()
    ustkl_config.read("magic_config.ini")
    orig_directory = os.getcwd()
    de_name = os.getenv("XDG_CURRENT_DESKTOP")
    assets_data = pd.read_csv('libs/sources.csv')
    assets_data = assets_data.fillna("")
    assets_data = assets_data.assign(downloaded = [""] * len(assets_data["id"]))
    addon_lib = libs.common.AddonLibrary()
    online_db = libs.common.OnlineDatabase()
    lock = 0
    data_relocation = ""
    assets_relocation = ""
    issvn = ["editor",
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
    version = "2025.03.alpha3"
