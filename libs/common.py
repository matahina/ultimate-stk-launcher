# -*- coding: utf-8 -*-

import glob
from pathlib import Path
import os
import tempfile
from urllib import request
import libs.settings
import shutil
import zipfile
import libs.helpers

import subprocess

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

    dalog = []

    dalog.append("## Am gonna make your dreams come true...")
    dalog.append("# Data will be in...")

    libs.settings.data_relocation = libs.common.relocate_data(libs.settings.ustkl_config.get(profile_id, 'data_path'))
    if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_id)]:
        libs.settings.assets_relocation = libs.common.relocate_data(libs.settings.ustkl_config.get(profile_id, 'svn_path'))
        dalog.append("location [assets]: "+libs.settings.assets_relocation)
    dalog.append("location [data]: "+libs.settings.data_relocation)
    dalog.append("")

    dalog.append("# Copying SFX/GFX/data files into tmp files...")
    os.chdir(libs.settings.orig_directory+"/my_files/")
    dalog.append("chdir "+ os.path.dirname( libs.settings.orig_directory+"/my_files/" ))


    filelist = []

    path = libs.settings.orig_directory+"/my_files/"

    for root, dirs, files in os.walk(libs.settings.orig_directory+"/my_files/"):
        for file in files:
            filelist.append(os.path.join(root,file).replace(path,""))

    filelist.remove(".placeholder")

    commnds = []

    for name in filelist:
        if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_id)] and ( (name[0:name.find("/",1)].replace("/","") in issvn) ):
            commnds.append("rm "+libs.settings.assets_relocation+"/"+name)
            commnds.append("cp --parents "+name+" "+libs.settings.assets_relocation)
        else:
            commnds.append("rm "+libs.settings.data_relocation+"/"+name)
            commnds.append("cp --parents "+name+" "+libs.settings.data_relocation)

    for commnd in commnds:
        sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
        sw_out=sw.stdout.decode("utf-8").replace('\n','')

        dalog.append(commnd)
        if sw_out != "":
            dalog.append(sw_out)

    dalog.append("")

    dalog.append("# Using the choosen powerup file")

    p_up_file_name = list(libs.settings.assets_data['name'].where(libs.settings.assets_data['id'] == powerup_id).where(libs.settings.assets_data['type'] == "powerup").dropna())
    pfile = p_up_file_name[0]+".xml"
    kart_file_name = list(libs.settings.assets_data['name'].where(libs.settings.assets_data['id'] == powerup_id).where(libs.settings.assets_data['type'] == "kart").dropna())
    if kart_file_name == []:
        kfile="kart_characteristics_orig.xml"
    else:
        kfile = kart_file_name[0]+".xml"

    os.chdir(libs.settings.data_relocation)

    dalog.append("chdir "+ libs.settings.data_relocation)

    commnds = ["rm powerup.xml",
               "rm kart_characteristics.xml",
               "cp "+libs.settings.orig_directory+"/tmp_files/"+pfile+" powerup.xml",
               "cp "+libs.settings.orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml"]

    for commnd in commnds:
        sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
        sw_out=sw.stdout.decode("utf-8").replace('\n','')

        dalog.append(commnd)
        if sw_out != "":
            dalog.append(sw_out)

    dalog.append("## Running")
    os.chdir(os.path.dirname(libs.settings.ustkl_config.get(profile_id, 'bin_path')  ))
    dalog.append("chdir "+ os.path.dirname( libs.settings.ustkl_config.get(profile_id, 'bin_path')  ))

    prefix = ""
    if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_id)]:
        prefix = prefix + 'export SUPERTUXKART_ASSETS_DIR="'+libs.settings.assets_relocation+'" ; '

    prefix = prefix + 'export SUPERTUXKART_DATADIR="'+libs.settings.data_relocation[:-6]+'" ; '
    if libs.settings.ustkl_config.get(profile_id, 'type') == "other":
        prefix = prefix + "export SYSTEM_LD_LIBRARY_PATH=\"$LD_LIBRARY_PATH\";export LD_LIBRARY_PATH=\"$DIRNAME/lib:$LD_LIBRARY_PATH\" ; "

    return dalog, prefix

def dl_file(the_url,the_name):
    the_answer = []
    the_answer.append("\n# "+the_name)
    try:
        request.urlretrieve(the_url, libs.settings.orig_directory+"/tmp_files/"+the_name+".xml")
    except:
        the_answer.append("[Could not retrieve] " + the_url)
    else:
        the_answer.append("[OK] " + the_url)
    return the_answer


