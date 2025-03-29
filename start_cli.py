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

import libs.settings
import libs.common



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

    style.output_title("Am gonna make your dreams come true...", 2)
    print("")

    style.prompt("Copying SFX/GFX/data files into tmp files...")
    libs.settings.data_relocation = libs.common.relocate_data(libs.settings.ustkl_config.get(profile_answer, 'data_path'))
    if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_answer)]:
        libs.settings.assets_relocation = libs.common.relocate_data(libs.settings.ustkl_config.get(profile_answer, 'svn_path'))
        print("location [assets]: "+libs.settings.assets_relocation)
    print("location [data]: "+libs.settings.data_relocation)
    os.chdir(libs.settings.orig_directory+"/my_files/")



    the_verb = libs.common.temperella(profile_answer)

    for elem in the_verb:
        print(elem)

    print("")


    style.prompt("Using the choosen powerup file")
    p_up_file_name = list(libs.settings.assets_data['name'].where(libs.settings.assets_data['id'] == powerup_answer).where(libs.settings.assets_data['type'] == "powerup").dropna())
    pfile = p_up_file_name[0]+".xml"
    kart_file_name = list(libs.settings.assets_data['name'].where(libs.settings.assets_data['id'] == powerup_answer).where(libs.settings.assets_data['type'] == "kart").dropna())
    if kart_file_name == []:
        kfile="kart_characteristics_orig.xml"
    else:
        kfile = kart_file_name[0]+".xml"

    os.chdir(libs.settings.data_relocation)
    print("chdir "+libs.settings.data_relocation)

    print("cp "+libs.settings.orig_directory+"/tmp_files/"+pfile+" powerup.xml")
    print("cp "+libs.settings.orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml")
    os.remove("powerup.xml")
    os.remove("kart_characteristics.xml")
    os.system("cp "+libs.settings.orig_directory+"/tmp_files/"+pfile+" powerup.xml")
    os.system("cp "+libs.settings.orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml")

    print("")

    os.chdir(os.path.dirname( libs.settings.ustkl_config.get(profile_answer, 'bin_path')  ))
    suffixbis = " | tee -a "+libs.settings.orig_directory+"/logs/"+echo_file+".log"
    prefix = ""
    if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_answer)]:
        prefix = prefix + 'export SUPERTUXKART_ASSETS_DIR="'+libs.settings.assets_relocation+'" ; '

    prefix = prefix + 'export SUPERTUXKART_DATADIR="'+libs.settings.data_relocation[:-6]+'" ; '
    if libs.settings.ustkl_config.get(profile_answer, 'type') == "other":
        prefix = prefix + "export SYSTEM_LD_LIBRARY_PATH=\"$LD_LIBRARY_PATH\";export LD_LIBRARY_PATH=\"$DIRNAME/lib:$LD_LIBRARY_PATH\" ; "
    style.prompt("running")
    print("chdir "+ os.path.dirname( libs.settings.ustkl_config.get(profile_answer, 'bin_path')  ))
    print(prefix+"."+libs.settings.ustkl_config.get(profile_answer, 'bin_path').replace(os.path.dirname( libs.settings.ustkl_config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
    os.system("echo '========================  '"+echo_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system(prefix+"."+libs.settings.ustkl_config.get(profile_answer, 'bin_path').replace(os.path.dirname( libs.settings.ustkl_config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
    print("")


    style.prompt("Removing tmp files")
    print("rm -R "+libs.settings.data_relocation)
    os.system("rm -R "+libs.settings.data_relocation)
    if ('svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_answer)]):
        print("rm -R "+libs.settings.assets_relocation)
        os.system("rm -R "+libs.settings.assets_relocation)

    libs.settings.assets_relocation = ""
    libs.settings.data_relocation = ""
    print("")


def initialize():
    title = "What to do?".upper()
    options = ['Config existing install',
                'Install last stable version (1.4)'
                ]
    option = questionary.select(title, options).ask()
    index = options.index(option)
    print("")

    if index == 0:
        style.output_title("Empty config file",2)
        print("")
        print("")
        style.prompt("Do it yourself :p",True)
        style.prompt("Have fun at: "+libs.settings.orig_directory+"/magic_config.ini",True)
        print("")
        print("")
        quit()
    elif index == 1:
        helpers.stk_stable(config)
        main()

def main():
    libs.settings.init()
    os.chdir(libs.settings.orig_directory)
    setproctitle.setproctitle('ult_STK_launch')
    print("")
    print("")
    print("")
    print("")
    lala = os.system('echo "WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜" | lolcat ')
    lala = os.system('echo "" | cowsay -f hellokitty | lolcat')

    if lala != 0:
        print("You need to install" + style.color.BOLD + " cowsay " + style.color.END + "and" + style.color.BOLD + " lolcat " + style.color.END + "in order to get the welcome message displayed. So sorry!")

    print("")
    input("Press Enter to continue...")

    if (not(os.path.exists(libs.settings.orig_directory+"/magic_config.ini")) or os.stat(libs.settings.orig_directory+"/magic_config.ini").st_size == 0):
        initialize()

    style.output_title("Let's Go!", 1)
    print("")
    libs.settings.ustkl_config.read(libs.settings.orig_directory+"/magic_libs.settings.ustkl_config.ini")
    update.extra_files(libs.settings.assets_data)

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
            style.output_title(title, 2)
            style.prompt("Sorry, not any git installs found in config",True)
            print()
        main()
    elif index == 2:
        style.output_title("Profiles Tuning",2)
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
            helpers.stk_git(config)
        if sp_index == 1:
            helpers.stk_stable(config)
        if sp_index == 2:
            helpers.stk_git_kimden_client(config)
        if sp_index == 3:
            helpers.stk_git_kimden(config)
        if sp_index == 4:
            helpers.stk_git_kimden_server(config)
        if sp_index == 5:
            helpers.stk_speed(config)
        if sp_index == 6:
            helpers.stk2(config)
        main()
    elif index == 4:
        print()
        quit()






main()
