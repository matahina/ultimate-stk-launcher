#!/usr/bin/env python3

import subprocess
import os
import os.path
from os import path
from urllib import request
import time
from pathlib import Path


from pick import pick

import re

import inquirer

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
# Thanks https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console

def output_title(text, level):
    if level == 1:
        print(color.PURPLE + color.BOLD + text.upper() + color.END)
    if level == 2:
        print(color.CYAN + text.upper() + color.END)

def quest(text, important = False):
    if important:
        print(color.UNDERLINE + color.YELLOW + text + color.END)
    else:
        print(color.UNDERLINE + text + color.END)

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
config = ConfigParser() # assumed as global variable
# Thanks https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3

orig_directory = os.getcwd()

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

urls = [["powerup_orig", "normal", "https://raw.githubusercontent.com/supertuxkart/stk-code/1.3/data/powerup.xml"],
        ["kart_characteristics_orig", "normal", "https://raw.githubusercontent.com/supertuxkart/stk-code/1.3/data/kart_characteristics.xml"],
        ["powerup_random", "random (mimiz)", "https://stk.kimden.online/public/powerup_mimiz.xml"],
        ["powerup_rebalanced", "rebalanced (mimiz)", "https://stk.kimden.online/public/rebalanced.xml"],
        ["powerup_yeet", "YEET (Iluvatyr)", "https://stk.iluvatyr.com/download/powerup.xml"],
        ["kart_characteristics_yeet", "YEET (Iluvatyr)", "https://stk.iluvatyr.com/download/kart_characteristics.xml"],
        ["powerup_cake", "cake (matahina)", "https://framagit.org/hina-dev/stk-party/-/raw/main/powerup_cake.xml"],
        ["powerup_gums", "gums (matahina)", "https://framagit.org/hina-dev/stk-party/-/raw/main/powerup_gums.xml"],
        ["powerup_aprilfool", "April 1st (mimiz)", "https://stk.kimden.online/public/0104.xml"],
        ["emoji_used", "", "https://raw.githubusercontent.com/supertuxkart/stk-code/1.3/data/emoji_used.txt"]]
    
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
# Thanks https://stackoverflow.com/questions/8924173/how-to-print-bold-text-in-python


def clear_console():
    os.system('clear')
    
def update_extra_files():
    output_title("Downloading powerup files in "+os.path.expanduser('~')+"/.config/ustkl/",2)
    

    
    for key in urls:
        print("")
        quest(key[0])
        try:
            request.urlretrieve(key[2], os.path.expanduser('~')+"/.config/ustkl/"+key[0]+".xml")
        except:
            print(color.RED + "Could not retrieve " + key[2] + color.END)
        else:
            print("OK " + key[2])
    
    print("")
    