def update_addon_database():
    uplog = []
    uplog.append("## Checking for addons")
    uplog.append("Download list in "+libs.settings.orig_directory+"/tmp_files/")
    the_url = "https://online.supertuxkart.net/downloads/xml/online_assets.xml"
    try:
        request.urlretrieve(the_url, libs.settings.orig_directory+"/tmp_files/online_assets.xml")
    except:
        uplog.append("[Could not retrieve] " + the_url + "\n")
    else:
        uplog.append("[OK] " + the_url + "\n")

        libs.settings.addon_lib.init_stk_tree()
        libs.settings.addon_lib.init_mytree()

        libs.settings.addon_lib.init_avail_tracks()
        libs.settings.addon_lib.init_installed_tracks()


        libs.settings.addon_lib.upd_track = []
        libs.settings.addon_lib.to_inst_track = []
        libs.settings.addon_lib.upd_arena = []
        libs.settings.addon_lib.to_inst_arena = []

        if libs.settings.addon_lib.installed_tracks != []:
            list_a = [row[0] for row in libs.settings.addon_lib.avail_tracks]
            list_b = [row[0] for row in libs.settings.addon_lib.installed_tracks]

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
                        if int(libs.settings.addon_lib.avail_tracks[i][7])>maxi:
                            maxi = int(libs.settings.addon_lib.avail_tracks[i][7])
                            idx_online = i
                    if maxi > int(libs.settings.addon_lib.installed_tracks[idx][2]):
                        libs.settings.addon_lib.upd_track.append(idx_online)


            list_a = [row[0] for row in libs.settings.addon_lib.avail_tracks]
            list_b = [row[0] for row in libs.settings.addon_lib.installed_tracks]

            list_aa = [row[3] for row in libs.settings.addon_lib.avail_tracks]
            last_avail = max(list_aa)
            list_bb = [row[3] for row in libs.settings.addon_lib.installed_tracks]
            last_installed = max(list_bb)

            new_tracks = []

            if last_avail > last_installed:
                for i, stamps in enumerate(list_aa):
                    if stamps > last_installed:
                        if not(libs.settings.addon_lib.avail_tracks[i][0] in list_b):
                            new_elem=[i,libs.settings.addon_lib.avail_tracks[i][0],libs.settings.addon_lib.avail_tracks[i][1]]
                            if libs.settings.addon_lib.to_inst_track != []:
                                if libs.settings.addon_lib.to_inst_track[-1][1] == new_elem[1]:
                                    brrr=libs.settings.addon_lib.to_inst_track.pop()
                            libs.settings.addon_lib.to_inst_track.append(new_elem)
                libs.settings.addon_lib.to_inst_track=[row[0] for row in libs.settings.addon_lib.to_inst_track]

        libs.settings.addon_lib.init_avail_arenas()
        libs.settings.addon_lib.init_installed_arenas()

        if libs.settings.addon_lib.installed_arenas != []:
            list_a = [row[0] for row in libs.settings.addon_lib.avail_arenas]
            list_b = [row[0] for row in libs.settings.addon_lib.installed_arenas]

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
                        if int(libs.settings.addon_lib.avail_arenas[i][7])>maxi:
                            maxi = int(libs.settings.addon_lib.avail_arenas[i][7])
                            idx_online = i
                    if maxi > int(libs.settings.addon_lib.installed_arenas[idx][2]):
                        libs.settings.addon_lib.upd_arena.append(idx_online)


            list_a = [row[0] for row in libs.settings.addon_lib.avail_arenas]
            list_b = [row[0] for row in libs.settings.addon_lib.installed_arenas]

            list_aa = [row[3] for row in libs.settings.addon_lib.avail_arenas]
            last_avail = max(list_aa)
            list_bb = [row[3] for row in libs.settings.addon_lib.installed_arenas]
            last_installed = max(list_bb)

            new_arenas = []

            if last_avail > last_installed:
                for i, stamps in enumerate(list_aa):
                    if stamps > last_installed:
                        if not(libs.settings.addon_lib.avail_arenas[i][0] in list_b):
                            new_elem=[i,libs.settings.addon_lib.avail_arenas[i][0],libs.settings.addon_lib.avail_arenas[i][1]]
                            if libs.settings.addon_lib.to_inst_arena != []:
                                if libs.settings.addon_lib.to_inst_arena[-1][1] == new_elem[1]:
                                    brrr=libs.settings.addon_lib.to_inst_arena.pop()
                            libs.settings.addon_lib.to_inst_arena.append(new_elem)
                libs.settings.addon_lib.to_inst_arena=[row[0] for row in libs.settings.addon_lib.to_inst_arena]

    return uplog

