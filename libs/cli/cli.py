# -*- coding: utf-8 -*-

# Functions for cli

import os
import questionary
import libs.common
import libs.variables
import libs.helpers
import datetime

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


def menu():

    print("")

    print("")
    title = "What do you want to do today?".upper()
    options = ['STÖÖÖÖRT STK',
                'Update powerups and addons',
                'Update STK from git and svn',
                'Tweak your profiles',
                'Do another install',
                "See who's online",
                'Quit'
                ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    if index == 0:
        goo()
        menu()
    elif index == 1:
        powerup_update()
        addons()
        menu()
    elif index == 2:
        title = "Which profile do you want to update today?"
        options = libs.variables.ustkl_config.sections()
        # options.remove("General")
        idx = []
        for i,prof in enumerate(options):
            if libs.variables.ustkl_config.get(prof, 'type') == "git" or libs.variables.ustkl_config.get(prof, 'type') == "git2" or libs.variables.ustkl_config.get(prof, 'type') == "git2_tme" or libs.variables.ustkl_config.get(prof, 'type') == "git-kimden" or libs.variables.ustkl_config.get(prof, 'type') == "git-kimden-server" :
                idx.append(i)

        if idx != []:
            plist = [options[i] for i in idx]
            names = []
            for name in plist:
                names.append(libs.variables.ustkl_config.get(name, 'name'))
            option = questionary.select(title, names).ask()
            index = names.index(option)
            print("")
            profile_answer = plist[index]
            libs.helpers.manage_profile("update",profile_answer)
        else:
            messengerella = []
            messengerella.append("## "+title)
            messengerella.append("Sorry, not any git installs found in config")
            message(messengerella)
            print()
        menu()
    elif index == 3:
        messengerella = []
        messengerella.append("## Profiles Tuning")
        messengerella.append("Do it yourself :p")
        messengerella.append("Have fun at: "+libs.variables.orig_directory+"/magic_libs.variables.ustkl_config.ini")
        message(messengerella)
    elif index == 4:
        installerella()
        menu()
    elif index == 5:
        print()
        message(libs.common.update_online_database())
        messengerella = []
        messengerella.append("## "+str(libs.variables.online_db.total_players)+" player")
        if libs.variables.online_db.total_players > 1:
            messengerella[-1] = messengerella[-1] + "s"
        for elem in range(0,len(libs.variables.online_db.servers)):
            messengerella.append("\n# "+libs.variables.online_db.servers[elem][0])
            for i in range(1,len(libs.variables.online_db.servers[elem])):
                messengerella.append("   "+libs.variables.online_db.servers[elem][i])
            messengerella.append("   "+"Players")
            for pelem in libs.variables.online_db.players[elem]:
                messengerella.append("      "+pelem)
        message(messengerella)
        menu()
    elif index == 6:
        print()
        quit()

def installerella():
    title = "Which version?".upper()
    options = ['STK GIT (master)',
               'STK STABLE (1.4)',
               'STK GIT Kimden Client (local-client)',
               'STK GIT Kimden (command-manager-prototype)',
               'STK GIT Kimden Server mode (command-manager-prototype)',
               'STK SPEED',
                'STK 2',
                'STK 2 TME (nomagno)']
    option = questionary.select(title, options).ask()
    sp_index = options.index(option)
    print("")
    if sp_index == 0:
        libs.helpers.manage_profile("stk_git")
    if sp_index == 1:
        libs.helpers.manage_profile("stk_stable")
    if sp_index == 2:
        libs.helpers.manage_profile("stk_git_kimden_client")
    if sp_index == 3:
        libs.helpers.manage_profile("stk_git_kimden")
    if sp_index == 4:
        libs.helpers.manage_profile("stk_git_kimden_server")
    if sp_index == 5:
        libs.helpers.manage_profile("stk_speed")
    if sp_index == 6:
        libs.helpers.manage_profile("stk2")
    if sp_index == 7:
        libs.helpers.manage_profile("stk2_tme")


def initialize():
    message(["## You should at least install a new profile!",""])
    installerella()
    menu()


def powerup_update():

    message(["## Downloading powerup files in ",libs.variables.orig_directory+"/tmp_files/"])


    for index,row in libs.variables.assets_data[["url","name"]].iterrows():
        res = libs.common.dl_file(row["url"],row["name"])
        message(res)

    print("")


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


def goo():
    title = "Which profile do you want to use today?"
    plist = libs.variables.ustkl_config.sections()
    names = []
    for name in plist:
        names.append(libs.variables.ustkl_config.get(name, 'name'))
    option = questionary.select(title, names).ask()
    index = names.index(option)
    print("")
    profile_answer = plist[index]





    p_up_list = libs.common.powerup_list(libs.variables.ustkl_config.get(profile_answer, 'type'))
    title = "Which powerup file do you want to use today?"
    option = questionary.select(title, p_up_list).ask()
    index = p_up_list.index(option)
    print("")
    powerup_answer = option

    title = "Do you wanna debüg today?"
    options = [
        "NÖ (default)",
        "Checklines",
        "Drivelines",
        "CHecklines AND Drivelines"
        ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    suffix = ""
    if index == 1:
        suffix = " --check-debug "
    if index == 2:
        suffix = " --track-debug "
    if index == 3:
        suffix = " --check-debug --track-debug "

    prefix = ""
    suffixbis = ""
    messengerella, prefix = libs.common.starterella(profile_answer,powerup_answer)

    message(messengerella)

    started_at = datetime.datetime.now()
    echo_file = started_at.strftime("%Y%m%d_%H%M%S")

    suffixbis = " | tee -a "+libs.variables.orig_directory+"/logs/"+echo_file+".log"
    command = prefix+"."+libs.variables.ustkl_config.get(profile_answer, 'bin_path').replace(os.path.dirname( libs.variables.ustkl_config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis
    print(command+"\n")

    os.system("echo '========================  '"+echo_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
    os.system(command)
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")


    messengerella = libs.common.enderella()

    message(messengerella)
