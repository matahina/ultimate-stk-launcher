#!/usr/bin/env python3

import subprocess
import os
import os.path
from os import path
from urllib import request
import time
from pathlib import Path
import datetime
import setproctitle
from pick import pick
from lxml import etree
import xml.etree.ElementTree as ET
from configparser import ConfigParser
import csv
import pandas as pd

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def output_title(text, level):
    if level == 1:
        print(color.PURPLE + color.BOLD + text.upper() + color.END)
    if level == 2:
        print(color.CYAN + text.upper() + color.END)

def prompt(text, important = False):
    if important:
        print(color.UNDERLINE + color.YELLOW + text + color.END)
    else:
        print(color.UNDERLINE + text + color.END)


config = ConfigParser()

orig_directory = os.getcwd()

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

assets_data = pd.read_csv('sources.csv')
assets_data = assets_data.fillna("")

def update_extra_files():
    output_title("Downloading powerup files in ",2)
    print(color.CYAN + orig_directory+"/tmp_files/" + color.END)


    for index,row in assets_data[["url","name"]].iterrows():
        print("")
        prompt(row["name"])
        try:
            request.urlretrieve(row["url"], orig_directory+"/tmp_files/"+row["name"]+".xml")
        except:
            print(color.RED + "Could not retrieve " + row["url"] + color.END)
        else:
            print("OK " + row["url"])

    print("")

