# -*- coding: utf-8 -*-

# For building/updating profiles

import os
import datetime
import libs.common
import libs.variables

def stk_speed():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_SPEED_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk_speed.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK speed')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-speed/cmake_build/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-speed/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git_speed")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-speed/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    libs.common.save_config()

def stk2():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_2_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk2.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK 2')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-2/stk-code-alayan/cmake_build/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-2/stk-code-alayan/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git2")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-2/stk-code-alayan/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-2/stk-assets/")
    libs.common.save_config()


def stk_git():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_MASTER_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code/cmake_build/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    libs.common.save_config()



def stk_stable():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_STABLE_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk_stable.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK Stable')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"SuperTuxKart-1.4-linux-x86_64/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"SuperTuxKart-1.4-linux-x86_64/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "stable")
    libs.common.save_config()




def stk_git_kimden():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_KIMDEN_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk_kimden.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden/cmake_build/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    libs.common.save_config()




def stk_git_kimden_client():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_KIMDEN_CLIENT_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk_kimden_client.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN CLIENT')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden-client/cmake_build/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden-client/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden-client/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    libs.common.save_config()




def stk_git_kimden_server():
    started_at = datetime.datetime.now()
    uecho_file = "INSTALL_STK_GIT_KIMDEN_SERVER_"+started_at.strftime("%Y%m%d_%H%M%S")


    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    libs.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
    the_path = ""
    the_path = input('')
    if the_path[-1] != "/":
        the_path = the_path + "/"
    os.system("sh "+libs.variables.orig_directory+"/libs/install_stk_kimden_server.sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")


    libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN SERVER')
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden-server/cmake_build/bin/supertuxkart")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden-server/data/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden-server/")
    libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
    libs.common.save_config()
