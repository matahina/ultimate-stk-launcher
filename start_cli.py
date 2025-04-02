#!/usr/bin/env python3

import subprocess
import os

import time
from pathlib import Path
import datetime
import setproctitle
import questionary
from configparser import ConfigParser
import csv
import pandas as pd
import sys
import libs.update_cli as update
import libs.style_cli as style
import libs.helpers_cli as helpers

import libs.helpers
import libs.settings
import libs.common






started_at = datetime.datetime.now()
echo_file = started_at.strftime("%Y%m%d_%H%M%S")


def goo():
    title = "Which profile do you want to use today?"
    plist = libs.settings.ustkl_config.sections()
    names = []
    for name in plist:
        names.append(libs.settings.ustkl_config.get(name, 'name'))
    option = questionary.select(title, names).ask()
    index = names.index(option)
    print("")
    profile_answer = plist[index]



    p_up_list = list(dict.fromkeys(libs.settings.assets_data["id"]))
    p_up_list.remove("")

    if libs.settings.ustkl_config.get(profile_answer, 'type') == "git2":
        p_up_list = ["STK2"]
    else:
        p_up_list.remove("STK2")
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
    the_verb, prefix = libs.common.starterella(profile_answer,powerup_answer)

    libs.helpers.message_cli(the_verb)

    suffixbis = " | tee -a "+libs.settings.orig_directory+"/logs/"+echo_file+".log"
    command = prefix+"."+libs.settings.ustkl_config.get(profile_answer, 'bin_path').replace(os.path.dirname( libs.settings.ustkl_config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis
    print(command+"\n")

    os.system("echo '========================  '"+echo_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system(command)
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")


    the_verb = libs.common.enderella()

    libs.helpers.message_cli(the_verb)


def initialize():
    title = "What to do?".upper()
    options = ['Config existing install',
                'Install last stable version (1.4)'
                ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    if index == 0:
        libs.helpers.message_cli(["## Empty config file"])
        print("")
        print("")
        style.prompt("Do it yourself :p",True)
        style.prompt("Have fun at: "+libs.settings.orig_directory+"/magic_config.ini",True)
        print("")
        print("")
        quit()
    elif index == 1:
        helpers_cli.stk_stable(config)
        main()

def main():
    libs.settings.init()
    os.chdir(libs.settings.orig_directory)
    setproctitle.setproctitle('ult_STK_launch')
    print("")
    print("")
    print("")
    print("")
    # lala = os.system('echo "WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜" | lolcat ')
    # lala = os.system('echo "" | cowsay -f hellokitty | lolcat')
    #
    # if lala != 0:
    #     print("You need to install" + style.color.BOLD + " cowsay " + style.color.END + "and" + style.color.BOLD + " lolcat " + style.color.END + "in order to get the welcome message displayed. So sorry!")

    print("      /\\_)o<        💜💜💜💜💜💜💜💜💜 WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜\n     |      \\\n     | O . O|\n      \\_____/\n")
    print("")
    input("Press Enter to continue...")

    if (not(os.path.exists(libs.settings.orig_directory+"/magic_config.ini")) or os.stat(libs.settings.orig_directory+"/magic_config.ini").st_size == 0):
        initialize()

    libs.helpers.message_cli(["## Let's Go!"])
    libs.settings.ustkl_config.read(libs.settings.orig_directory+"/magic_libs.settings.ustkl_config.ini")

    libs.helpers.message_cli(["## Downloading powerup files in ",libs.settings.orig_directory+"/tmp_files/"])


    for index,row in libs.settings.assets_data[["url","name"]].iterrows():
        res = libs.common.dl_file(row["url"],row["name"])
        libs.helpers.message_cli(res)

    print("")

    update.addons()
    os.chdir(libs.settings.orig_directory)


    title = "What do you want to do today?".upper()
    options = ['STÖÖÖÖRT STK',
                'Update STK from git and svn',
                'Tweak your profiles',
                'Do another install',
                'Quit'
                ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    if index == 0:
        goo()
        quit()
    elif index == 1:
        title = "Which profile do you want to update today?"
        options = libs.settings.ustkl_config.sections()
        # options.remove("General")
        idx = []
        for i,prof in enumerate(options):
            if libs.settings.ustkl_config.get(prof, 'type') == "git" or libs.settings.ustkl_config.get(prof, 'type') == "git2" or libs.settings.ustkl_config.get(prof, 'type') == "git-kimden" or libs.settings.ustkl_config.get(prof, 'type') == "git-kimden-server" :
                idx.append(i)

        if idx != []:
            plist = [options[i] for i in idx]
            names = []
            for name in plist:
                names.append(libs.settings.ustkl_config.get(name, 'name'))
            option = questionary.select(title, names).ask()
            index = names.index(option)
            print("")
            profile_answer = plist[index]
            update.stk_profile(profile_answer, config)
        else:
            libs.helpers.message_cli(["## "+title])
            style.prompt("Sorry, not any git installs found in config",True)
            print()
        main()
    elif index == 2:
        libs.helpers.message_cli(["## Profiles Tuning"])
        print("")
        print("")
        style.prompt("Do it yourself :p",True)
        style.prompt("Have fun at: "+libs.settings.orig_directory+"/magic_libs.settings.ustkl_config.ini",True)
        print("")
        print("")
    elif index == 3:
        title = "Which version?".upper()
        options = ['STK GIT (master)',
                   'STK STABLE (1.4)',
                   'STK GIT Kimden Client (local-client)',
                   'STK GIT Kimden (command-manager-prototype)',
                   'STK GIT Kimden Server mode (command-manager-prototype)',
                   'STK SPEED',
                    'STK 2']
        option = questionary.select(title, options).ask()
        sp_index = options.index(option)
        print("")
        if sp_index == 0:
            helpers_cli.stk_git(config)
        if sp_index == 1:
            helpers_cli.stk_stable(config)
        if sp_index == 2:
            helpers_cli.stk_git_kimden_client(config)
        if sp_index == 3:
            helpers_cli.stk_git_kimden(config)
        if sp_index == 4:
            helpers_cli.stk_git_kimden_server(config)
        if sp_index == 5:
            helpers_cli.stk_speed(config)
        if sp_index == 6:
            helpers_cli.stk2(config)
        main()
    elif index == 4:
        print()
        quit()






main()
