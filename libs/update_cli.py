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


def addons():

    style.output_title("Checking for addons",2)


    update_log = libs.common.update_addon_database()


    for elem in update_log:
        if "not retrieve" in elem:
            print(style.color.RED + elem + style.color.END)
        else:
            print(elem)


    if libs.settings.addon_lib.upd_track != []:
        complmt = ""
        for i in libs.settings.addon_lib.upd_track:
            complmt = complmt + "\n" + "\n- " + libs.settings.addon_lib.avail_tracks[i][1] + " by " + libs.settings.addon_lib.avail_tracks[i][4] + " " + libs.settings.addon_lib.avail_tracks[i][5] + "\n" + "desc: " + libs.settings.addon_lib.avail_tracks[i][6] + "\n" + "size: " + str(round(int(libs.settings.addon_lib.avail_tracks[i][8])/(1024*1024),1)) + "MB"

        title = "Do you wanna update those addon tracks?"+complmt
        options = ['Yeah',
                    'Nope'
                    ]
        option = questionary.select(title, options).ask()
        index = options.index(option)
        print("")

        if index == 0:
            for i in libs.settings.addon_lib.upd_track:
                log = libs.common.get_addon(i,"track","update")
                for elem in log:
                    if "Error" in elem:
                        print(style.color.RED + elem + style.color.END)
                    else:
                        print(elem)

    if libs.settings.addon_lib.to_inst_track != []:
        options = []
        for i in libs.settings.addon_lib.to_inst_track:
            options.append(libs.settings.addon_lib.avail_tracks[i][1] + "  |  " + "by " + libs.settings.addon_lib.avail_tracks[i][4] + " " + libs.settings.addon_lib.avail_tracks[i][5] + "  |  " + "desc: " + libs.settings.addon_lib.avail_tracks[i][6] + "  |  " + "size: " + str(round(int(libs.settings.addon_lib.avail_tracks[i][8])/(1024*1024),1)) + "MB"+ "\n")

        title = "Maybe you wanna install those new addon tracks since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
        selected = questionary.checkbox(title,choices=options).ask()
        print("")

        if selected != []:
            sel_tracks = []
            for i in selected:
                sel_tracks.append(new_tracks[options.index(i)])
            for j,i in enumerate(sel_tracks):
                log = libs.common.get_addon(i,"track","install")
                for elem in log:
                    if "Error" in elem:
                        print(style.color.RED + elem + style.color.END)
                    else:
                        print(elem)


    if libs.settings.addon_lib.upd_arena != []:
        complmt = ""
        for i in libs.settings.addon_lib.upd_arena:
            complmt = complmt + "\n" + "\n- " + libs.settings.addon_lib.avail_arenas[i][1] + " by " + libs.settings.addon_lib.avail_arenas[i][4] + " " + libs.settings.addon_lib.avail_arenas[i][5] + "\n" + "desc: " + libs.settings.addon_lib.avail_arenas[i][6] + "\n" + "size: " + str(round(int(libs.settings.addon_lib.avail_arenas[i][8])/(1024*1024),1)) + "MB"

        title = "Do you wanna update those addon arenas?"+complmt
        options = ['Yeah',
                    'Nope'
                    ]
        option = questionary.select(title, options).ask()
        index = options.index(option)
        print("")

        if index == 0:
            for i in libs.settings.addon_lib.upd_arena:
                log = libs.common.get_addon(i,"arena","update")
                for elem in log:
                    if "Error" in elem:
                        print(style.color.RED + elem + style.color.END)
                    else:
                        print(elem)



    if libs.settings.addon_lib.to_inst_arena != []:
        options = []
        for i in libs.settings.addon_lib.to_inst_arena:
            options.append(libs.settings.addon_lib.avail_arenas[i][1] + "  |  " + "by " + libs.settings.addon_lib.avail_arenas[i][4] + " " + libs.settings.addon_lib.avail_arenas[i][5] + "  |  " + "desc: " + libs.settings.addon_lib.avail_arenas[i][6] + "  |  " + "size: " + str(round(int(libs.settings.addon_lib.avail_arenas[i][8])/(1024*1024),1)) + "MB"+ "\n")

        title = "Maybe you wanna install those new addon arenas since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
        selected = questionary.checkbox(title,choices=options).ask()
        print("")

        if selected != []:
            sel_arenas = []
            for i in selected:
                sel_arenas.append(new_arenas[options.index(i)])
            for j,i in enumerate(sel_arenas):
                log = libs.common.get_addon(i,"arena","install")
                for elem in log:
                    if "Error" in elem:
                        print(style.color.RED + elem + style.color.END)
                    else:
                        print(elem)


    print("")
    print("")


def stk_profile(profile_answer, config):

    started_at = datetime.datetime.now()
    uecho_file = "UPDATE_"+profile_answer+"_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    style.prompt("Updating "+profile_answer + " " + config.get(profile_answer, 'name'))

    if config.get(profile_answer, 'type') == "git2":
        os.system("sh "+libs.settings.orig_directory+"/libs/update_stk_git2.sh "+config.get(profile_answer, 'svn_path')+ " " +config.get(profile_answer, 'git_path')+ " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    elif config.get(profile_answer, 'type') == "git-kimden-server":
        os.system("sh "+libs.settings.orig_directory+"/libs/update_stk_kimden_server.sh "+config.get(profile_answer, 'svn_path')+ " " +config.get(profile_answer, 'git_path')+ " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    else:
        os.system("sh "+libs.settings.orig_directory+"/libs/update_stk_git.sh "+config.get(profile_answer, 'svn_path')+ " " +config.get(profile_answer, 'git_path')+ " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
