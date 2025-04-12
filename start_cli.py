# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# python start_cli.py
# to launch the cli version

import subprocess
import os

from pathlib import Path
import datetime
import setproctitle
import questionary
import libs.cli
import libs.helpers
import libs.common
import libs.variables






started_at = datetime.datetime.now()
echo_file = started_at.strftime("%Y%m%d_%H%M%S")


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




    if libs.variables.ustkl_config.get(profile_answer, 'type') == "git2":
        p_up_list = libs.common.powerup_list(2)
    else:
        p_up_list = libs.common.powerup_list(0)
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

    libs.cli.message(messengerella)

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

    libs.cli.message(messengerella)


def initialize():
    title = "What to do?".upper()
    options = ['Config existing install',
                'Install last stable version (1.4)'
                ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    if index == 0:
        messengerella = []
        messengerella.append("## Empty config file")
        messengerella.append("# Do it yourself :p")
        messengerella.append("Have fun at: "+libs.variables.orig_directory+"/magic_config.ini")
        libs.cli.message(messengerella)
        quit()
    elif index == 1:
        libs.helpers.stk_stable()
        main()

def main():
    libs.variables.init()
    os.chdir(libs.variables.orig_directory)
    setproctitle.setproctitle('ult_STK_launch')
    print("")
    print("")
    print("")
    print("")

    print("      /\\_)o<        💜💜💜💜💜💜💜💜💜 WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜\n     |      \\\n     | O . O|"+"                                  Version: "+libs.variables.version+"\n      \\_____/\n")
    print("")
    input("Press Enter to continue...")

    if (not(os.path.exists(libs.variables.orig_directory+"/magic_config.ini")) or os.stat(libs.variables.orig_directory+"/magic_config.ini").st_size == 0):
        initialize()

    libs.cli.message(["## Let's Go!"])
    libs.variables.ustkl_config.read(libs.variables.orig_directory+"/magic_libs.variables.ustkl_config.ini")

    libs.cli.message(["## Downloading powerup files in ",libs.variables.orig_directory+"/tmp_files/"])


    for index,row in libs.variables.assets_data[["url","name"]].iterrows():
        res = libs.common.dl_file(row["url"],row["name"])
        libs.cli.message(res)

    print("")

    libs.cli.addons()
    os.chdir(libs.variables.orig_directory)
    menu()

def menu():

    print("")

    print("")
    title = "What do you want to do today?".upper()
    options = ['STÖÖÖÖRT STK',
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
        title = "Which profile do you want to update today?"
        options = libs.variables.ustkl_config.sections()
        # options.remove("General")
        idx = []
        for i,prof in enumerate(options):
            if libs.variables.ustkl_config.get(prof, 'type') == "git" or libs.variables.ustkl_config.get(prof, 'type') == "git2" or libs.variables.ustkl_config.get(prof, 'type') == "git-kimden" or libs.variables.ustkl_config.get(prof, 'type') == "git-kimden-server" :
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
            libs.cli.message(messengerella)
            print()
        menu()
    elif index == 2:
        messengerella = []
        messengerella.append("## Profiles Tuning")
        messengerella.append("Do it yourself :p")
        messengerella.append("Have fun at: "+libs.variables.orig_directory+"/magic_libs.variables.ustkl_config.ini")
        libs.cli.message(messengerella)
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
        menu()
    elif index == 4:
        print()
        libs.cli.message(libs.common.update_online_database())
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
        libs.cli.message(messengerella)
        menu()
    elif index == 5:
        print()
        quit()






main()
