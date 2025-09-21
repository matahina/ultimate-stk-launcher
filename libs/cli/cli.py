# -*- coding: utf-8 -*-

# Functions for cli

import os
import questionary
import libs.common
import libs.variables
import libs.helpers
import subprocess
import csv
import re
import json
import yaml
from pathlib import Path
import libs.cli.variables

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
                'Update powerups, recipes and addons',
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
        recipes()
        addons()
        menu()
    elif index == 2:
        updaterella()
        menu()
    elif index == 3:
        messengerella = []
        messengerella.append("## Profiles Tuning")
        messengerella.append("Do it yourself :p")
        messengerella.append("Have fun at: "+libs.common.pathery(["magic_libs.variables.ustkl_config.ini"]))
        message(messengerella)
        menu()
    elif index == 4:
        installerella()
        menu()
    elif index == 5:
        playerella()
        menu()
    elif index == 6:
        print()
        exit()

def playerella():
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


def installerella():
    title = "Which version?".upper()
    options = []

    already_there = False
    for prof in libs.variables.ustkl_config.sections():
        if libs.variables.ustkl_config.get(prof,"type") == "stk-distro":
            already_there = True

    if not already_there:
        options.append(libs.cli.variables.stk_distro_installer_string)

    options = options + list(libs.variables.recipes_lib.list_recipes().values())

    options.append(libs.cli.variables.go_back_string)

    option = questionary.select(title, options).ask()
    sp_index = options.index(option)
    if option != libs.cli.variables.go_back_string:
        if option == libs.cli.variables.stk_distro_installer_string:
            libs.helpers.manage_profile(
                "stk-distro",
                "install"
            )
        else:
            if not already_there:
                sp_index = sp_index - 1
            libs.helpers.manage_profile(
                list(libs.variables.recipes_lib.list_recipes().keys())[sp_index],
                "install"
            )
        print("")

def updaterella():
    title = "Which profile do you want to update today?".upper()
    options_list = []
    options_name = []
    for prof in libs.variables.ustkl_config.sections():
        if libs.variables.ustkl_config[prof]["type"] in list(libs.variables.recipes_lib.list_updatable_recipes().keys()):
            options_name.append(libs.variables.ustkl_config[prof]["name"])
            options_list.append(prof)
    options_name.append(libs.cli.variables.go_back_string)
    option = questionary.select(title, options_name).ask()
    sp_index = options_name.index(option)
    if option != libs.cli.variables.go_back_string:
        libs.helpers.manage_profile(
            options_list[sp_index],
            "update"
        )
        print("")

def initialize():
    message(["## You should at least install a new profile!",""])
    installerella()
    menu()


def powerup_update():

    message(["## Downloading powerup files in ", libs.common.pathery(["assets"])])


    message(libs.variables.assets_data.reset())

    try:
        with open(libs.common.pathery(['assets','sources.csv'])) as csvfile:
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


def recipes():

    message(["## Downloading recipes in "+libs.common.pathery(["assets","recipes"])])


    message(libs.variables.recipes_lib.reset())

    try:
        with open(libs.common.pathery(["assets","tmp_files","recipes.json"])) as jsonfile:
            recipes_file = json.load(jsonfile)

        for elem in recipes_file:
            da_recipe_name = elem["name"].replace(".yaml","")
            messagerella = []
            messagerella = messagerella + libs.common.dl_file(elem["download_url"],da_recipe_name,".yaml","recipes")
            if ("Could not retrieve" not in " ".join(messagerella) and da_recipe_name != "example"):
                config = yaml.safe_load(open(
                    libs.common.pathery(["assets","recipes",da_recipe_name+".yaml"])))
                if config['assets']["type"] == "standard":
                    config['assets']['updatable'] = True
                if config['assets']["type"] == "none":
                    config['assets']['updatable'] = False
                libs.variables.recipes_lib.add_recipe(da_recipe_name,
                                                       config['recipe']['name'],
                                                       config['recipe']['stk-version'],
                                                       config['assets']['updatable'] or config['code']['updatable']
                                                       )
            message(messagerella)
    except:
        message(["No recipe sources!"])
    print("")


