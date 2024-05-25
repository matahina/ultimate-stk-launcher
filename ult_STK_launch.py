#!/usr/bin/env python3

import subprocess
import os
orig_directory = os.getcwd()
import time
from pathlib import Path
import datetime
import setproctitle
import questionary
from configparser import ConfigParser
import csv
import pandas as pd
import sys
sys.path.append(orig_directory+"/libs")
import update as update
import style as style
import helpers as helpers

config = ConfigParser()

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

assets_data = pd.read_csv('libs/sources.csv')
assets_data = assets_data.fillna("")

started_at = datetime.datetime.now()
echo_file = started_at.strftime("%Y%m%d_%H%M%S")


def goo():
    title = "Which profile do you want to use today?"
    plist = config.sections()
    names = []
    for name in plist:
        names.append(config.get(name, 'name'))
    option = questionary.select(title, names).ask()
    index = names.index(option)
    print("")
    profile_answer = plist[index]



    p_up_list = list(dict.fromkeys(assets_data["id"]))
    p_up_list.remove("")

    if config.get(profile_answer, 'type') == "git2":
        p_up_list = ["STK2"]
    else:
        p_up_list.remove("STK2")
    title = "Which powerup file do you want to use today?"
    option = questionary.select(title, p_up_list).ask()
    index = p_up_list.index(option)
    print("")
    powerup_answer = option

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

    style.prompt("Replacing SFX/GFX/data files")
    os.chdir(orig_directory+"/my_files/")

    filelist = []
    revert_list = []

    path = orig_directory+"/my_files/"

    for root, dirs, files in os.walk(orig_directory+"/my_files/"):
        for file in files:
            filelist.append(os.path.join(root,file).replace(path,""))

    filelist.remove(".placeholder")

    for name in filelist:
        if 'svn_path' in [row[0] for row in config.items(profile_answer)]:
            if ( (name[0:name.find("/",1)].replace("/","") in issvn) ):
                os.system(prefix+"mv "+config.get(profile_answer, 'svn_path')+name+" "+config.get(profile_answer, 'svn_path')+name+"_old")
                revert_list.append(prefix+"rm "+" "+config.get(profile_answer, 'svn_path')+name)
                revert_list.append(prefix+"mv "+config.get(profile_answer, 'svn_path')+name+"_old"+" "+config.get(profile_answer, 'svn_path')+name)
                os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'svn_path'))
            else:
                os.system(prefix+"mv "+config.get(profile_answer, 'data_path')+name+" "+config.get(profile_answer, 'data_path')+name+"_old")
                revert_list.append(prefix+"rm "+" "+config.get(profile_answer, 'data_path')+name)
                revert_list.append(prefix+"mv "+config.get(profile_answer, 'data_path')+name+"_old"+" "+config.get(profile_answer, 'data_path')+name)
                os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'data_path'))
        else:
            os.system(prefix+"mv "+config.get(profile_answer, 'data_path')+name+" "+config.get(profile_answer, 'data_path')+name+"_old")
            revert_list.append(prefix+"rm "+" "+config.get(profile_answer, 'data_path')+name)
            revert_list.append(prefix+"mv "+config.get(profile_answer, 'data_path')+name+"_old"+" "+config.get(profile_answer, 'data_path')+name)
            os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'data_path'))

    print("")


    style.prompt("Using the choosen powerup file")
    p_up_file_name = list(assets_data['name'].where(assets_data['id'] == powerup_answer).where(assets_data['type'] == "powerup").dropna())
    pfile = p_up_file_name[0]+".xml"
    kart_file_name = list(assets_data['name'].where(assets_data['id'] == powerup_answer).where(assets_data['type'] == "kart").dropna())
    if kart_file_name == []:
        kfile="kart_characteristics_orig.xml"
    else:
        kfile = kart_file_name[0]+".xml"

    os.chdir(config.get(profile_answer, 'data_path'))

    print(prefix+"cp "+orig_directory+"/tmp_files/"+pfile+" powerup.xml")
    os.system(prefix+"mv powerup.xml powerup.xml_old")
    os.system(prefix+"cp "+orig_directory+"/tmp_files/"+pfile+" powerup.xml")

    print(prefix+"cp "+orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml")
    os.system(prefix+"mv kart_characteristics.xml kart_characteristics.xml_old")
    os.system(prefix+"cp "+orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml")

    print("")

    os.chdir(os.path.dirname( config.get(profile_answer, 'bin_path')  ))
    suffixbis = " | tee -a "+orig_directory+"/logs/"+echo_file+".log"

    style.prompt("running")
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


    style.prompt("Reverting SFX/GFX/data files")
    os.chdir(orig_directory+"/my_files/")

    for cmd in revert_list:
        os.system(cmd)

    os.chdir(config.get(profile_answer, 'data_path'))

    os.system(prefix+"mv powerup.xml_old powerup.xml")
    os.system(prefix+"mv kart_characteristics.xml_old kart_characteristics.xml")

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
        style.prompt("Have fun at: "+orig_directory+"/magic_config.ini",True)
        print("")
        print("")
        quit()
    elif index == 1:
        helpers.stk_stable(config)
        main()

def main():
    os.chdir(orig_directory)
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

    if (not(os.path.exists(orig_directory+"/magic_config.ini")) or os.stat(orig_directory+"/magic_config.ini").st_size == 0):
        initialize()

    style.output_title("Let's Go!", 1)
    print("")
    config.read(orig_directory+"/magic_config.ini")
    update.extra_files(assets_data)
    update.addons()
    os.chdir(orig_directory)


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
        options = config.sections()
        # options.remove("General")
        idx = []
        for i,prof in enumerate(options):
            if config.get(prof, 'type') == "git" or config.get(prof, 'type') == "git2" or config.get(prof, 'type') == "git-kimden" or config.get(prof, 'type') == "git-kimden-server" :
                idx.append(i)

        if idx != []:
            plist = [options[i] for i in idx]
            names = []
            for name in plist:
                names.append(config.get(name, 'name'))
            option = questionary.select(title, options).ask()
            index = options.index(option)
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
        style.prompt("Have fun at: "+orig_directory+"/magic_config.ini",True)
        print("")
        print("")
    elif index == 3:
        title = "Which version?".upper()
        options = ['STK GIT (master)',
                   'STK STABLE (1.4)',
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
            helpers.stk_git_kimden(config)
        if sp_index == 3:
            helpers.stk_git_kimden_server(config)
        if sp_index == 4:
            helpers.stk_speed(config)
        if sp_index == 5:
            helpers.stk2(config)
        main()
    elif index == 4:
        print()
        quit()






main()
