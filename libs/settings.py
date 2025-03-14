# -*- coding: utf-8 -*-

from configparser import ConfigParser
import os
import pandas as pd
from lxml import etree
import xml.etree.ElementTree as ET

def init():
    global ustkl_config
    global orig_directory
    global de_name
    global assets_data
    global addon_lib
    global lock

    ustkl_config = ConfigParser()
    ustkl_config.read("magic_config.ini")
    orig_directory = os.getcwd()
    de_name = os.getenv("XDG_CURRENT_DESKTOP")
    assets_data = pd.read_csv('libs/sources.csv')
    assets_data = assets_data.fillna("")
    assets_data = assets_data.assign(downloaded = [""] * len(assets_data["id"]))
    addon_lib = AddonLibrary()
    lock = 0

class AddonLibrary:
    def __init__(self):
        self.mytree = []
        self.stk_tree = []
        self.upd_track = []
        self.to_inst_track = []
        self.upd_arena = []
        self.to_inst_arena = []
        self.avail_tracks = []
        self.installed_tracks = []
        self.avail_arenas = []
        self.installed_arenas = []

    def init_mytree(self):
        try:
            self.mytree = ET.parse(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
        except:
            self.mytree = []

    def init_stk_tree(self):
        try:
            self.stk_tree = etree.parse(orig_directory+"/tmp_files/online_assets.xml")
        except:
            self.stk_tree = []

    def init_avail_tracks(self):
        self.avail_tracks = []
        if self.stk_tree != []:
            for user in self.stk_tree.xpath("/assets/track"):
                self.avail_tracks.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

    def init_installed_tracks(self):
        self.installed_tracks = []
        if self.mytree != []:
            root = self.mytree.getroot()
            for child in root:
                if child.tag == '{https://online.supertuxkart.net/}track':
                    if child.attrib['installed'] == "true":
                        self.installed_tracks.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])

    def init_avail_arenas(self):
        self.avail_arenas = []
        if self.stk_tree != []:
            for user in self.stk_tree.xpath("/assets/arena"):
                self.avail_arenas.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

    def init_installed_arenas(self):
        self.installed_arenas = []
        if self.mytree != []:
            root = self.mytree.getroot()
            for child in root:
                        if child.tag == '{https://online.supertuxkart.net/}arena':
                            if child.attrib['installed'] == "true":
                                self.installed_arenas.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])