def edit_profile(number):
    nice_clue = config.get('Profile_'+number,'name')
    if nice_clue == 'NotThisName':
        
        output_title("This Profile", 2)
        print("")
        
        an_answer = input(color.UNDERLINE + "Pls give a name to this profile:" + color.END +" ")
        print("")
        config.set('Profile_'+number,'name',an_answer)
        
        quest("Now choose the bin file for STK")
        while True:
            an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE BIN STK FILE???'], stdout=subprocess.PIPE)
            if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                break
            else:
                print(color.RED + "Pls choose a file" + color.END)
        print(an_answer.stdout.decode('utf-8').replace("\n",""))
        print("")
        config.set('Profile_'+number,'bin_path',an_answer.stdout.decode('utf-8').replace("\n",""))
        
        quest("then the location of the DATA folder")
        while True:
            an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  Data  DIRECTORY???'], stdout=subprocess.PIPE)
            if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                break
            else:
                print(color.RED + "Pls choose a directory" + color.END)
        print(an_answer.stdout.decode('utf-8').replace("\n",""))
        print("")        
        config.set('Profile_'+number,'data_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
        
        
        title = "So, what kind of install is it (for this profile)?"
        options = ['distro-based (apt-get, rpm, pacman, emerge, whatever...)',
                    'from git (for the bold!)',
                    'from a tarball (so locally, no sudo required to change any file)'
                    ]
        option, index = pick(options, title)
        quest(title)
        print(option)
        print("") 
        
        if index == 0:
            config.set('Profile_'+number,'type',"sudo")
            
        elif index == 1:
            config.set('Profile_'+number,'type',"git")
            
            quest("Now choose the location of the GIT folder")
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  git  DIRECTORY???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a directory" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            print("")
            config.set('Profile_'+number,'git_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
            
            quest("then of the SVN folder")
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  svn  DIRECTORY???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a directory" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            print("")      
            config.set('Profile_'+number,'svn_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
            
        elif index == 2:
            config.set('Profile_'+number,'type',"from_tarball")
        
        config.add_section('General')
        config.set('General','emoji_file','')
        config.set('General','KDE_Openbox_stuff','')
        config.set('General','echoing_stdout','')
        
        title = "Do you have a particular emoji file?"
        options = ['Yeah',
                    'Nope'
                    ]
        option, index = pick(options, title)
        quest(title)
        print(option)
        print("") 
        
        if index == 0:
            quest("Now choose your emoji file for STK")
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE CUSTOM emoji_used.txt FILE???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a file" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            print("")
            config.set('General','emoji_file',an_answer.stdout.decode('utf-8').replace("\n",""))
        
        title = "Do you run under KDE Plasma and wanna switch temporarily to OpenBox when launching STK?"
        options = ['Yeah',
                    'Nope'
                    ]
        option, index = pick(options, title)
        quest(title)
        print(option)
        print("") 
        
        if index == 0:
            config.set('General','KDE_Openbox_stuff',"yes")
        
        title = "Do you have an existing file where you want to cat stdout.log?"
        options = ['Yeah',
                    'Nope'
                    ]
        option, index = pick(options, title)
        quest(title)
        print(option)
        print("") 
        
        if index == 0:
            quest("Now choose your output stdout file for STK")
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE CUSTOM output stdout FILE???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a file" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            print("")
            config.set('General','echoing_stdout',an_answer.stdout.decode('utf-8').replace("\n",""))
        
        title = "Do you have custom sfx files?"
        options = ['Yeah',
                    'Nope'
                    ]
        option, index = pick(options, title)
        quest(title)
        print(option)
        print("") 
        
        if index == 0:
            quest("Now choose your sfx files for STK")
            quest("only choose files with exact names", True)
            quest("those files have to be stored in proper directory (sfx, gfx, models, etc.)", True)
            quest("Then you select the directory in which these subdirectories are".upper(), True)
            while True:
                an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE THE CUSTOM sfx FILES???'], stdout=subprocess.PIPE)
                if (an_answer.stdout.decode('utf-8').replace("\n","") != ""):
                    break
                else:
                    print(color.RED + "Pls choose a directory" + color.END)
            print(an_answer.stdout.decode('utf-8').replace("\n",""))
            config.set('General','sfx_files',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
            
            filelist = []
            path = config.get("General", 'sfx_files')
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    #append the file name to the list
                    filelist.append(os.path.join(root,file).replace(path,""))

            #print all the file names
            
            print("Saving back original files for this profile")
            print("")  
            Path(os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(number)).mkdir(parents=True, exist_ok=True)
            for name in filelist:
                
                if ( (config.get("Profile_"+str(number), 'svn_path') != "") and (name[0:name.find("/",1)].replace("/","") in issvn) ):
                    os.chdir(config.get("Profile_"+str(number), 'svn_path'))
                    os.system("cp --parents "+name+" "+os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(number)+"/")
                else:
                    os.chdir(config.get("Profile_"+str(number), 'data_path'))
                    os.system("cp --parents "+name+" "+os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(number)+"/")
            
        
        with open(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini", 'w') as configfile:
            config.write(configfile)
            
        output_title("Profile Updated!", 2)
        print("")
        input("Press Enter to continue...")
        cls()
        #update_extra_files()
        

def initialize():
    output_title("Config is being created...", 1)
    print("")
    
    Path(os.path.expanduser('~')+"/.config/ustkl/").mkdir(parents=True, exist_ok=True)
    
    f = open(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini", 'w')
    f.close()
    config.read(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")
    config.add_section('Profile_1')
    config.set('Profile_1','name','NotThisName')
    edit_profile("1")


def stk_update():
    title = "Which profile do you want to revert today?"
    options = config.sections()
    options.remove("General")
    idx = []
    for i,prof in enumerate(options):
        if config.get(prof, 'type') == "git":
            idx.append(i)
    if idx != []:
        plist = [options[i] for i in idx]
        names = []
        for name in plist:
            names.append(config.get(name, 'name'))
        option, index = pick(names, title)
        output_title(title, 2)
        print(option)
        print("")     
        profile_answer = plist[index]
        
        quest("Updating "+profile_answer + " " + config.get(profile_answer, 'name'))
        
        print("Updating SVN")
        print("")    
        os.chdir(config.get(profile_answer, 'svn_path'))
        os.system("svn up")     
        
        print("Updating GIT")
        print("")    
        os.chdir(config.get(profile_answer, 'git_path'))
        os.system("git pull")
        
        print("Building GIT")
        print("")    
        os.chdir(config.get(profile_answer, 'git_path')+"cmake_build")
        os.system("cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo")
        os.system("make -j10")
        
        print()
    else:
        output_title(title, 2)
        quest("Sorry, not any git installs found in config",True)
        print()
                    

def stk_revert():
    
    title = "Which profile do you want to revert today?"
    plist = config.sections()
    plist.remove("General")
    names = []
    for name in plist:
        names.append(config.get(name, 'name'))
    option, index = pick(names, title)
    output_title(title, 2)
    print(option)
    print("")     
    profile_answer = plist[index]
    
    prefix = ""
    if config.get(profile_answer,"type") == "sudo":
        prefix = "sudo "
    if config.get(profile_answer,"type") == "git":
        os.chdir(config.get(profile_answer, 'git_path'))
        os.system(prefix+"git clean -f")
    if config.get(profile_answer,'svn_path') != "":
        os.chdir(config.get(profile_answer, 'svn_path'))
        os.system(prefix+"svn revert --recursive .")
        
    the_path = os.path.expanduser('~')+"/.config/ustkl/"+profile_answer+"/"
    
    filelist = []  
    for root, dirs, files in os.walk(the_path):
        for file in files:
            #append the file name to the list
            filelist.append(os.path.join(root,file).replace(the_path,""))

    #print all the file names
    os.chdir(the_path)
    for name in filelist:
        if ( (config.get(profile_answer, 'svn_path') != "") and (name[0:name.find("/",1)].replace("/","") in issvn) ):
            os.system(prefix+" cp --parents "+name+" "+config.get(profile_answer, 'svn_path'))
        else:
            os.system(prefix+" cp --parents "+name+" "+config.get(profile_answer, 'data_path'))
            
        
        

def goo():
    powerups = [row[1] for row in urls]

    for i, filename in enumerate([row[0] for row in urls]):
        if not(os.path.exists(os.path.expanduser('~')+"/.config/ustkl/"+filename+".xml")):
            powerups[i] == ""
            if (i==1 or i==3):
                powerups[i+1] == ""
            if (i==2 or i==4):
                powerups[i-1] == ""

    initial = [x for x in powerups if x]

    title = "Which powerup file do you want to use today?"
    options = sorted(set(initial), key=initial.index)
    option, index = pick(options, title)
    output_title(title, 2)
    print(option)
    print("")     
    powerup_answer = option

            
    title = "Which profile do you want to use today?"
    plist = config.sections()
    plist.remove("General")
    names = []
    for name in plist:
        names.append(config.get(name, 'name'))
    option, index = pick(names, title)
    output_title(title, 2)
    print(option)
    print("")     
    profile_answer = plist[index]
    
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
    option, index = pick(options, title)
    output_title(title, 2)
    print(option)
    print("")     
    
    suffix = ""
    if index == "1":
        suffix = " --check-debug "
    if index == "2":
        suffix = " --track-debug "
    if index == "3":
        suffix = " --check-debug --track-debug "
    
    output_title("Am gonna make your dreams come true...", 2)
    print("")
    
    if config.get("General","kde_openbox_stuff") == "yes":
        quest("KDE STUFF")
        os.system("kquitapp5 plasmashell &>/dev/null")
        os.system("openbox --replace &>/dev/null")
        print("")
        
    if config.get(profile_answer,"type") == "git":
        quest("Cleaning GIT")
        os.chdir(config.get(profile_answer, 'git_path'))
        os.system("git clean -f")
        print("")
    
    if config.get("General", 'emoji_file') != "":
        quest("Using the choosen emoji_used file")
        os.chdir(config.get(profile_answer, 'data_path'))
        os.system(prefix+"rm emoji_used.txt")
        os.system(prefix+"cp "+config.get("General", 'emoji_file')+" emoji_used.txt")
        print("")
    
    if config.get(profile_answer, 'svn_path') != "":
        quest("Cleaning SVN")
        os.chdir(config.get(profile_answer, 'svn_path'))
        os.system("svn revert --recursive .")
        print("")
    
    if config.get("General", 'sfx_files') != "":
        quest("Replacing SFX/GFX files")
        os.chdir(config.get("General", 'sfx_files'))
    
        filelist = []
        
        path = config.get("General", 'sfx_files')
        
        for root, dirs, files in os.walk(config.get("General", 'sfx_files')):
            for file in files:
                #append the file name to the list
                filelist.append(os.path.join(root,file).replace(path,""))

        #print all the file names
        for name in filelist:
            if ( (config.get(profile_answer, 'svn_path') != "") and (name[0:name.find("/",1)].replace("/","") in issvn) ):
                os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'svn_path'))
            else:
                os.system(prefix+"cp --parents "+name+" "+config.get(profile_answer, 'data_path'))
        
        print("")
            
        
    powerups.index(powerup_answer)

    quest("Using the choosen powerup file")
    pfile = urls[powerups.index(powerup_answer)][0]+".xml"
    if powerups.index(powerup_answer) == 2:
        kfile = urls[powerups.index(powerup_answer)+1][0]+".xml"
    else:
        kfile="kart_characteristics_orig.xml"
    
    os.chdir(config.get(profile_answer, 'data_path'))
    
    print(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+pfile+" powerup.xml")
    os.system(prefix+"rm powerup.xml")
    os.system(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+pfile+" powerup.xml")
    
    print(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+kfile+" kart_characteristics.xml")
    os.system(prefix+"rm kart_characteristics.xml")
    os.system(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+kfile+" kart_characteristics.xml")
    
    print("")
    
    os.chdir(os.path.dirname( config.get(profile_answer, 'bin_path')  ))
    suffixbis = ""
    if config.get("General", 'echoing_stdout') != "":
        suffixbis = " | tee -a "+config.get("General", 'echoing_stdout')
    
    quest("running")
    print("chdir "+ os.path.dirname( config.get(profile_answer, 'bin_path')  ))
    print("."+config.get(profile_answer, 'bin_path').replace(os.path.dirname( config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
    os.system("."+config.get(profile_answer, 'bin_path').replace(os.path.dirname( config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
    print("")
    
    if config.get("General","kde_openbox_stuff") == "yes":
        quest("KDE STUFF")
        os.system("kstart5 plasmashell &>/dev/null")
        os.system("kwin --replace &>/dev/null")
        print("")
    
    
    
    
def main():
    

    lala = os.system('cowsay -f unipony-smaller  "WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜" | lolcat')
    
    if lala != 0:
        print("You need to install" + color.BOLD + "cowsay" + color.END + "and" + color.BOLD + "lolcat" + color.END + "in order to get the welcome message displayed. So sorry!")
    
    print("")
    input("Press Enter to continue...")
    cls()
    
    if (not(path.exists(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")) or os.stat("/home/petite_fleur/.config/ustkl/magic_config.ini").st_size == 0):
        initialize()
        
    output_title("Let's Go!", 1)
    print("")
    config.read(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")
    update_extra_files()
    
    
    title = "What do you want to do today?".upper()
    options = ['STÖÖÖÖRT STK',
                'Update STK from git and svn',
                'Revert all changes made to git and svn (emoji file, sfx files, etc.)',
                'Tweak your profiles'
                ]
    option, index = pick(options, title)
    output_title(title, 2)
    print(option)
    print("") 
        
    if index == 0:
        goo()
    elif index == 1:
        stk_update()
    elif index == 2:
        stk_revert()
    elif index == 3:
        output_title("Profiles Tuning",2)
        quest("not implemented yet",True)
        quest("At the moment, have fun at: "+os.path.expanduser('~')+"/.config/ustkl/magic_config.ini",True)
        print("")



clear_console()
main()