def update_addons():
    output_title("Checking for addons",2)
    try:
        request.urlretrieve("https://online.supertuxkart.net/downloads/xml/online_assets.xml", orig_directory+"/tmp_files/online_assets.xml")
    except:
        print(color.RED + "Could not retrieve " + "https://online.supertuxkart.net/downloads/xml/online_assets.xml" + color.END)

    tree = etree.parse(orig_directory+"/tmp_files/online_assets.xml")

    mytree = ET.parse(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
    root = mytree.getroot()

    avail_tracks = []
    installed_tracks = []


    for user in tree.xpath("/assets/track"):
        avail_tracks.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

    for child in root:
        if child.tag == '{https://online.supertuxkart.net/}track':
            if child.attrib['installed'] == "true":
                installed_tracks.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])

    if installed_tracks != []:
        list_a = [row[0] for row in avail_tracks]
        list_b = [row[0] for row in installed_tracks]

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
                    if int(avail_tracks[i][7])>maxi:
                        maxi = int(avail_tracks[i][7])
                        idx_online = i
                if maxi > int(installed_tracks[idx][2]):
                    indexes_online.append(idx_online)
                    indexes_offline.append(idx)

        if indexes_offline != [] and indexes_online != []:
            complmt = ""
            for i in indexes_online:
                complmt = complmt + "\n" + "\n- " + avail_tracks[i][1] + " by " + avail_tracks[i][4] + " " + avail_tracks[i][5] + "\n" + "desc: " + avail_tracks[i][6] + "\n" + "size: " + str(round(int(avail_tracks[i][8])/(1024*1024),1)) + "MB"

            title = "Do you wanna update those addon tracks?"+complmt
            options = ['Yeah',
                        'Nope'
                        ]
            option, index = pick(options, title)
            prompt("Do you wanna update those addon tracks?")
            print(option)
            print("")

            if index == 0:
                for j,i in enumerate(indexes_online):
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                    os.system("rm -rf "+installed_tracks[indexes_offline[j]][0])
                    Path(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_tracks[i][0]).mkdir(parents=True, exist_ok=True)
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_tracks[i][0])
                    request.urlretrieve(avail_tracks[i][2], avail_tracks[i][3]+".zip")
                    os.system("unzip "+avail_tracks[i][3]+".zip")
                    os.system("rm "+avail_tracks[i][3]+".zip")
                    #open file1 in reading mode
                    file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')

                    #open file2 in writing mode
                    file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')

                    #read from file1 and write to file2
                    for line in file1:
                        if "track" in line:
                            if avail_tracks[i][0] in line:
                                file2.write(line.replace('installed-revision="'+installed_tracks[indexes_offline[j]][2]+'"',
                                'installed-revision="'+avail_tracks[i][7]+'"').replace('date="'+installed_tracks[indexes_offline[j]][3]+'"',
                                'date="'+avail_tracks[i][3]+'"'))
                            else:
                                file2.write(line)
                        else:
                            file2.write(line)

                    #close file1 and file2
                    file1.close()
                    file2.close()
                    os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                    os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')

        tree = etree.parse(orig_directory+"/tmp_files/online_assets.xml")

        mytree = ET.parse(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
        root = mytree.getroot()

        avail_tracks = []
        installed_tracks = []

        for user in tree.xpath("/assets/track"):
            avail_tracks.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

        for child in root:
            if child.tag == '{https://online.supertuxkart.net/}track':
                if child.attrib['installed'] == "true":
                    installed_tracks.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])

        list_a = [row[0] for row in avail_tracks]
        list_b = [row[0] for row in installed_tracks]

        list_aa = [row[3] for row in avail_tracks]
        last_avail = max(list_aa)
        list_bb = [row[3] for row in installed_tracks]
        last_installed = max(list_bb)

        new_tracks = []

        if last_avail > last_installed:
            for i, stamps in enumerate(list_aa):
                if stamps > last_installed:
                    if not(avail_tracks[i][1] in list_b):
                        new_tracks.append(i)

        if new_tracks != []:
            options = []
            for i in new_tracks:
                options.append(avail_tracks[i][1] + "  |  " + "by " + avail_tracks[i][4] + " " + avail_tracks[i][5] + "  |  " + "desc: " + avail_tracks[i][6] + "  |  " + "size: " + str(round(int(avail_tracks[i][8])/(1024*1024),1)) + "MB"+ "\n")

            title = "Maybe you wanna install those new addon tracks since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
            selected = pick(options, title, multiselect=True)
            prompt("Maybe you wanna install those new addon tracks since last time?")
            print(selected)
            print("")

            if selected != []:
                sel_tracks = []
                for i in [row[1] for row in selected]:
                    sel_tracks.append(new_tracks[i])
                for j,i in enumerate(sel_tracks):
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                    os.system("rm -rf "+avail_tracks[i][0])
                    Path(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_tracks[i][0]).mkdir(parents=True, exist_ok=True)
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_tracks[i][0])
                    request.urlretrieve(avail_tracks[i][2], avail_tracks[i][3]+".zip")
                    os.system("unzip "+avail_tracks[i][3]+".zip")
                    os.system("rm "+avail_tracks[i][3]+".zip")


    tree = etree.parse(orig_directory+"/tmp_files/online_assets.xml")

    mytree = ET.parse(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
    root = mytree.getroot()

    avail_arenas = []
    installed_arenas = []

    for user in tree.xpath("/assets/arena"):
        avail_arenas.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

    for child in root:
        if child.tag == '{https://online.supertuxkart.net/}arena':
            if child.attrib['installed'] == "true":
                installed_arenas.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])

    if installed_arenas != []:
        list_a = [row[0] for row in avail_arenas]
        list_b = [row[0] for row in installed_arenas]

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
                    if int(avail_arenas[i][7])>maxi:
                        maxi = int(avail_arenas[i][7])
                        idx_online = i
                if maxi > int(installed_arenas[idx][2]):
                    indexes_online.append(idx_online)
                    indexes_offline.append(idx)

        if indexes_offline != [] and indexes_online != []:
            complmt = ""
            for i in indexes_online:
                complmt = complmt + "\n" + "\n- " + avail_arenas[i][1] + " by " + avail_arenas[i][4] + " " + avail_arenas[i][5] + "\n" + "desc: " + avail_arenas[i][6] + "\n" + "size: " + str(round(int(avail_arenas[i][8])/(1024*1024),1)) + "MB"

            title = "Do you wanna update those addon arenas?"+complmt
            options = ['Yeah',
                        'Nope'
                        ]
            option, index = pick(options, title)
            prompt("Do you wanna update those addon arenas?")
            print(option)
            print("")

            if index == 0:
                for j,i in enumerate(indexes_online):
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                    os.system("rm -rf "+installed_arenas[indexes_offline[j]][0])
                    Path(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_arenas[i][0]).mkdir(parents=True, exist_ok=True)
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_arenas[i][0])
                    request.urlretrieve(avail_arenas[i][2], avail_arenas[i][3]+".zip")
                    os.system("unzip "+avail_arenas[i][3]+".zip")
                    os.system("rm "+avail_arenas[i][3]+".zip")
                    #open file1 in reading mode
                    file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')

                    #open file2 in writing mode
                    file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')

                    #read from file1 and write to file2
                    for line in file1:
                        if "track" in line:
                            if avail_arenas[i][0] in line:
                                file2.write(line.replace('installed-revision="'+installed_arenas[indexes_offline[j]][2]+'"',
                                'installed-revision="'+avail_arenas[i][7]+'"').replace('date="'+installed_arenas[indexes_offline[j]][3]+'"',
                                'date="'+avail_arenas[i][3]+'"'))
                            else:
                                file2.write(line)
                        else:
                            file2.write(line)


                    #close file1 and file2
                    file1.close()
                    file2.close()
                    os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                    os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')


        tree = etree.parse(orig_directory+"/tmp_files/online_assets.xml")

        mytree = ET.parse(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
        root = mytree.getroot()

        avail_arenas = []
        installed_arenas = []

        for user in tree.xpath("/assets/arena"):
            avail_arenas.append([user.get("id"),user.get("name"),user.get("file"),user.get("date"),user.get("uploader"),user.get("designer"),user.get("description"),user.get("revision"),user.get("size")])

        for child in root:
            if child.tag == '{https://online.supertuxkart.net/}arena':
                if child.attrib['installed'] == "true":
                    installed_arenas.append([child.attrib["id"], child.attrib["name"], child.attrib["installed-revision"],child.attrib["date"]])

        list_a = [row[0] for row in avail_arenas]
        list_b = [row[0] for row in installed_arenas]

        list_aa = [row[3] for row in avail_arenas]
        last_avail = max(list_aa)
        list_bb = [row[3] for row in installed_arenas]
        last_installed = max(list_bb)

        new_arenas = []

        if last_avail > last_installed:
            for i, stamps in enumerate(list_aa):
                if stamps > last_installed:
                    if not(avail_arenas[i][1] in list_b):
                        new_arenas.append(i)

        if new_arenas != []:
            options = []
            for i in new_arenas:
                options.append(avail_arenas[i][1] + "  |  " + "by " + avail_arenas[i][4] + " " + avail_arenas[i][5] + "  |  " + "desc: " + avail_arenas[i][6] + "  |  " + "size: " + str(round(int(avail_arenas[i][8])/(1024*1024),1)) + "MB"+ "\n")

            title = "Maybe you wanna install those new addon arenas since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
            selected = pick(options, title, multiselect=True)
            prompt("Maybe you wanna install those new addon arenas since last time?")
            print(selected)
            print("")

            if selected != []:
                sel_arenas = []
                for i in [row[1] for row in selected]:
                    sel_arenas.append(new_arenas[i])
                for j,i in enumerate(sel_arenas):
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                    os.system("rm -rf "+avail_arenas[i][0])
                    Path(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_arenas[i][0]).mkdir(parents=True, exist_ok=True)
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_arenas[i][0])
                    request.urlretrieve(avail_arenas[i][2], avail_arenas[i][3]+".zip")
                    os.system("unzip "+avail_arenas[i][3]+".zip")
                    os.system("rm "+avail_arenas[i][3]+".zip")