def get_addon(the_index,the_type,the_method):
    getlog = []
    if the_type == "track":
        getlog.append("\n# "+libs.settings.addon_lib.avail_tracks[the_index][0])
        try:
            request.urlretrieve(libs.settings.addon_lib.avail_tracks[the_index][2], libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][3]+".zip")
        except:
            getlog.append("[Could not retrieve] " + libs.settings.addon_lib.avail_tracks[the_index][2])
        else:
            getlog.append("[OK] " + libs.settings.addon_lib.avail_tracks[the_index][2])
            try:
                if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[the_index][0]):
                    shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[the_index][0])
            except:
                getlog.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[the_index][0])
            else:
                getlog.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[the_index][0])
                try:
                    zip_ref = zipfile.ZipFile(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][3]+".zip","r")
                except:
                    getlog.append("Error can't open zip file!")
                else:
                    try:
                        os.makedirs(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][0], exist_ok=True)
                    except:
                        getlog.append("Error can't create target dir!")
                    else:
                        getlog.append("Will extract in "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][0])
                        try:
                            zip_ref.extractall(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][0])
                        except:
                            getlog.append("Error can't extract zip!")
                        else:
                            try:
                                brrr=shutil.move(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][0], os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                            except:
                                getlog.append("Error in mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                            else:
                                getlog.append("Done mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                try:
                                    os.remove(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[the_index][3]+".zip")
                                except:
                                    getlog.append("Error removing temporary zip file")
                                else:
                                    getlog.append("Success updating "+libs.settings.addon_lib.avail_tracks[the_index][0])
                                    try:
                                        if the_method == "install":
                                            replacement = '<track name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][3])+'" installed="true" installed-revision="'+libs.helpers.settings.orig_directorypers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][8])+'"/>\n'
                                            #open file1 in reading mode
                                            file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                            #open file2 in writing mode
                                            file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                            #read from file1 and write to file2
                                            for line in file1:
                                                if "</addons>" in line:
                                                    file2.write(replacement)
                                                file2.write(line)
                                        else: #update
                                            replacement = '<track name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[the_index][8])+'"/>\n'
                                            #open file1 in reading mode
                                            file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                            #open file2 in writing mode
                                            file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                            #read from file1 and write to file2
                                            for line in file1:
                                                if "track" in line and libs.settings.addon_lib.avail_tracks[the_index][0] in line:
                                                    file2.write(replacement)
                                                else:
                                                    file2.write(line)
                                        #close file1 and file2
                                        file1.close()
                                        file2.close()
                                        os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                        os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                    except:
                                        getlog.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                    else:
                                        getlog.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')

    elif the_type == "arena":
        getlog.append("\n# "+libs.settings.addon_lib.avail_arenas[the_index][0])
        try:
            request.urlretrieve(libs.settings.addon_lib.avail_arenas[the_index][2], libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][3]+".zip")
        except:
            getlog.append("[Could not retrieve] " + libs.settings.addon_lib.avail_arenas[the_index][2])
        else:
            getlog.append("[OK] " + libs.settings.addon_lib.avail_arenas[the_index][2])
            try:
                if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[the_index][0]):
                    shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[the_index][0])
            except:
                getlog.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[the_index][0])
            else:
                getlog.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[the_index][0])
                try:
                    zip_ref = zipfile.ZipFile(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][3]+".zip","r")
                except:
                    getlog.append("Error can't open zip file!")
                else:
                    try:
                        os.makedirs(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][0], exist_ok=True)
                    except:
                        getlog.append("Error can't create target dir!")
                    else:
                        getlog.append("Will extract in "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][0])
                        try:
                            zip_ref.extractall(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][0])
                        except:
                            getlog.append("Error can't extract zip!")
                        else:
                            try:
                                brrr=shutil.move(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][0], os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                            except:
                                getlog.append("Error in mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                            else:
                                getlog.append("Done mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                try:
                                    os.remove(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[the_index][3]+".zip")
                                except:
                                    getlog.append("Error removing temporary zip file")
                                else:
                                    getlog.append("Success updating "+libs.settings.addon_lib.avail_arenas[the_index][0])
                                    try:
                                        if the_method == "install":
                                            replacement = '<arena name="'+libs.helpers.parser_of_the_year(lthe_indexibs.settings.addon_lib.avail_arenas[the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][8])+'"/>\n'
                                            #open file1 in reading mode
                                            file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                            #open file2 in writing mode
                                            file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                            #read from file1 and write to file2
                                            for line in file1:
                                                if "</addons>" in line:
                                                    file2.write(replacement)
                                                file2.write(line)
                                        else: #update
                                            replacement = '<arena name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[the_index][8])+'"/>'
                                            #open file1 in reading mode
                                            file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                            #open file2 in writing mode
                                            file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                            #read from file1 and write to file2
                                            for line in file1:
                                                if "arena" in line and libs.settings.addon_lib.avail_arenas[the_index][0] in line:
                                                    file2.write(replacement)
                                                else:
                                                    file2.write(line)
                                        #close file1 and file2
                                        file1.close()
                                        file2.close()
                                        os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                        os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                    except:
                                        getlog.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                    else:
                                        getlog.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')

    return getlog
