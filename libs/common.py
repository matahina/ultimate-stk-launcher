# -*- coding: utf-8 -*-

# Functions shared by both ui and gui

import glob
from pathlib import Path
from os import environ as envvar
import tempfile
from urllib import request
import shutil
import zipfile
from configparser import ConfigParser
from lxml import etree
import ipaddress
import pycountry
import subprocess
import libs.variables
import libs.helpers_xml

def save_config():
    with open(pathery(["magic_config.ini"]), 'w') as configfile:
        libs.variables.ustkl_config.write(configfile)
    libs.variables.ustkl_config = ConfigParser()
    libs.variables.ustkl_config.read(pathery(["magic_config.ini"]))


class AddonLibrary:
    def __init__(self):
        self.mytree = []
        self.stk_tree = []
        self.upd_track = []
        self.to_inst_track = []
        self.upd_kart = []
        self.to_inst_kart = []
        self.upd_arena = []
        self.to_inst_arena = []
        self.avail_tracks = []
        self.installed_tracks = []
        self.avail_karts = []
        self.installed_karts = []
        self.avail_arenas = []
        self.installed_arenas = []

    def init_mytree(self):
        try:
            self.mytree = etree.parse(pathery(['~','.local','share','supertuxkart','addons','addons_installed.xml'],False))
        except Exception:
            libs.variables.mylog.exception("Error reading installed addons XML")
            self.mytree = []

    def init_stk_tree(self):
        try:
            self.stk_tree = etree.parse(pathery(["assets","online_assets.xml"]), parser=etree.XMLParser(resolve_entities=False,no_network=True))
        except Exception:
            libs.variables.mylog.exception("Error reading online addons XML")
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

    def init_avail_karts(self):
        self.avail_karts = []
        if self.stk_tree != []:
            for user in self.stk_tree.xpath("/assets/kart"):
                self.avail_karts.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

    def init_installed_karts(self):
        self.installed_karts = []
        if self.mytree != []:
            root = self.mytree.getroot()
            for child in root:
                if child.tag == '{https://online.supertuxkart.net/}kart':
                    if child.attrib['installed'] == "true":
                        self.installed_karts.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])

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

    def update_db(self, the_filter=True):
        self.init_stk_tree()

        with libs.helpers_xml.xml_lock:
            self.init_mytree()
            self.init_installed_tracks()
            self.init_installed_arenas()
            self.init_installed_karts()

        self.upd_track = []
        self.to_inst_track = []
        self.upd_arena = []
        self.to_inst_arena = []
        self.upd_kart = []
        self.to_inst_kart = []

        self.init_avail_tracks()

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
                except Exception:
                    libs.variables.mylog.exception("Error selecting track revision")
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

            if not(the_filter):
                last_installed = "0"

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
                except Exception:
                    libs.variables.mylog.exception("Error selecting arena revision")
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

            if not(the_filter):
                last_installed = "0"

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

        self.init_avail_karts()

        if self.installed_karts != [] and self.avail_karts != []:
            list_a = [row[0] for row in self.avail_karts]
            list_b = [row[0] for row in self.installed_karts]

            indexes_online = []
            indexes_offline = []
            for idx,kart in enumerate(list_b):
                try:
                    indices = ([i for i, x in enumerate(list_a) if x == kart])
                    maxi = 0
                    idx_online = 0
                except Exception:
                    libs.variables.mylog.exception("Error selecting kart revision")
                    pass
                else:
                    for i in indices:
                        if int(self.avail_karts[i][7])>maxi:
                            maxi = int(self.avail_karts[i][7])
                            idx_online = i
                    if maxi > int(self.installed_karts[idx][2]):
                        self.upd_kart.append(idx_online)


            list_a = [row[0] for row in self.avail_karts]
            list_b = [row[0] for row in self.installed_karts]

            list_aa = [row[3] for row in self.avail_karts]
            last_avail = max(list_aa)
            list_bb = [row[3] for row in self.installed_karts]
            last_installed = max(list_bb)

            new_karts = []

            if not(the_filter):
                last_installed = "0"

            if last_avail > last_installed:
                for i, stamps in enumerate(list_aa):
                    if stamps > last_installed:
                        if not(self.avail_karts[i][0] in list_b):
                            new_elem=[i,self.avail_karts[i][0],self.avail_karts[i][1]]
                            if self.to_inst_kart != []:
                                if self.to_inst_kart[-1][1] == new_elem[1]:
                                    brrr=self.to_inst_kart.pop()
                            self.to_inst_kart.append(new_elem)
                self.to_inst_kart=[row[0] for row in self.to_inst_kart]

    def getavail_by_type(self,the_type,the_index,the_elem):
        the_answer = ""
        if the_type == "track" and self.avail_tracks != []:
            the_answer = self.avail_tracks[the_index][the_elem]
        if the_type == "arena" and self.avail_arenas != []:
            the_answer = self.avail_arenas[the_index][the_elem]
        if the_type == "kart" and self.avail_karts != []:
            the_answer = self.avail_karts[the_index][the_elem]
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
            self.the_tree = etree.parse(pathery(["assets","online_now.xml"]), parser=etree.XMLParser(resolve_entities=False,no_network=True))
            for elem in self.the_tree.xpath("/get-all/servers/server/server-info"):
                if elem.get("current_players") != "0":
                    self.players.append([])
                    for subelem in elem.xpath("../players/player-info"):
                        line = ""
                        try:
                            rank = "(rank: " + subelem.get("rank") +")"
                        except Exception:
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
        except Exception:
            libs.variables.mylog.exception("Error reading online server database")
            pass

