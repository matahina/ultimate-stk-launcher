#!/usr/bin/env python3

import subprocess
import os
import os.path
from os import path
from urllib import request

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
config = ConfigParser() # assumed as global variable
# Thanks https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3

orig_directory = os.getcwd()

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
    print(color.BOLD + color.RED + color.UNDERLINE + "Downloading powerup files in "+os.path.expanduser('~')+"/.config/ustkl/" + color.END)
    response = request.urlretrieve("https://raw.githubusercontent.com/supertuxkart/stk-code/1.3/data/powerup.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_orig.xml")
    response = request.urlretrieve("https://raw.githubusercontent.com/supertuxkart/stk-code/1.3/data/kart_characteristics.xml", os.path.expanduser('~')+"/.config/ustkl/"+"kart_characteristics_orig.xml")
    response = request.urlretrieve("https://stk.iluvatyr.com/download/powerup.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_yeet.xml")
    response = request.urlretrieve("https://stk.iluvatyr.com/download/kart_characteristics.xml", os.path.expanduser('~')+"/.config/ustkl/"+"kart_characteristics_yeet.xml")
    response = request.urlretrieve("https://framagit.org/hina-dev/stk-party/-/raw/main/powerup_cake.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_cake.xml")
    response = request.urlretrieve("https://framagit.org/hina-dev/stk-party/-/raw/main/powerup_gums.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_gums.xml")
    response = request.urlretrieve("https://stk.kimden.online/public/powerup_mimiz.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_random.xml")
    response = request.urlretrieve("https://stk.kimden.online/public/rebalanced.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_rebalanced.xml")
    response = request.urlretrieve("https://stk.kimden.online/public/0104.xml", os.path.expanduser('~')+"/.config/ustkl/"+"powerup_aprilfool.xml")
    response = request.urlretrieve("https://raw.githubusercontent.com/supertuxkart/stk-code/1.3/data/emoji_used.txt", os.path.expanduser('~')+"/.config/ustkl/"+"emoji_used.txt")
    
