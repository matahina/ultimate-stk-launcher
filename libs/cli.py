# -*- coding: utf-8 -*-

# Functions for cli

import os
import datetime
import questionary
import libs.common
import libs.variables

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

def message(text):
    for elem in text:
        if "##" in elem:
            print("\n"+color.GREEN + elem.upper() + color.END)
        else:
            if "Could not retrieve" in elem or "Error" in elem:
                print(color.RED + elem + color.END)
            else:
                print(elem)

def addons():

    message(libs.common.update_addon_database())

    print("")
    print("")

    if libs.variables.addon_lib.upd_track != []:
        complmt = ""
        for i in libs.variables.addon_lib.upd_track:
            complmt = complmt + "\n" + "\n- " + libs.variables.addon_lib.avail_tracks[i][1] + " by " + libs.variables.addon_lib.avail_tracks[i][4] + " " + libs.variables.addon_lib.avail_tracks[i][5] + "\n" + "desc: " + libs.variables.addon_lib.avail_tracks[i][6] + "\n" + "size: " + str(round(int(libs.variables.addon_lib.avail_tracks[i][8])/(1024*1024),1)) + "MB"

        title = "Do you wanna update those addon tracks?"+complmt
        options = ['Yeah',
                    'Nope'
                    ]
        option = questionary.select(title, options).ask()
        index = options.index(option)
        print("")

        if index == 0:
            for i in libs.variables.addon_lib.upd_track:
                log = libs.common.get_addon(i,"track","update")
                message(log)

    if libs.variables.addon_lib.to_inst_track != []:
        options = []
        for i in libs.variables.addon_lib.to_inst_track:
            options.append(libs.variables.addon_lib.avail_tracks[i][1] + "  |  " + "by " + libs.variables.addon_lib.avail_tracks[i][4] + " " + libs.variables.addon_lib.avail_tracks[i][5] + "  |  " + "desc: " + libs.variables.addon_lib.avail_tracks[i][6] + "  |  " + "size: " + str(round(int(libs.variables.addon_lib.avail_tracks[i][8])/(1024*1024),1)) + "MB"+ "\n")

        title = "Maybe you wanna install those new addon tracks since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
        selected = questionary.checkbox(title,choices=options).ask()
        print("")

        if selected != []:
            sel_tracks = []
            for i in selected:
                sel_tracks.append(libs.variables.addon_lib.to_inst_track[options.index(i)])
            for j,i in enumerate(sel_tracks):
                log = libs.common.get_addon(i,"track","install")
                message(log)


    if libs.variables.addon_lib.upd_arena != []:
        complmt = ""
        for i in libs.variables.addon_lib.upd_arena:
            complmt = complmt + "\n" + "\n- " + libs.variables.addon_lib.avail_arenas[i][1] + " by " + libs.variables.addon_lib.avail_arenas[i][4] + " " + libs.variables.addon_lib.avail_arenas[i][5] + "\n" + "desc: " + libs.variables.addon_lib.avail_arenas[i][6] + "\n" + "size: " + str(round(int(libs.variables.addon_lib.avail_arenas[i][8])/(1024*1024),1)) + "MB"

        title = "Do you wanna update those addon arenas?"+complmt
        options = ['Yeah',
                    'Nope'
                    ]
        option = questionary.select(title, options).ask()
        index = options.index(option)
        print("")

        if index == 0:
            for i in libs.variables.addon_lib.upd_arena:
                log = libs.common.get_addon(i,"arena","update")
                message(log)



    if libs.variables.addon_lib.to_inst_arena != []:
        options = []
        for i in libs.variables.addon_lib.to_inst_arena:
            options.append(libs.variables.addon_lib.avail_arenas[i][1] + "  |  " + "by " + libs.variables.addon_lib.avail_arenas[i][4] + " " + libs.variables.addon_lib.avail_arenas[i][5] + "  |  " + "desc: " + libs.variables.addon_lib.avail_arenas[i][6] + "  |  " + "size: " + str(round(int(libs.variables.addon_lib.avail_arenas[i][8])/(1024*1024),1)) + "MB"+ "\n")

        title = "Maybe you wanna install those new addon arenas since last time?\n[Press SPACE to select, ▲ ▼ to navigate, ENTER to confirm]"
        selected = questionary.checkbox(title,choices=options).ask()
        print("")

        if selected != []:
            sel_arenas = []
            for i in selected:
                sel_arenas.append(libs.variables.addon_lib.to_inst_arena[options.index(i)])
            for j,i in enumerate(sel_arenas):
                log = libs.common.get_addon(i,"arena","install")
                message(log)


    print("")
    print("")


def update_profile(profile_answer):

    started_at = datetime.datetime.now()
    uecho_file = "UPDATE_"+profile_answer+"_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    message(["## Updating "+profile_answer + " " + libs.variables.ustkl_config.get(profile_answer, 'name')])

    if libs.variables.ustkl_config.get(profile_answer, 'type') == "git2":
        os.system("sh "+libs.variables.orig_directory+"/libs/update_stk_git2.sh "+libs.variables.ustkl_config.get(profile_answer, 'svn_path')+ " " +libs.variables.ustkl_config.get(profile_answer, 'git_path')+ " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    elif libs.variables.ustkl_config.get(profile_answer, 'type') == "git-kimden-server":
        os.system("sh "+libs.variables.orig_directory+"/libs/update_stk_kimden_server.sh "+libs.variables.ustkl_config.get(profile_answer, 'svn_path')+ " " +libs.variables.ustkl_config.get(profile_answer, 'git_path')+ " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    else:
        os.system("sh "+libs.variables.orig_directory+"/libs/update_stk_git.sh "+libs.variables.ustkl_config.get(profile_answer, 'svn_path')+ " " +libs.variables.ustkl_config.get(profile_answer, 'git_path')+ " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