def edit_profile(number):
    nice_clue = config.get('Profile_'+number,'name')
    if nice_clue == 'NotThisName':

        output_title("This Profile", 2)
        print("")

        an_answer = input(color.UNDERLINE + "Pls give a name to this profile:" + color.END +" ")
        print("")
        config.set('Profile_'+number,'name',an_answer)

        prompt("Now choose the bin file for STK")
        while True:
            an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE BIN STK FILE???'], stdout=subprocess.PIPE)
            if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                break
            else:
                print(color.RED + "Pls choose a file" + color.END)
        print(an_answer.stdout.decode('utf-8').replace("\n",""))
        print("")
        config.set('Profile_'+number,'bin_path',an_answer.stdout.decode('utf-8').replace("\n",""))

        prompt("then the location of the DATA folder")
        while True:
            an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  Data  DIRECTORY???'], stdout=subprocess.PIPE)
            if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                break
            else:
                print(color.RED + "Pls choose a directory" + color.END)
        print(an_answer.stdout.decode('utf-8').replace("\n",""))
        print("")
        config.set('Profile_'+number,'data_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")


        title = "So, what kind of install is it (for this profile)?"
        options = ['distro-based (apt-get, rpm, pacman, emerge, whatever...)',
                    'from git (for the bold!)',
                    'from a tarball (so locally, no sudo required to change any file)'
                    ]
        option, index = pick(options, title)
        prompt(title)
        print(option)
        print("")

        if index == 0:
            config.set('Profile_'+number,'type',"sudo")

        elif index == 1:
            config.set('Profile_'+number,'type',"git")

            prompt("Now choose the location of the GIT folder")
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  git  DIRECTORY???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a directory" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            print("")
            config.set('Profile_'+number,'git_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")

            prompt("then of the SVN folder")
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  svn  DIRECTORY???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a directory" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            print("")
            config.set('Profile_'+number,'svn_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")

        elif index == 2:
            config.set('Profile_'+number,'type',"from_tarball")

        with open(orig_directory+"/magic_config.ini", 'w') as configfile:
            config.write(configfile)

        output_title("Profile Updated!", 2)
        print("")
        input("Press Enter to continue...")
        cls()
        #update_extra_files()


def initialize():
    output_title("Config is being created...", 1)
    print("")

    Path(orig_directory+"/tmp_files/").mkdir(parents=True, exist_ok=True)

    f = open(orig_directory+"/magic_config.ini", 'w')
    f.close()
    config.read(orig_directory+"/magic_config.ini")
    config.add_section('Profile_1')
    config.set('Profile_1','name','NotThisName')
    edit_profile("1")


def stk_update():
    title = "Which profile do you want to revert today?"
    options = config.sections()
    options.remove("General")
    idx = []
    for i,prof in enumerate(options):
        if config.get(prof, 'type') == "git":
            idx.append(i)
    if idx != []:
        plist = [options[i] for i in idx]
        names = []
        for name in plist:
            names.append(config.get(name, 'name'))
        option, index = pick(names, title)
        output_title(title, 2)
        print(option)
        print("")
        profile_answer = plist[index]

        uecho_file = "UPDATE_"+echo_file

        os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + orig_directory+"/logs/"+uecho_file+".log")
        os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
        os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
        os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")

        prompt("Updating "+profile_answer + " " + config.get(profile_answer, 'name'))

        print("Updating SVN")
        print("")
        os.chdir(config.get(profile_answer, 'svn_path'))
        os.system("svn up >>" + orig_directory+"/logs/"+uecho_file+".log")

        print("Updating GIT")
        print("")
        os.chdir(config.get(profile_answer, 'git_path'))
        os.system("git pull >>" + orig_directory+"/logs/"+uecho_file+".log")

        print("Building GIT")
        print("")
        os.chdir(config.get(profile_answer, 'git_path')+"cmake_build")
        os.system("cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo >>" + orig_directory+"/logs/"+uecho_file+".log")
        os.system("make -j10 >>" + orig_directory+"/logs/"+uecho_file+".log")

        print()
        os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
        os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
        os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    else:
        output_title(title, 2)
        prompt("Sorry, not any git installs found in config",True)
        print()


def stk_revert():

    title = "Which profile do you want to revert today?"
    plist = config.sections()
    plist.remove("General")
    names = []
    for name in plist:
        names.append(config.get(name, 'name'))
    option, index = pick(names, title)
    output_title(title, 2)
    print(option)
    print("")
    profile_answer = plist[index]

    prefix = ""
    if config.get(profile_answer,"type") == "sudo":
        prefix = "sudo "
    if config.get(profile_answer,"type") == "git":
        os.chdir(config.get(profile_answer, 'git_path'))
        os.system(prefix+"git clean -f")
    if 'svn_path' in [row[0] for row in config.items(profile_answer)]:
        if config.get(profile_answer,'svn_path') != "":
            os.chdir(config.get(profile_answer, 'svn_path'))
            os.system(prefix+"svn revert --recursive .")

    the_path = orig_directory+"/tmp_files/"+profile_answer+"/"

    filelist = []
    for root, dirs, files in os.walk(the_path):
        for file in files:
            #append the file name to the list
            filelist.append(os.path.join(root,file).replace(the_path,""))

    #print all the file names
    os.chdir(the_path)
    for name in filelist:
        if 'svn_path' in [row[0] for row in config.items(profile_answer)]:
            if ( (config.get(profile_answer, 'svn_path') != "") and (name[0:name.find("/",1)].replace("/","") in issvn) ):
                os.system(prefix+" cp --parents "+name+" "+config.get(profile_answer, 'svn_path'))
            else:
                os.system(prefix+" cp --parents "+name+" "+config.get(profile_answer, 'data_path'))
        else:
            os.system(prefix+" cp --parents "+name+" "+config.get(profile_answer, 'data_path'))




def goo():
    p_up_list = list(dict.fromkeys(assets_data["id"]))
    p_up_list.remove("")

    title = "Which powerup file do you want to use today?"
    option, index = pick(p_up_list, title)
    output_title(title, 2)
    print(option)
    print("")
    powerup_answer = option


    title = "Which profile do you want to use today?"
    plist = config.sections()
    names = []
    for name in plist:
        names.append(config.get(name, 'name'))
    option, index = pick(names, title)
    output_title(title, 2)
    print(option)
    print("")
    profile_answer = plist[index]

    prefix = ""
    if config.get(profile_answer,"type") == "sudo":
        prefix = "sudo "

    title = "Do you wanna debüg today?"
    options = [
        "NÖ (default)",
        "Checklines",
        "Drivelines",
        "CHecklines AND Drivelines"
        ]
    option, index = pick(options, title)
    output_title(title, 2)
    print(option)
    print("")

    suffix = ""
    if index == 1:
        suffix = " --check-debug "
    if index == 2:
        suffix = " --track-debug "
    if index == 3:
        suffix = " --check-debug --track-debug "

    output_title("Am gonna make your dreams come true...", 2)
    print("")

    if config.get(profile_answer,"type") == "git":
        prompt("Cleaning GIT")
        os.chdir(config.get(profile_answer, 'git_path'))
        os.system("git clean -f")
        print("")

    if 'svn_path' in [row[0] for row in config.items(profile_answer)]:
        if config.get(profile_answer, 'svn_path') != "":
            prompt("Cleaning SVN")
            os.chdir(config.get(profile_answer, 'svn_path'))
            os.system("svn revert --recursive .")
            print("")

    prompt("Replacing SFX/GFX files")
    os.chdir(orig_directory+"/my_files/")

    filelist = []

    path = orig_directory+"/my_files/"

    for root, dirs, files in os.walk(orig_directory+"/my_files/"):
        for file in files:
            filelist.append(os.path.join(root,file).replace(path,""))

    for name in filelist:
        if 'svn_path' in [row[0] for row in config.items(profile_answer)]:
            if ( (name[0:name.find("/",1)].replace("/","") in issvn) ):
                os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'svn_path'))
            else:
                os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'data_path'))
        else:
            os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'data_path'))

    print("")


    prompt("Using the choosen powerup file")
    p_up_file_name = list(assets_data['name'].where(assets_data['id'] == powerup_answer).where(assets_data['type'] == "powerup").dropna())
    pfile = p_up_file_name[0]+".xml"
    kart_file_name = list(assets_data['name'].where(assets_data['id'] == powerup_answer).where(assets_data['type'] == "kart").dropna())
    if kart_file_name == []:
        kfile="kart_characteristics_orig.xml"
    else:
        kfile = kart_file_name[0]+".xml"

    os.chdir(config.get(profile_answer, 'data_path'))

    print(prefix+"cp "+orig_directory+"/tmp_files/"+pfile+" powerup.xml")
    os.system(prefix+"rm powerup.xml")
    os.system(prefix+"cp "+orig_directory+"/tmp_files/"+pfile+" powerup.xml")

    print(prefix+"cp "+orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml")
    os.system(prefix+"rm kart_characteristics.xml")
    os.system(prefix+"cp "+orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml")

    print("")

    os.chdir(os.path.dirname( config.get(profile_answer, 'bin_path')  ))
    suffixbis = " | tee -a "+orig_directory+"/logs/"+echo_file+".log"

    prompt("running")
    print("chdir "+ os.path.dirname( config.get(profile_answer, 'bin_path')  ))
    print("."+config.get(profile_answer, 'bin_path').replace(os.path.dirname( config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
    os.system("echo '========================  '"+echo_file+"'  ========================' >>" + orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+echo_file+".log")
    os.system("."+config.get(profile_answer, 'bin_path').replace(os.path.dirname( config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
    os.system("echo '' >>" + orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+echo_file+".log")
    print("")




def main():
    cls()
    setproctitle.setproctitle('ult_STK_launch')

    lala = os.system('echo "WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜" | lolcat ')
    lala = os.system('echo "" | cowsay -f hellokitty | lolcat')

    if lala != 0:
        print("You need to install" + color.BOLD + " cowsay " + color.END + "and" + color.BOLD + " lolcat " + color.END + "in order to get the welcome message displayed. So sorry!")

    print("")
    input("Press Enter to continue...")
    cls()

    if (not(path.exists(orig_directory+"/magic_config.ini")) or os.stat(orig_directory+"/magic_config.ini").st_size == 0):
        initialize()

    output_title("Let's Go!", 1)
    print("")
    config.read(orig_directory+"/magic_config.ini")
    update_extra_files()
    update_addons()


    title = "What do you want to do today?".upper()
    options = ['STÖÖÖÖRT STK',
                'Update STK from git and svn',
                'Revert all changes made to git and svn (emoji file, sfx files, etc.)',
                'Tweak your profiles'
                ]
    option, index = pick(options, title)
    output_title(title, 2)
    print(option)
    print("")

    if index == 0:
        goo()
    elif index == 1:
        stk_update()
    elif index == 2:
        stk_revert()
    elif index == 3:
        output_title("Profiles Tuning",2)
        prompt("not implemented yet",True)
        prompt("At the moment, have fun at: "+orig_directory+"/magic_config.ini",True)
        print("")






started_at = datetime.datetime.now()
echo_file = started_at.strftime("%Y%m%d_%H%M%S")
main()