def edit_profile(number):
    nice_clue = config.get('Profile_'+number,'name')
    if nice_clue == 'NotThisName':
        an_answer = input(color.CYAN + "Pls give a name to this profile: " + color.END)
        config.set('Profile_'+number,'name',an_answer)
        print("")
        print("Now choose the bin file for STK, then the location of the DATA folder")
        an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE BIN STK FILE???'], stdout=subprocess.PIPE)
        config.set('Profile_'+number,'bin_path',an_answer.stdout.decode('utf-8').replace("\n",""))
        an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  Data  DIRECTORY???'], stdout=subprocess.PIPE)
        config.set('Profile_'+number,'data_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
        an_answer = ""
        i = 0
        while (an_answer not in ["1", "2", "3"]): 
            print("")
            print(color.BLUE + color.BOLD + "So, what kind of install is it (for this profile)?" + color.END)
            print("")
            print("1) distro-based (apt-get, rpm, pacman, emerge, whatever...)")
            print("2) from git (for the bold!)")
            print("3) from a tarball (so locally, no sudo required to change any file)")
            print("")
            if i == 0:
                an_answer = input("Pls tell me: ")
            else:
                an_answer = input(color.BOLD + "Pls tell me SERIOUSLY: " + color.END)
            i+=1
            
        if an_answer == "1":
            config.set('Profile_'+number,'type',"sudo")
        elif an_answer == "2":
            config.set('Profile_'+number,'type',"git")
            an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  git  DIRECTORY???'], stdout=subprocess.PIPE)
            config.set('Profile_'+number,'git_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
            an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE IS THE  svn  DIRECTORY???'], stdout=subprocess.PIPE)
            config.set('Profile_'+number,'svn_path',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
        elif an_answer == "3":
            config.set('Profile_'+number,'type',"from_tarball")
        
        config.add_section('General')
        config.set('General','emoji_file','')
        config.set('General','KDE_Openbox_stuff','')
        config.set('General','echoing_stdout','')
        
        print()
        an_answer = input(color.BOLD + "Do you have a particular emoji file? [y/N] " + color.END)
        
        if an_answer == "y":
            an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE CUSTOM emoji_used.txt FILE???'], stdout=subprocess.PIPE)
            config.set('General','emoji_file',an_answer.stdout.decode('utf-8').replace("\n",""))
        
        print()
        an_answer = input(color.BOLD + "Do you run under KDE Plasma and wanna switch temporarily to OpenBox when launching STK? [y/N] " + color.END)
        
        if an_answer == "y":
            config.set('General','KDE_Openbox_stuff',"yes")
        
        print()
        an_answer = input(color.BOLD + "Do you have an existing file where you want to cat stdout.log? [y/N] " + color.END)
        
        if an_answer == "y":
            an_answer = subprocess.run(['zenity', '--file-selection', '--title=WHERE IS THE CUSTOM output stdout FILE???'], stdout=subprocess.PIPE)
            config.set('General','echoing_stdout',an_answer.stdout.decode('utf-8').replace("\n",""))
        
        print()
        an_answer = input(color.BOLD + "Do you have custom sfx files? (very optional, only choose files with exact name and not already in sfx directory) [y/N] " + color.END)
        if (an_answer == "y"):
            an_answer = subprocess.run(['zenity', '--file-selection', '--directory', '--title=WHERE THE CUSTOM sfx FILES???'], stdout=subprocess.PIPE)
            config.set('General','sfx_files',an_answer.stdout.decode('utf-8').replace("\n","")+"/")
            
            filelist = []
            path = config.get("General", 'sfx_files')
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    #append the file name to the list
                    filelist.append(os.path.join(root,file).replace(path,""))

            #print all the file names
            for name in filelist:
                os.mkdir(os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(number))
                if (config.get("Profile_"+str(number), 'svn_path') != ""):
                    os.chdir(config.get("Profile_"+str(number), 'svn_path'))
                    os.system("cp --parents "+name+" "+os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(number)+"/")
                else:
                    os.chdir(config.get("Profile_"+str(number), 'data_path'))
                    os.system("cp --parents "+name+" "+os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(number)+"/")
            
        
        with open(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini", 'w') as configfile:
            config.write(configfile)
            
        update_extra_files()
        

def initialize():
    print("Config is being created...")
    print("")
    os.mkdir(os.path.expanduser('~')+"/.config/ustkl/")
    f = open(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini", 'x')
    f.close()
    config.read(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")
    config.add_section('Profile_1')
    config.set('Profile_1','name','NotThisName')
    edit_profile("1")


def stk_update():
    matching = [s for s in config.sections() if "Profile_" in s]
    real_matching = []
    for p in matching:
        if config.get(p, 'type') == "git":
            real_matching.append(p)
    if real_matching == []:
        print()
        print("Sorry, not any git installs found in config")
        print()
    else:
        print()
        print(color.BOLD + color.CYAN + "Which one do you want to upgrade today?".upper() + color.END)
        print()
        i=0
        for elem in real_matching:
            i+=1
            print(str(i)+") "+elem+ " " + config.get(elem, 'name'))
        print("")
        key_answer = input("Pls tell me: ")
        print("")
        if (int(key_answer) -1) < 0 or (int(key_answer)) > len(real_matching):
            print(color.BOLD + color.RED + color.UNDERLINE + "ERROR BACK TO MAIN MENU BRRRRRR" + color.END)
        else:
            print(color.BOLD + color.RED + color.UNDERLINE + "Updating "+real_matching[(int(key_answer) -1)] + " " + config.get(real_matching[(int(key_answer) -1)], 'name') + color.END)
            os.chdir(config.get(real_matching[(int(key_answer) -1)], 'svn_path'))
            print(color.RED + "UPDATING SVN" + color.END)
            os.system("svn up")
            base = dict(config.items("General"))
            os.chdir(config.get(real_matching[(int(key_answer) -1)], 'git_path'))
            print(color.RED + "UPDATING GIT" + color.END)
            os.system("git pull")
            print(color.RED + "BUILDING GIT" + color.END)
            os.chdir(config.get(real_matching[(int(key_answer) -1)], 'git_path')+"cmake_build")
            os.system("cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo")
            os.system("make -j10")
                    

def goo():
    key_answer = ""
    print("")
    if key_answer == "":
        print(color.BOLD + color.CYAN + "Which powerup file do you want to use today?".upper() + color.END)
    else:
        print(color.BOLD + color.RED + color.UNDERLINE + "HEY SERIOUSLY CHOOSE ONE OF THESE OPTIONS AND NOTHING ELSE BRRRRRR" + color.END)
    print("")
    print("1) Normal")
    print("2) Random (mimiz)")
    print("3) Rebalanced (mimiz)")
    print("4) Cake (matahina)")
    print("5) Gums (matahina)")
    print("6) YEET (Iluvatyr)")
    print("7) April 1st (mimiz)")
    print("")
    super_key_answer = input("Pls tell me: ")
    
    if super_key_answer not in ["1","2","3","4","5","6","7"]:
        goo()
        
    print("")
    print(color.BOLD + color.CYAN + "Which profile do you want to use today?".upper() + color.END)
    print("(default: 1)")
    print("")
    
    i=0
    for elem in config.sections():
        if elem != "General":
            i+=1
            print(str(i)+") "+elem+ " " + config.get(elem, 'name'))
    print("")
    key_answer = input("Pls tell me: ")
    print("")
    
    if (int(key_answer) < 1) or (int(key_answer) > len(config.sections())):
        key_answer = "1"
    
    prefix = ""
    if config.get("Profile_"+str(key_answer),"type") == "sudo":
        prefix = "sudo "
    
    print("")
    print(color.BOLD + color.CYAN + "Do you wanna debüg today?".upper() + color.END)
    print("")
    print("1) NÖ (default)")
    print("2) Checklines")
    print("3) Drivelines")
    print("4) CHecklines AND Drivelines")
    print("")
    new_key_answer = input("Pls tell me: ")
    
    suffix = ""
    if new_key_answer == "2":
        suffix = " --check-debug "
    if new_key_answer == "3":
        suffix = " --track-debug "
    if new_key_answer == "4":
        suffix = " --check-debug --track-debug "
        
    if config.get("General","kde_openbox_stuff") == "yes":
        print("KDE STUFF")
        os.system("killall -9 plasmashell &>/dev/null")
        os.system("openbox --replace &>/dev/null")
    
    if config.get("Profile_"+str(key_answer),"type") == "git":
        os.chdir(config.get("Profile_"+str(key_answer), 'git_path'))
        os.system("git clean -f")
    
    if config.get("General", 'emoji_file') != "":
        print("Using the choosen emoji_used file")
        os.chdir(config.get("Profile_"+str(key_answer), 'data_path'))
        os.system(prefix+"rm emoji_used.txt")
        os.system(prefix+"cp "+config.get("General", 'emoji_file')+" emoji_used.txt")
    
    if config.get("Profile_"+str(key_answer), 'svn_path') != "":
        os.chdir(config.get("Profile_"+str(key_answer), 'svn_path'))
        os.system("svn revert --recursive .")
    
    if config.get("General", 'sfx_files') != "":
        os.chdir(config.get("General", 'sfx_files'))
        the_path = config.get("Profile_"+str(key_answer), 'data_path')
        if config.get("Profile_"+str(key_answer), 'svn_path') != "":
            the_path = config.get("Profile_"+str(key_answer), 'svn_path')
        os.system(prefix+"cp -R * "+the_path)
            
        
    
    print("Using the choosen powerup file")
    kfile="kart_characteristics_orig.xml"
    if super_key_answer == "1":
        pfile = "powerup_orig.xml"
    if super_key_answer == "2":
        pfile = "powerup_random.xml"
    if super_key_answer == "3":
        pfile = "powerup_rebalanced.xml"
    if super_key_answer == "4":
        pfile = "powerup_cake.xml"
    if super_key_answer == "5":
        pfile = "powerup_gums.xml"
    if super_key_answer == "6":
        pfile = "powerup_yeet.xml"
        kfile = "kart_characteristics_yeet.xml"
    if super_key_answer == "7":
        pfile = "powerup_aprilfool.xml"
    print("Using the choosen powerup file")
    os.chdir(config.get("Profile_"+str(key_answer), 'data_path'))
    print(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+pfile+" powerup.xml")
    os.system(prefix+"rm powerup.xml")
    os.system(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+pfile+" powerup.xml")
    os.system(prefix+"rm kart_characteristics.xml")
    os.system(prefix+"cp "+os.path.expanduser('~')+"/.config/ustkl/"+kfile+" kart_characteristics.xml")
    
    os.chdir(os.path.dirname( config.get("Profile_"+str(key_answer), 'bin_path')  ))
    suffixbis = ""
    if config.get("General", 'echoing_stdout') != "":
        suffixbis = " | tee -a "+config.get("General", 'echoing_stdout')
    os.system("."+config.get("Profile_"+str(key_answer), 'bin_path').replace(os.path.dirname( config.get("Profile_"+str(key_answer), 'bin_path')  ),'') + suffix + suffixbis)
    
    if config.get("General","kde_openbox_stuff") == "yes":
        print("KDE STUFF")
        os.system("kstart5 plasmashell &>/dev/null")
        os.system("kwin --replace &>/dev/null")
    
    
    
    
    
def main(key_answer):
    if not(path.exists(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")):
        initialize()
    config.read(os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")
    update_extra_files()
    print("")
    if key_answer == "":
        print(color.BOLD + color.CYAN + "What do you want to do today?".upper() + color.END)
    else:
        print(color.BOLD + color.RED + color.UNDERLINE + "HEY SERIOUSLY CHOOSE ONE OF THESE OPTIONS AND NOTHING ELSE BRRRRRR" + color.END)
    print("")
    print("1) Update STK from git and svn")
    print("2) Tweak your profiles")
    print("3) STÖÖÖÖRT STK")
    print("4) Revert all changes made to git and svn (emoji file, sfx files, etc.)")
    print("")
    key_answer = input("Pls tell me: ")
    
    if key_answer == "1":
        stk_update()
    elif key_answer == "2":
        print("not implemented yet")
        print("At the moment, have fun at: "+os.path.expanduser('~')+"/.config/ustkl/magic_config.ini")
    elif key_answer == "3":
        goo()
    elif key_answer == "4":
        print("")
        print(color.BOLD + color.CYAN + "Which profile do you want to clear today?".upper() + color.END)
        print("(default: 1)")
        print("")
        
        i=0
        for elem in config.sections():
            if elem != "General":
                i+=1
                print(str(i)+") "+elem+ " " + config.get(elem, 'name'))
        print("")
        key_answer = input("Pls tell me: ")
        print("")
        
        if (int(key_answer) < 1) or (int(key_answer) > len(config.sections())):
            key_answer = "1"
        
        prefix = ""
        if config.get("Profile_"+str(key_answer),"type") == "sudo":
            prefix = "sudo "
        os.chdir(config.get("Profile_"+str(key_answer), 'git_path'))
        os.system(prefix+"git clean -f")
        if config.get("Profile_"+str(key_answer),'svn_path') != "":
            os.chdir(config.get("Profile_"+str(key_answer), 'svn_path'))
            os.system(prefix+"svn revert --recursive .")
            
        filelist = []
        the_path = os.path.expanduser('~')+"/.config/ustkl/"+"Profile_"+str(key_answer)
        
        for root, dirs, files in os.walk(the_path):
            for file in files:
                #append the file name to the list
                filelist.append(os.path.join(root,file).replace(the_path,""))

        #print all the file names
        for name in filelist:
            os.chdir(the_path)
            os.system(prefix+" cp --parents "+name+" "+config.get("Profile_"+str(key_answer), 'data_path'))
            os.system(prefix+" cp --parents "+name+" "+config.get("Profile_"+str(key_answer), 'svn_path'))
    else:
        main(key_answer)


clear_console()
main("")
