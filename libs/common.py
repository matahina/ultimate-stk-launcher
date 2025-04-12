# -*- coding: utf-8 -*-

# Functions shared by both ui and gui

import glob
from pathlib import Path
import os
import tempfile
from urllib import request
import shutil
import zipfile
from configparser import ConfigParser
import pandas as pd
from lxml import etree
import xml.etree.ElementTree as ET
import ipaddress
import pycountry
import subprocess
import libs.variables

def save_config():
    with open(libs.variables.orig_directory+"/magic_config.ini", 'w') as configfile:
        libs.variables.ustkl_config.write(configfile)
    libs.variables.ustkl_config = ConfigParser()
    libs.variables.ustkl_config.read("magic_config.ini")


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
            self.stk_tree = etree.parse(libs.variables.orig_directory+"/tmp_files/online_assets.xml")
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

    def update_db(self):
        self.init_stk_tree()
        self.init_mytree()

        self.init_avail_tracks()
        self.init_installed_tracks()


        self.upd_track = []
        self.to_inst_track = []
        self.upd_arena = []
        self.to_inst_arena = []

        if self.installed_tracks != [] and self.avail_tracks != []:
            list_a = [row[0] for row in self.avail_tracks]
            list_b = [row[0] for row in self.installed_tracks]

            indexes_online = []
            indexes_offline = []
            for idx,track in enumerate(list_b):
                try:
                    indices = ([i for i, x in enumerate(list_a) if x == track])
                    maxi = 0
                    idx_online = 0
                except:
                    pass
                else:
                    for i in indices:
                        if int(self.avail_tracks[i][7])>maxi:
                            maxi = int(self.avail_tracks[i][7])
                            idx_online = i
                    if maxi > int(self.installed_tracks[idx][2]):
                        self.upd_track.append(idx_online)


            list_a = [row[0] for row in self.avail_tracks]
            list_b = [row[0] for row in self.installed_tracks]

            list_aa = [row[3] for row in self.avail_tracks]
            last_avail = max(list_aa)
            list_bb = [row[3] for row in self.installed_tracks]
            last_installed = max(list_bb)

            new_tracks = []

            if last_avail > last_installed:
                for i, stamps in enumerate(list_aa):
                    if stamps > last_installed:
                        if not(self.avail_tracks[i][0] in list_b):
                            new_elem=[i,self.avail_tracks[i][0],self.avail_tracks[i][1]]
                            if self.to_inst_track != []:
                                if self.to_inst_track[-1][1] == new_elem[1]:
                                    brrr=self.to_inst_track.pop()
                            self.to_inst_track.append(new_elem)
                self.to_inst_track=[row[0] for row in self.to_inst_track]

        self.init_avail_arenas()
        self.init_installed_arenas()

        if self.installed_arenas != [] and self.avail_arenas != []:
            list_a = [row[0] for row in self.avail_arenas]
            list_b = [row[0] for row in self.installed_arenas]

            indexes_online = []
            indexes_offline = []
            for idx,arena in enumerate(list_b):
                try:
                    indices = ([i for i, x in enumerate(list_a) if x == arena])
                    maxi = 0
                    idx_online = 0
                except:
                    pass
                else:
                    for i in indices:
                        if int(self.avail_arenas[i][7])>maxi:
                            maxi = int(self.avail_arenas[i][7])
                            idx_online = i
                    if maxi > int(self.installed_arenas[idx][2]):
                        self.upd_arena.append(idx_online)


            list_a = [row[0] for row in self.avail_arenas]
            list_b = [row[0] for row in self.installed_arenas]

            list_aa = [row[3] for row in self.avail_arenas]
            last_avail = max(list_aa)
            list_bb = [row[3] for row in self.installed_arenas]
            last_installed = max(list_bb)

            new_arenas = []

            if last_avail > last_installed:
                for i, stamps in enumerate(list_aa):
                    if stamps > last_installed:
                        if not(self.avail_arenas[i][0] in list_b):
                            new_elem=[i,self.avail_arenas[i][0],self.avail_arenas[i][1]]
                            if self.to_inst_arena != []:
                                if self.to_inst_arena[-1][1] == new_elem[1]:
                                    brrr=self.to_inst_arena.pop()
                            self.to_inst_arena.append(new_elem)
                self.to_inst_arena=[row[0] for row in self.to_inst_arena]

    def getavail_by_type(self,the_type,the_index,the_elem):
        the_answer = ""
        if the_type == "track" and self.avail_tracks != []:
            the_answer = self.avail_tracks[the_index][the_elem]
        if the_type == "arena" and self.avail_arenas != []:
            the_answer = self.avail_arenas[the_index][the_elem]
        return the_answer

