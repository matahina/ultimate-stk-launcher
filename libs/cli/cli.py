# -*- coding: utf-8 -*-

# Functions for cli

import os
import questionary
import libs.common
import libs.variables
import libs.helpers
import datetime
import subprocess
import csv
import re

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

def message(text, err = False):
    for elem in text:
        libs.variables.mylog.info(elem.replace("\n",""))
        if "##" in elem:
            print("\n"+color.GREEN + elem.upper() + color.END)
        else:
            if "Could not retrieve" in elem or "Error" in elem or err:
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
            if libs.variables.ustkl_config.get(prof, 'type') == "git" or libs.variables.ustkl_config.get(prof, 'type') == "git2" or libs.variables.ustkl_config.get(prof, 'type') == "git2_emt" or libs.variables.ustkl_config.get(prof, 'type') == "git-kimden-client" or libs.variables.ustkl_config.get(prof, 'type') == "git-kimden-server" :
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
        menu()
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
        exit()

def installerella():
    title = "Which version?".upper()
    options = ['STK GIT (master)',
               'STK STABLE (1.4)',
               'STK GIT Kimden Client (local-client)',
               'STK GIT Kimden (master)',
               'STK GIT Kimden Server mode (master)',
               'STK SPEED',
                'STK 2',
                'STK 2 Eat My Tyre (nomagno)']
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
        libs.helpers.manage_profile("stk2_emt")


def initialize():
    message(["## You should at least install a new profile!",""])
    installerella()
    menu()


def powerup_update():

    message(["## Downloading powerup files in ",libs.variables.orig_directory+"/assets/"])


    message(libs.variables.assets_data.reset())

    try:
        with open(libs.variables.orig_directory+'/assets/sources.csv') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if row[0] != "id":
                    messagerella = []
                    messagea = []
                    messageb = []
                    if row[4] != "standard":
                        messagea = libs.common.dl_file(row[4],"powerup_"+row[2])
                        messagerella = messagerella + messagea
                    if row[5] != "standard":
                        messageb = libs.common.dl_file(row[5],"kart_"+row[2])
                        messagerella = messagerella + messageb
                    if ("Could not retrieve" not in " ".join(messagea) and "Could not retrieve" not in " ".join(messageb)):
                        if row[0] == "standard" :
                            libs.variables.assets_data.add_standard(row[2],row[3],row[4],row[5])
                        else:
                            libs.variables.assets_data.add_asset(row[0],row[2],row[3],row[4],row[5])
                    message(messagerella)
    except:
        message(["No asset sources!"])
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






    p_up_list = libs.variables.assets_data.list_assets(libs.variables.ustkl_config.get(profile_answer, 'version'))
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
        "CHecklines AND Drivelines",
        "🠜 Back to main menu"
        ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    suffix = []
    if index == 1:
        suffix.append("--check-debug")
    if index == 2:
        suffix.append("--track-debug")
    if index == 3:
        suffix.append("--check-debug")
        suffix.append("--track-debug")
    if index == 4:
        menu()
    else:
        prefix = ""
        suffixbis = ""
        messengerella, prefix = libs.common.starterella(profile_answer,libs.variables.assets_data.get_assets(powerup_answer,libs.variables.ustkl_config.get(profile_answer, 'version')))

        message(messengerella)
        command = prefix+"."+libs.variables.ustkl_config.get(profile_answer, 'bin_path').replace(os.path.dirname( libs.variables.ustkl_config.get(profile_answer, 'bin_path')  ),'')
        print(command + " ".join(suffix) +"\n")

        # invoke process
        process = subprocess.Popen([command]+suffix,shell=False,stdout=subprocess.PIPE)

        # Poll process.stdout to show stdout live
        while True:
          output = process.stdout.readline().decode('utf-8')
          if process.poll() is not None:
            break
          if output:
            message([
                re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('',
                                                                         str(output.strip()))
                                                ])


        messengerella = libs.common.enderella()

        message(messengerella)