def scanerella(the_path,go_depth=True,only_dirs=False):
    scan_list = []
    for entry in Path(the_path).iterdir():
        if not(not(entry.is_dir()) and only_dirs):
            scan_list.append(str(entry))
        if entry.is_dir() and go_depth:
            if not ".svn" in str(entry) and not ".git" in str(entry):
                second_list = scanerella(str(entry))
                scan_list = scan_list + second_list
    return scan_list

def copyrella(data_source, new_place = "", is_data = False):
    if new_place == "":
        new_place = tempfile.mkdtemp(prefix="ustkl-")
        if is_data:
            Path(new_place,"data").mkdir(parents=True, exist_ok=True)
            new_place = pathery([new_place,"data"])
    prefix = "/".join(data_source[0].split("/")[:-1])
    for elem in data_source:
        if Path(elem).is_dir():
            Path(new_place+elem.replace(prefix,"")).mkdir(parents=True, exist_ok=True)
        else:
            # Path(new_place+elem.replace(prefix,"")).symlink_to(Path(elem))
            shutil.copyfile(Path(elem), Path(new_place+elem.replace(prefix,"")))

    return new_place

def starterella(profile_id,pupkart_list):

    messengerella = []

    messengerella.append("## Am gonna make your dreams come true...")
    messengerella.append("# Data will be in...")

    libs.variables.data_relocation = copyrella(scanerella(libs.variables.ustkl_config.get(profile_id, 'data_path')),is_data=True)

    if 'assets_path' in [row[0] for row in libs.variables.ustkl_config.items(profile_id)]:
        libs.variables.assets_relocation = copyrella(scanerella(libs.variables.ustkl_config.get(profile_id, 'assets_path')))
        messengerella.append("location [assets]: "+libs.variables.assets_relocation)
    else:
        libs.variables.assets_relocation = ""
    messengerella.append("location [data]: "+libs.variables.data_relocation)
    messengerella.append("")



    messengerella.append("# Copying SFX/GFX/data files into tmp files...")
    customfiles_list = scanerella(Path(libs.variables.orig_directory,"my_files"))
    customfiles_list_assets = []
    if 'assets_path' in [row[0] for row in libs.variables.ustkl_config.items(profile_id)]:
        for elem in customfiles_list:
            for subelem in elem.split("/"):
                if subelem in libs.variables.is_asset:
                    customfiles_list_assets.append(elem)
    customfiles_list_data = [x for x in customfiles_list if x not in customfiles_list_assets]

    copyrella(customfiles_list_data,libs.variables.data_relocation)
    if customfiles_list_assets != []:
        copyrella(customfiles_list_assets,libs.variables.assets_relocation)

    if pupkart_list != []:
        messengerella.append("")

        messengerella.append("# Using the choosen powerup file")

        pfile = pupkart_list[0]
        kfile = pupkart_list[1]

        file_list = []
        file_list.append(pathery(["assets",pfile+".xml"]))
        file_list.append(pathery(["assets",kfile+".xml"]))

        copyrella(file_list,libs.variables.data_relocation)

        shutil.move(Path(libs.variables.data_relocation,pfile+".xml"),
                    Path(libs.variables.data_relocation,"powerup.xml"))
        shutil.move(Path(libs.variables.data_relocation,kfile+".xml"),
                    Path(libs.variables.data_relocation,"kart_characteristics.xml"))

    messengerella.append("## Running")

    prefix = ""
    if 'assets_path' in [row[0] for row in libs.variables.ustkl_config.items(profile_id)]:
        envvar['SUPERTUXKART_ASSETS_DIR']=libs.variables.assets_relocation

    envvar['SUPERTUXKART_DATADIR']="/".join(pathery([libs.variables.data_relocation]).split("/")[:-1])

    if "stable" in libs.variables.ustkl_config.get(profile_id, 'type'):
        envvar['SYSTEM_LD_LIBRARY_PATH']=libs.variables.assets_relocation
        envvar['LD_LIBRARY_PATH']=pathery(["/".join(libs.variables.ustkl_config.get(profile_id, 'bin_path').split("/")[:-2]),"lib"],False)
    else:
        envvar['SYSTEM_LD_LIBRARY_PATH']=""
        envvar['LD_LIBRARY_PATH']=""

    return messengerella