class OnlineDatabase:
    def __init__(self):
        self.the_tree = []
        self.servers = []
        self.players = []
        self.total_players = 0

    def init_list(self):
        self.the_tree = []
        self.servers = []
        self.players = []
        self.total_players = 0
        try:
            self.the_tree = etree.parse(libs.variables.orig_directory+"/tmp_files/online_now.xml")
            for elem in self.the_tree.xpath("/get-all/servers/server/server-info"):
                if elem.get("current_players") != "0":
                    self.players.append([])
                    for subelem in elem.xpath("../players/player-info"):
                        line = ""
                        try:
                            rank = "(rank: " + subelem.get("rank") +")"
                        except:
                            rank = ""
                        line = line + subelem.get("username") + " " + pycountry.countries.get(alpha_2=subelem.get("country-code")).flag + " "+ rank
                        self.players[-1].append(line)
                    if self.players[-1] == []:
                        self.players.pop()
                    else:
                        if elem.get("current_ai") != "0":
                            self.players[-1].append(elem.get("current_ai")+" 🤖")
                        self.servers.append([])
                        line = ""
                        if elem.get("official") == "1":
                            line = line + "⭐ "
                        if elem.get("password") == "1":
                            line = line + "🔐 "
                        line = line + "[" + elem.get("current_players")+"/"+elem.get("max_players") + "]   "
                        line = line + elem.get("name") + " " + pycountry.countries.get(alpha_2=elem.get("country_code")).flag  + " (" + str(round(float(elem.get("distance")))) + " km) "
                        self.servers[-1].append(line)
                        line = "address: "
                        line = line + str(ipaddress.ip_address(int(elem.get("ip")))) + ":" + elem.get("port")
                        if elem.get("private_port") != elem.get("port"):
                            line = line + "["+elem.get("private_port")+"]"
                        self.servers[-1].append(line)
                        if elem.get("game_mode") == "0":
                            self.servers[-1].append("mode: Grand Prix")
                        if elem.get("game_mode") == "1":
                            self.servers[-1].append("mode: Grand Prix (time trial)")
                        if elem.get("game_mode") == "3":
                            self.servers[-1].append("mode: normal race")
                        if elem.get("game_mode") == "4":
                            self.servers[-1].append("mode: time trial")
                        if elem.get("game_mode") == "6":
                            self.servers[-1].append("mode: soccer")
                        if elem.get("game_mode") == "7":
                            self.servers[-1].append("mode: free-for-all")
                        if elem.get("game_mode") == "8":
                            self.servers[-1].append("mode: capture the flag")
                        if elem.get("difficulty") == "0":
                            self.servers[-1].append("level: beginner")
                        if elem.get("difficulty") == "1":
                            self.servers[-1].append("level: intermediate")
                        if elem.get("difficulty") == "2":
                            self.servers[-1].append("level: expert")
                        if elem.get("difficulty") == "3":
                            self.servers[-1].append("level: supertux")
                        if elem.get("game_started") != "0":
                            self.servers[-1].append(elem.get("current_track")+" ongoing")
            self.total_players = 0
            for elem in self.players:
                self.total_players = self.total_players + len(elem)
        except:
            pass



def powerup_list(version):
    stk_version = 1
    if "git2" in version:
        stk_version = 2

    onlyfiles = [f for f in os.listdir(libs.variables.orig_directory+"/tmp_files/") if os.path.isfile(os.path.join(libs.variables.orig_directory+"/tmp_files/", f))]

    pos = 0
    for elem in libs.variables.assets_data["name"]:
        if elem+".xml" in onlyfiles:
            libs.variables.assets_data.loc[pos, "downloaded"] = "Y"
        pos = pos+1

    powerups = list(set(libs.variables.assets_data["id"]))
    powerups.remove("")

    for elem in powerups:
        if "" in list(libs.variables.assets_data.where(libs.variables.assets_data["id"] == elem).dropna()["downloaded"]):
            for i in list(libs.variables.assets_data.where(libs.variables.assets_data["id"] == elem).dropna()["downloaded"].index):
                libs.variables.assets_data.loc[i, "downloaded"] = ""

    a1 = libs.variables.assets_data.where(libs.variables.assets_data["downloaded"] == "Y")
    a1 = a1.fillna("")
    a2 = a1.where(a1["stk_version"] == stk_version)
    a2 = a2.fillna("")

    p_up_list = list(dict.fromkeys(a2["id"]))
    try:
        p_up_list.remove("")
    except:
        pass

    return p_up_list

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

