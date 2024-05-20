import os
import datetime
import style as style
from configparser import ConfigParser

def stk_speed(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_SPEED_"+started_at.strftime("%Y%m%d_%H%M%S")

    orig_directory = os.getcwd()
    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+orig_directory+"/libs/install_stk_speed.sh "+the_path + " | tee -a " + orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK speed')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-speed/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-speed/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git_speed")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-speed/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)

def stk2(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_2_"+started_at.strftime("%Y%m%d_%H%M%S")

    orig_directory = os.getcwd()
    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+orig_directory+"/libs/install_stk2.sh "+the_path + " | tee -a " + orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK 2')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"alayan/stk-code-alayan/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"alayan/stk-code-alayan/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git2")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"alayan/stk-code-alayan/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"alayan/stk-assets/")
    with open(orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)


def stk_git(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_"+started_at.strftime("%Y%m%d_%H%M%S")

    orig_directory = os.getcwd()
    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+orig_directory+"/libs/install_stk.sh "+the_path + " | tee -a " + orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git2")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)
