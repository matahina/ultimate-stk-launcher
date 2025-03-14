import libs.style_cli as style
import csv
import pandas as pd
from lxml import etree
from pick import pick
import xml.etree.ElementTree as ET
import os
from urllib import request
from configparser import ConfigParser
import datetime
import questionary
from pathlib import Path
import libs.settings

def extra_files(assets_data):
    orig_directory = os.getcwd()
    style.output_title("Downloading powerup files in ",2)
    print(style.color.CYAN + orig_directory+"/tmp_files/" + style.color.END)


    for index,row in assets_data[["url","name"]].iterrows():
        print("")
        style.prompt(row["name"])
        try:
            request.urlretrieve(row["url"], orig_directory+"/tmp_files/"+row["name"]+".xml")
        except:
            print(style.color.RED + "Could not retrieve " + row["url"] + style.color.END)
        else:
            print("OK " + row["url"])

    print("")

def addons():
    orig_directory = os.getcwd()
    style.output_title("Checking for addons",2)
    try:
        request.urlretrieve("https://online.supertuxkart.net/downloads/xml/online_assets.xml", orig_directory+"/tmp_files/online_assets.xml")
    except:
        print(style.color.RED + "Could not retrieve " + "https://online.supertuxkart.net/downloads/xml/online_assets.xml" + style.color.END)

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
            option = questionary.select(title, options).ask()
            index = options.index(option)
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
                    if not(avail_tracks[i][0] in list_b):
                        new_elem=[i,avail_tracks[i][0],avail_tracks[i][1]]
                        if new_tracks != []:
                            if new_tracks[-1][1] == new_elem[1]:
                                brrr=new_tracks.pop()
                        new_tracks.append(new_elem)
            new_tracks=[row[0] for row in new_tracks]

        if new_tracks != []:
            options = []
            for i in new_tracks:
                options.append(avail_tracks[i][1] + "  |  " + "by " + avail_tracks[i][4] + " " + avail_tracks[i][5] + "  |  " + "desc: " + avail_tracks[i][6] + "  |  " + "size: " + str(round(int(avail_tracks[i][8])/(1024*1024),1)) + "MB"+ "\n")

            title = "Maybe you wanna install those new addon tracks since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
            selected = questionary.checkbox(title,choices=options).ask()
            print("")

            if selected != []:
                sel_tracks = []
                for i in selected:
                    sel_tracks.append(new_tracks[options.index(i)])
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
            option = questionary.select(title, options).ask()
            index = options.index(option)
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
                    if not(avail_arenas[i][0] in list_b):
                        new_elem=[i,avail_arenas[i][0],avail_arenas[i][1]]
                        if new_arenas != []:
                            if new_arenas[-1][1] == new_elem[1]:
                                brrr=new_arenas.pop()
                        new_arenas.append(new_elem)
            new_arenas=[row[0] for row in new_arenas]

        if new_arenas != []:
            options = []
            for i in new_arenas:
                options.append(avail_arenas[i][1] + "  |  " + "by " + avail_arenas[i][4] + " " + avail_arenas[i][5] + "  |  " + "desc: " + avail_arenas[i][6] + "  |  " + "size: " + str(round(int(avail_arenas[i][8])/(1024*1024),1)) + "MB"+ "\n")

            title = "Maybe you wanna install those new addon arenas since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
            selected = questionary.checkbox(title,choices=options).ask()
            print("")

            if selected != []:
                sel_arenas = []
                for i in selected:
                    sel_arenas.append(new_arenas[options.index(i)])
                for j,i in enumerate(sel_arenas):
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                    os.system("rm -rf "+avail_arenas[i][0])
                    Path(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_arenas[i][0]).mkdir(parents=True, exist_ok=True)
                    os.chdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+avail_arenas[i][0])
                    request.urlretrieve(avail_arenas[i][2], avail_arenas[i][3]+".zip")
                    os.system("unzip "+avail_arenas[i][3]+".zip")
                    os.system("rm "+avail_arenas[i][3]+".zip")


    print("")
    print("")


def stk_profile(profile_answer, config):

    started_at = datetime.datetime.now()
    uecho_file = "UPDATE_"+profile_answer+"_"+started_at.strftime("%Y%m%d_%H%M%S")

    orig_directory = os.getcwd()
    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")

    style.prompt("Updating "+profile_answer + " " + config.get(profile_answer, 'name'))

    if config.get(profile_answer, 'type') == "git2":
        os.system("sh "+orig_directory+"/libs/update_stk_git2.sh "+config.get(profile_answer, 'svn_path')+ " " +config.get(profile_answer, 'git_path')+ " | tee -a " + orig_directory+"/logs/"+uecho_file+".log")
    elif config.get(profile_answer, 'type') == "git-kimden-server":
        os.system("sh "+orig_directory+"/libs/update_stk_kimden_server.sh "+config.get(profile_answer, 'svn_path')+ " " +config.get(profile_answer, 'git_path')+ " | tee -a " + orig_directory+"/logs/"+uecho_file+".log")
    else:
        os.system("sh "+orig_directory+"/libs/update_stk_git.sh "+config.get(profile_answer, 'svn_path')+ " " +config.get(profile_answer, 'git_path')+ " | tee -a " + orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