def starterella(profile_id,powerup_id):

    messengerella = []

    messengerella.append("## Am gonna make your dreams come true...")
    messengerella.append("# Data will be in...")

    libs.variables.data_relocation = relocate_data(libs.variables.ustkl_config.get(profile_id, 'data_path'))
    if 'svn_path' in [row[0] for row in libs.variables.ustkl_config.items(profile_id)]:
        libs.variables.assets_relocation = relocate_data(libs.variables.ustkl_config.get(profile_id, 'svn_path'))
        messengerella.append("location [assets]: "+libs.variables.assets_relocation)
    else:
        libs.variables.assets_relocation = ""
    messengerella.append("location [data]: "+libs.variables.data_relocation)
    messengerella.append("")

    messengerella.append("# Copying SFX/GFX/data files into tmp files...")
    os.chdir(libs.variables.orig_directory+"/my_files/")
    messengerella.append("chdir "+ os.path.dirname( libs.variables.orig_directory+"/my_files/" ))


    filelist = []

    path = libs.variables.orig_directory+"/my_files/"

    for root, dirs, files in os.walk(libs.variables.orig_directory+"/my_files/"):
        for file in files:
            filelist.append(os.path.join(root,file).replace(path,""))

    filelist.remove(".placeholder")

    commnds = []

    for name in filelist:
        if 'svn_path' in [row[0] for row in libs.variables.ustkl_config.items(profile_id)] and ( (name[0:name.find("/",1)].replace("/","") in libs.variables.issvn) ):
            commnds.append("rm "+libs.variables.assets_relocation+"/"+name)
            commnds.append("cp --parents "+name+" "+libs.variables.assets_relocation)
        else:
            commnds.append("rm "+libs.variables.data_relocation+"/"+name)
            commnds.append("cp --parents "+name+" "+libs.variables.data_relocation)

    for commnd in commnds:
        sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
        sw_out=sw.stdout.decode("utf-8").replace('\n','')

        messengerella.append(commnd)
        if sw_out != "":
            messengerella.append(sw_out)

    messengerella.append("")

    messengerella.append("# Using the choosen powerup file")

    p_up_file_name = list(libs.variables.assets_data['name'].where(libs.variables.assets_data['id'] == powerup_id).where(libs.variables.assets_data['type'] == "powerup").dropna())
    pfile = p_up_file_name[0]+".xml"
    kart_file_name = list(libs.variables.assets_data['name'].where(libs.variables.assets_data['id'] == powerup_id).where(libs.variables.assets_data['type'] == "kart").dropna())
    if kart_file_name == []:
        kfile="kart_characteristics_orig.xml"
    else:
        kfile = kart_file_name[0]+".xml"

    os.chdir(libs.variables.data_relocation)

    messengerella.append("chdir "+ libs.variables.data_relocation)

    commnds = ["rm powerup.xml",
               "rm kart_characteristics.xml",
               "cp "+libs.variables.orig_directory+"/tmp_files/"+pfile+" powerup.xml",
               "cp "+libs.variables.orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml"]

    for commnd in commnds:
        sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
        sw_out=sw.stdout.decode("utf-8").replace('\n','')

        messengerella.append(commnd)
        if sw_out != "":
            messengerella.append(sw_out)

    messengerella.append("## Running")
    os.chdir(os.path.dirname(libs.variables.ustkl_config.get(profile_id, 'bin_path')  ))
    messengerella.append("chdir "+ os.path.dirname( libs.variables.ustkl_config.get(profile_id, 'bin_path')  ))

    prefix = ""
    if 'svn_path' in [row[0] for row in libs.variables.ustkl_config.items(profile_id)]:
        prefix = prefix + 'export SUPERTUXKART_ASSETS_DIR="'+libs.variables.assets_relocation+'" ; '

    prefix = prefix + 'export SUPERTUXKART_DATADIR="'+libs.variables.data_relocation[:-6]+'" ; '
    if libs.variables.ustkl_config.get(profile_id, 'type') == "other":
        prefix = prefix + "export SYSTEM_LD_LIBRARY_PATH=\"$LD_LIBRARY_PATH\";export LD_LIBRARY_PATH=\"$DIRNAME/lib:$LD_LIBRARY_PATH\" ; "

    return messengerella, prefix


def enderella():
    messengerella = []
    messengerella.append("")
    messengerella.append("# Removing tmp files")
    messengerella.append("rm -R "+libs.variables.data_relocation)
    shutil.rmtree(libs.variables.data_relocation)
    if libs.variables.assets_relocation != "":
        messengerella.append("rm -R "+libs.variables.assets_relocation)
        shutil.rmtree(libs.variables.assets_relocation)
    messengerella.append("## Dooooone =D")
    libs.variables.assets_relocation = ""
    libs.variables.data_relocation = ""

    return messengerella


def dl_file(the_url,the_name, the_ext = ".xml"):
    messengerella = []
    messengerella.append("\n# "+the_name)
    try:
        Path.unlink(libs.variables.orig_directory+"/tmp_files/"+the_name+the_ext)
    except:
        pass

    try:
        request.urlretrieve(the_url, libs.variables.orig_directory+"/tmp_files/"+the_name+the_ext)
    except:
        messengerella.append("[Could not retrieve] " + the_url)
    else:
        messengerella.append("[OK] " + the_url)
    return messengerella



def update_online_database():
    messengerella = []
    messengerella.append("## Checking who's online")

    messengerella = messengerella + dl_file("https://online.supertuxkart.net/api/v2/server/get-all","online_now")

    libs.variables.online_db.init_list()

    return messengerella



def update_addon_database():
    messengerella = []
    messengerella.append("## Checking for addons")

    messengerella = messengerella + dl_file("https://online.supertuxkart.net/downloads/xml/online_assets.xml","online_assets")

    libs.variables.addon_lib.update_db()

    return messengerella



def get_addon(the_index,the_type,the_method):
    messengerella = []
    messengerella = messengerella + dl_file(libs.variables.addon_lib.getavail_by_type(the_type,the_index,2),libs.variables.addon_lib.getavail_by_type(the_type,the_index,0),".zip")
    if not any(["[Could not retrieve]" in element for element in messengerella]):
        try:
            if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)):
                shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))
        except:
            messengerella.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))
        else:
            messengerella.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))
            try:
                zip_ref = zipfile.ZipFile(libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)+".zip","r")
            except:
                messengerella.append("Error can't open zip file!")
            else:
                try:
                    os.makedirs(libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0), exist_ok=True)
                except:
                    messengerella.append("Error can't create target dir!")
                else:
                    messengerella.append("Will extract in "+libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))
                    try:
                        zip_ref.extractall(libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))
                    except:
                        messengerella.append("Error can't extract zip!")
                    else:
                        try:
                            brrr=shutil.move(libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0), os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                        except:
                            messengerella.append("Error in mv "+libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                        else:
                            messengerella.append("Done mv "+libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                            try:
                                Path.unlink(libs.variables.orig_directory+"/tmp_files/"+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)+".zip")
                            except:
                                messengerella.append("Error removing temporary zip file")
                            else:
                                messengerella.append("Success updating "+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))
                                try:
                                    replacement = '<'+the_type+' name="'+parser_of_the_year(libs.variables.addon_lib.getavail_by_type(the_type,the_index,1))+'" id="'+parser_of_the_year(libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))+'" designer="'+parser_of_the_year(libs.variables.addon_lib.getavail_by_type(the_type,the_index,5))+'" date="'+parser_of_the_year(libs.variables.addon_lib.getavail_by_type(the_type,the_index,3))+'" installed="true" installed-revision="'+parser_of_the_year(libs.variables.addon_lib.getavail_by_type(the_type,the_index,7))+'" size="'+parser_of_the_year(libs.variables.addon_lib.getavail_by_type(the_type,the_index,8))+'"/>\n'
                                    #open file1 in reading mode
                                    file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                    #open file2 in writing mode
                                    file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')

                                    if the_method == "install":
                                        #read from file1 and write to file2
                                        for line in file1:
                                            if "</addons>" in line:
                                                file2.write(replacement)
                                            file2.write(line)
                                    else: #update
                                        #read from file1 and write to file2
                                        for line in file1:
                                            if the_type in line and libs.variables.addon_lib.getavail_by_type(the_type,the_index,0) in line:
                                                file2.write(replacement)
                                            else:
                                                file2.write(line)
                                    #close file1 and file2
                                    file1.close()
                                    file2.close()
                                    Path.unlink(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                    shutil.move(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2', os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                except:
                                    messengerella.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                else:
                                    messengerella.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')

    return messengerella

def break_line(long_string,cut_length):
    trigger_a = False
    trigger_b = False
    if len(long_string)>cut_length:
        while not trigger_b:
            if not trigger_a:
                pos = long_string.find(" ", cut_length)
                long_string = long_string[0:pos]+"\n"+long_string[pos+1:]
                trigger_a=True
            else:
                pos = long_string.rfind("\n")
                if len(long_string)-pos > cut_length:
                    pos2 = long_string.find(" ", pos+cut_length)
                    long_string = long_string[0:pos2]+"\n"+long_string[pos2+1:]
                else:
                    trigger_b=True
    return long_string

def quantity(number, action):
    if number == 0:
        result = "No addon to "+action
    else:
        result = str(number)+" addon to "+action
    if action == "install":
        result = result.replace("addon","new addon")
    if number>1:
        result = result.replace("addon","addons")
    return result+" "

def parser_of_the_year(my_string):
    not_illegal='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_,".@()[]{{|}}*+'
    new_good_string = ""
    for char in my_string:
        if char in not_illegal:
            new_good_string+=char
        else:
            new_good_string+="&#x"+hex(ord((char)))[2:].upper()+";"
    return new_good_string