def enderella():
    messengerella = []
    messengerella.append("")
    messengerella.append("# Removing tmp files")

    folders = []

    if libs.variables.data_relocation != "":
        folders.append(Path(libs.variables.data_relocation).parent)

    if libs.variables.assets_relocation != "":
        folders.append(Path(libs.variables.assets_relocation))

    for folder in folders:
        if folder.parent.resolve() == Path(tempfile.gettempdir()).resolve() and folder.name.startswith("ustkl-") and not folder.is_symlink():
            messengerella.append("rm -R "+str(folder))
            shutil.rmtree(folder)
        else:
            messengerella.append("Error: unsafe directory "+str(folder))

    messengerella.append("## Dooooone =D")
    libs.variables.assets_relocation = ""
    libs.variables.data_relocation = ""

    return messengerella

def dl_file(the_url,the_name, the_ext = ".xml",the_dir = ""):
    messengerella = []
    messengerella.append("\n# "+the_name)

    destination = Path(pathery(["assets",the_dir,the_name+the_ext]))

    try:
        with tempfile.TemporaryDirectory(dir=destination.parent) as tmp_dir:
            tmp_file = Path(tmp_dir,destination.name)
            request.urlretrieve(the_url,str(tmp_file))
            tmp_file.replace(destination)
    except Exception:
        libs.variables.mylog.exception("Could not retrieve "+the_url)
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



def update_addon_database(the_filter=True):
    messengerella = []
    messengerella.append("## Checking for addons")

    messengerella = messengerella + dl_file("https://online.supertuxkart.net/dl/xml/online_assets.xml","online_assets")

    libs.variables.addon_lib.update_db(the_filter)

    return messengerella



