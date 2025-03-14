import os
import datetime
import libs.style_cli as style
from configparser import ConfigParser
import libs.settings

def stk_speed(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_SPEED_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk_speed.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK speed')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-speed/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-speed/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git_speed")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-speed/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)

def stk2(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_2_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk2.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK 2')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-2/stk-code-alayan/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-2/stk-code-alayan/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git2")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-2/stk-code-alayan/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-2/stk-assets/")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)


def stk_git(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_MASTER_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)



def stk_stable(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_STABLE_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk_stable.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK Stable')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"SuperTuxKart-1.4-linux-x86_64/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"SuperTuxKart-1.4-linux-x86_64/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "stable")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)




def stk_git_kimden(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_KIMDEN_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk_kimden.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)




def stk_git_kimden_client(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_KIMDEN_CLIENT_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk_kimden_client.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN CLIENT')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden-client/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden-client/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden-client/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)




def stk_git_kimden_server(config):
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_KIMDEN_SERVER_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    title = "Where to clone repos? [Give absolute path of the directory to exec git clone]"
    style.output_title(title, 1)
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.settings.orig_directory+"/libs/install_stk_kimden_server.sh "+the_path + " | tee -a " + libs.settings.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+uecho_file+".log")


    config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN SERVER')
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden-server/cmake_build/bin/supertuxkart")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden-server/data/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden-server/")
    config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    with open(libs.settings.orig_directory+"/magic_config.ini", 'w') as configfile:
        config.write(configfile)
