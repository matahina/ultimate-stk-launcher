# -*- coding: utf-8 -*-

# Main variables

from configparser import ConfigParser
import libs.common
import libs.assets
import os
import logging
import datetime



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
    global mylog
    global mylogfile

    ustkl_config = ConfigParser()
    ustkl_config.read("magic_config.ini")
    orig_directory = os.getcwd()
    de_name = os.getenv("XDG_CURRENT_DESKTOP")
    assets_data = libs.assets.AssetDict()
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
    version = "2025.09.beta2"
    mylog = logging.getLogger("ustkl")
    mylogfile = libs.variables.orig_directory+"/logs/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+'.log'
    logging.basicConfig(filename=mylogfile, encoding='utf-8', level=logging.DEBUG, format="%(asctime)s | %(message)s")