def get_addon(the_index,the_type,the_method):
    the_word = "updating"
    the_place = "tracks"
    if the_method == "install":
        the_word = "installing"
    if the_type == "kart":
        the_place = "karts"

    messengerella = []

    addon_id = libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)

    # Avoid bad path that might turn later in rm -rf / or rm -rf /$HOME
    if not addon_id or addon_id in [".", ".."] or "/" in addon_id or "\\" in addon_id:
        messengerella.append("Error: invalid addon ID")
        return messengerella
    messengerella = messengerella + dl_file(libs.variables.addon_lib.getavail_by_type(the_type,the_index,2),libs.variables.addon_lib.getavail_by_type(the_type,the_index,0),".zip","tmp_files")
    if not any(["[Could not retrieve]" in element for element in messengerella]):
        try:
            zip_ref = zipfile.ZipFile(pathery(["assets","tmp_files",libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)+".zip"]),"r")
        except Exception:
            libs.variables.mylog.exception("Error opening addon ZIP "+addon_id)
            messengerella.append("Error can't open zip file!")
        else:
            try:
                tmp_dir = Path(libs.variables.orig_directory,"assets","tmp_files",addon_id)
                if tmp_dir.is_dir():
                    shutil.rmtree(tmp_dir)
                tmp_dir.mkdir(parents=True, exist_ok=False)
            except Exception:
                libs.variables.mylog.exception("Error creating temporary addon directory "+addon_id)
                messengerella.append("Error can't create target dir!")
            else:
                messengerella.append("Will extract in "+
                                     pathery(["assets","tmp_files",libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)]))
                try:
                    zip_ref.extractall(pathery(["assets","tmp_files",libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)]))
                    # check if zip is valid addon pack!
                    if not Path(tmp_dir,"kart.xml" if the_type == "kart" else "track.xml").is_file():
                        raise ValueError("Missing addon definition")
                except Exception:
                    libs.variables.mylog.exception("Error extracting addon ZIP "+addon_id)
                    messengerella.append("Error can't extract zip!")
                else:
                    installed_dir = Path('~','.local','share','supertuxkart','addons',the_place,addon_id).expanduser()
                    backup_dir = installed_dir.with_name(addon_id+".ustkl-backup")

                    try:
                        if backup_dir.exists() or backup_dir.is_symlink():
                            raise FileExistsError(str(backup_dir))

                        if installed_dir.is_symlink():
                            raise ValueError("Unexpected symlink")

                        if installed_dir.is_dir():
                            installed_dir.rename(backup_dir)
                            messengerella.append("Backup created "+str(backup_dir))
                    except Exception:
                        libs.variables.mylog.exception("Error backing up "+str(installed_dir))
                        messengerella.append("Error backing up "+str(installed_dir))
                    else:
                        try:
                            tmp_dir.rename(installed_dir)
                        except Exception:
                            libs.variables.mylog.exception("Error moving "+str(tmp_dir)+" to "+str(installed_dir))
                            messengerella.append("Error in mv "+str(tmp_dir)+" "+str(installed_dir))
                            try:
                                if backup_dir.is_dir():
                                    backup_dir.rename(installed_dir)
                                    messengerella.append("Backup restored "+str(installed_dir))
                            except Exception:
                                libs.variables.mylog.exception("Error restoring "+str(backup_dir))
                                messengerella.append("Error restoring "+str(backup_dir))
                        else:
                            messengerella.append("Done mv "+str(tmp_dir)+" "+str(installed_dir))

                            try:
                                if backup_dir.is_dir():
                                    shutil.rmtree(backup_dir)
                            except Exception:
                                libs.variables.mylog.exception("Error removing "+str(backup_dir))
                                messengerella.append("Error removing "+str(backup_dir))

                            try:
                                Path.unlink(pathery(["assets","tmp_files",libs.variables.addon_lib.getavail_by_type(the_type,the_index,0)+".zip"]))
                            except Exception:
                                libs.variables.mylog.exception("Error removing temporary ZIP "+addon_id)
                                messengerella.append("Error removing temporary zip file")
                            else:
                                messengerella.append("Success "+the_word+" "+libs.variables.addon_lib.getavail_by_type(the_type,the_index,0))

                                xml_path = pathery(['~', '.local', 'share', 'supertuxkart', 'addons', 'addons_installed.xml'], False)

                                try:
                                    attributes = {
                                        "id": libs.variables.addon_lib.getavail_by_type(the_type,the_index,0),
                                        "name": libs.variables.addon_lib.getavail_by_type(the_type,the_index,1),
                                        "designer": libs.variables.addon_lib.getavail_by_type(the_type,the_index,5) or "",
                                        "date": libs.variables.addon_lib.getavail_by_type(the_type,the_index,3),
                                        "installed": "true",
                                        "installed-revision": libs.variables.addon_lib.getavail_by_type(the_type,the_index,7),
                                        "size": libs.variables.addon_lib.getavail_by_type(the_type,the_index,8)
                                    }
                                    with libs.helpers_xml.xml_lock:
                                        libs.variables.addon_lib.init_mytree()
                                        tree = libs.variables.addon_lib.mytree

                                        if tree == []:
                                            raise ValueError("Could not read installed addons")

                                        libs.helpers_xml.update_installed_addon(xml_path, the_type, attributes, tree)

                                except Exception:
                                    libs.variables.mylog.exception("Error updating "+xml_path)
                                    messengerella.append("Error updating " + xml_path)

                                else:
                                    messengerella.append("Success updating " + xml_path)


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

def pathery(the_args,start_from_there=True):
    if start_from_there:
        return str(Path(libs.variables.orig_directory,*the_args).expanduser())
    else:
        return str(Path(*the_args).expanduser())


def cleanup_addons():
    messengerella = []

    try:
        removed, skipped = libs.helpers_xml.clean_addon_database(
            pathery(['~','.local','share','supertuxkart','addons','addons_installed.xml'],False),
            libs.variables.addon_lib.stk_tree
        )
    except Exception:
        libs.variables.mylog.exception("Error cleaning addon database")
        messengerella.append("Error cleaning addon database")
    else:
        messengerella.append("Removed "+str(removed)+" XML entries")

        for addon_id in skipped:
            messengerella.append("Skipped "+addon_id)

    return messengerella
