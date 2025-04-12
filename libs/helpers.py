# -*- coding: utf-8 -*-

# For building/updating profiles

import os
import datetime
import libs.common
import libs.variables

def manage_profile(the_type,profile_answer=""):
    started_at = datetime.datetime.now()
    x = "update_" if the_type == "update" else "install_"

    uecho_file = x.upper() + the_type.upper() + "_"+profile_answer+"_"+started_at.strftime("%Y%m%d_%H%M%S")

    os.system("echo '========================  '"+uecho_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")

    if the_type == "update":
        libs.cli.cli.message(["## Updating "+profile_answer + " " + libs.variables.ustkl_config.get(profile_answer, 'name')])
        if libs.variables.ustkl_config.get(profile_answer, 'type') == "git2":
            os.system("sh "+libs.variables.orig_directory+"/libs/recipes/update_stk_git2.sh "+libs.variables.ustkl_config.get(profile_answer, 'svn_path')+ " " +libs.variables.ustkl_config.get(profile_answer, 'git_path')+ " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
        elif libs.variables.ustkl_config.get(profile_answer, 'type') == "git-kimden-server":
            os.system("sh "+libs.variables.orig_directory+"/libs/recipes/update_stk_kimden_server.sh "+libs.variables.ustkl_config.get(profile_answer, 'svn_path')+ " " +libs.variables.ustkl_config.get(profile_answer, 'git_path')+ " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
        else:
            os.system("sh "+libs.variables.orig_directory+"/libs/recipes/update_stk_git.sh "+libs.variables.ustkl_config.get(profile_answer, 'svn_path')+ " " +libs.variables.ustkl_config.get(profile_answer, 'git_path')+ " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    else:
        libs.cli.cli.message(["## Where to clone repos? [Give absolute path of the directory to exec git clone]"])
        the_path = ""
        the_path = input('')
        if the_path[-1] != "/":
            the_path = the_path + "/"
        os.system("sh "+libs.variables.orig_directory+"/libs/recipes/install_"+the_type+".sh "+the_path + " | tee -a " + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
        libs.variables.ustkl_config.add_section("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"))

        if the_type == "stk_speed":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK speed')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-speed/cmake_build/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-speed/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git_speed")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-speed/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
        elif the_type == "stk2":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK 2')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-2/stk-code-alayan/cmake_build/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-2/stk-code-alayan/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git2")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-2/stk-code-alayan/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-2/stk-assets/")
        elif the_type == "stk_git":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code/cmake_build/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
        elif the_type == "stk_stable":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK Stable')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"SuperTuxKart-1.4-linux-x86_64/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"SuperTuxKart-1.4-linux-x86_64/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "stable")
        elif the_type == "stk_git_kimden":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden/cmake_build/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
        elif the_type == "stk_git_kimden_client":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN CLIENT')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden-client/cmake_build/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden-client/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden-client/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
        elif the_type == "stk_git_kimden_server":
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'name', 'STK GIT KIMDEN SERVER')
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'bin_path', the_path+"stk-code-kimden-server/cmake_build/bin/supertuxkart")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'data_path', the_path+"stk-code-kimden-server/data/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'type', "git")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'git_path', the_path+"stk-code-kimden-server/")
            libs.variables.ustkl_config.set("Profile_"+started_at.strftime("%Y%m%d_%H%M%S"), 'svn_path', the_path+"stk-assets/")
        libs.common.save_config()

    print()
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
    os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+uecho_file+".log")