def addons():

    message(libs.common.update_addon_database())

    print("")
    print("")

    if libs.variables.addon_lib.upd_track != []:
        complmt = ""
        for i in libs.variables.addon_lib.upd_track:
            complmt = complmt + "\n" + "\n- " + libs.variables.addon_lib.avail_tracks[i][1].replace("\r"," ").replace("\n","") + " by " + libs.variables.addon_lib.avail_tracks[i][4].replace("\r"," ").replace("\n","") + " " + libs.variables.addon_lib.avail_tracks[i][5].replace("\r"," ").replace("\n","") + "\n" + "desc: " + libs.variables.addon_lib.avail_tracks[i][6].replace("\r"," ").replace("\n","") + "\n" + "size: " + str(round(int(libs.variables.addon_lib.avail_tracks[i][8])/(1024*1024),1)) + "MB"

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
            options.append(libs.variables.addon_lib.avail_tracks[i][1].replace("\r"," ").replace("\n","") + "  |  " + "by " + libs.variables.addon_lib.avail_tracks[i][4].replace("\r"," ").replace("\n","") + " " + libs.variables.addon_lib.avail_tracks[i][5].replace("\r"," ").replace("\n","") + "  |  " + "desc: " + libs.variables.addon_lib.avail_tracks[i][6].replace("\r"," ").replace("\n","") + "  |  " + "size: " + str(round(int(libs.variables.addon_lib.avail_tracks[i][8])/(1024*1024),1)) + "MB"+ "\n")

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
            complmt = complmt + "\n" + "\n- " + libs.variables.addon_lib.avail_arenas[i][1].replace("\r"," ").replace("\n","") + " by " + libs.variables.addon_lib.avail_arenas[i][4].replace("\r"," ").replace("\n","") + " " + libs.variables.addon_lib.avail_arenas[i][5].replace("\r"," ").replace("\n","") + "\n" + "desc: " + libs.variables.addon_lib.avail_arenas[i][6].replace("\r"," ").replace("\n","") + "\n" + "size: " + str(round(int(libs.variables.addon_lib.avail_arenas[i][8])/(1024*1024),1)) + "MB"

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
            options.append(libs.variables.addon_lib.avail_arenas[i][1].replace("\r"," ").replace("\n","") + "  |  " + "by " + libs.variables.addon_lib.avail_arenas[i][4].replace("\r"," ").replace("\n","") + " " + libs.variables.addon_lib.avail_arenas[i][5].replace("\r"," ").replace("\n","") + "  |  " + "desc: " + libs.variables.addon_lib.avail_arenas[i][6].replace("\r"," ").replace("\n","") + "  |  " + "size: " + str(round(int(libs.variables.addon_lib.avail_arenas[i][8])/(1024*1024),1)) + "MB"+ "\n")

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
    the_list = libs.variables.ustkl_config.sections()
    names = []
    plist = []
    for name in the_list:
        if "server" not in libs.variables.ustkl_config.get(name, 'type'):
            plist.append(name)
            names.append(libs.variables.ustkl_config.get(name, 'name'))
    names.append(libs.cli.variables.go_back_string)
    option = questionary.select(title, names).ask()
    index = names.index(option)
    if option != libs.cli.variables.go_back_string:
        print("")
        profile_answer = plist[index]

        p_up_list = libs.variables.assets_data.list_assets(libs.variables.ustkl_config.get(profile_answer, 'stk-version'))
        if p_up_list != []:
            p_up_list.append(libs.cli.variables.go_back_string)
            title = "Which powerup file do you want to use today?"
            option = questionary.select(title, p_up_list).ask()
            index = p_up_list.index(option)
            print("")

        if option != libs.cli.variables.go_back_string or p_up_list == []:
            if p_up_list == []:
                powerup_answer = "None"
            else:
                powerup_answer = option

            title = "Do you wanna debüg today?"
            options = [
                "NÖ (default)",
                "Checklines",
                "Drivelines",
                "CHecklines AND Drivelines",
                libs.cli.variables.go_back_string
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
            if option != libs.cli.variables.go_back_string:
                suffixbis = ""
                if powerup_answer == "None":
                    pupkartlist = []
                else:
                    pupkartlist = libs.variables.assets_data.get_assets(
                        powerup_answer,
                        libs.variables.ustkl_config.get(profile_answer, 'stk-version')
                        )

                messengerella = libs.common.starterella(profile_answer,pupkartlist)

                message(messengerella)

                command = libs.variables.ustkl_config.get(profile_answer, 'bin_path')

                messengerella = ["# Running executable"]

                run([command]+suffix, messengerella)

                messengerella = libs.common.enderella()

                message(messengerella)

def run(the_command, the_message):

        the_message.append(" ".join(the_command))
        message(the_message)

        # invoke process
        process = subprocess.Popen(the_command,shell=False,stdout=subprocess.PIPE)

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

def get_nproc():

    result = "1"
    try:
        computer_says = int(subprocess.check_output(['nproc']).decode("utf-8").replace("\n",""))-1
        if computer_says > 1:
            result = str(computer_says)
    except:
        pass

    return result

