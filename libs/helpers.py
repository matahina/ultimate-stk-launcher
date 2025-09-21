# -*- coding: utf-8 -*-

# For building/updating profiles

from pathlib import Path
import libs.common
import libs.variables
import yaml
import json
import questionary
import libs.cli.cli
import libs.cli.variables

def manage_profile(da_recipe_name,the_type):

    stop_now = False

    match the_type:
        case "install":
            i=1
            new_p_name = "Profile_"+str(len(libs.variables.ustkl_config.sections())+i)
            while new_p_name in libs.variables.ustkl_config.sections():
                i=i+1
                new_p_name = "Profile_"+str(len(libs.variables.ustkl_config.sections())+i)
            config_save = False
            match da_recipe_name:
                case "stk-distro":
                    bin_path = False
                    data_path = False
                    # debian = False
                    paths = ["/usr/bin/supertuxkart","/usr/share/supertuxkart"]

                    if not(Path(paths[0]).is_dir()) and Path(paths[0]).exists():
                        bin_path = True
                        if Path(paths[1]).is_dir() and Path(paths[1]).exists():
                            data_path = True
                    else:
                        paths = ["/usr/games/supertuxkart/data","/usr/share/games/supertuxkart/data"]

                    if not(Path(paths[0]).is_dir()) and Path(paths[0]).exists():
                        bin_path = True
                        if Path(paths[1]).is_dir() and Path(paths[1]).exists():
                            data_path = True
                            # debian= True

                    if bin_path and data_path:
                        config_save = True

                        libs.variables.ustkl_config.add_section(new_p_name)

                        libs.variables.ustkl_config.set(new_p_name,
                                                        'type', da_recipe_name)

                        libs.variables.ustkl_config.set(new_p_name,
                                                    'stk-version', str(1))

                        libs.variables.ustkl_config.set(new_p_name,
                                                    'name', "STK Distro")

                        libs.variables.ustkl_config.set(new_p_name,
                                                    'bin_path', paths[0])

                        libs.variables.ustkl_config.set(new_p_name,
                                                    'data_path', paths[1])

                        messagerella = ["","# Distro paths found!",
                                   "bin_path: "+paths[0],
                                   "data_path: "+paths[1]]
                    else:
                        messagerella = ["","# Distro paths not found!"]

                    libs.cli.cli.message(messagerella)

                case _:
                    config = yaml.safe_load(open(libs.common.pathery(["assets","recipes",da_recipe_name+".yaml"])))
                    path_a_valid = False
                    path_b_valid = False
                    main_path_writable = True
                    prefix = ""
                    option = ""
                    title = ""
                    if config["assets"]["type"] == "none":
                        path_a_valid = True
                    if config["recipe"]["stk-version"] != 3:
                        prefix = "stk-"+str(config["recipe"]["stk-version"])+"x"
                    else:
                        prefix = "stk-2x-tyre"
                    while (not (path_a_valid and path_b_valid)) and option != libs.cli.variables.go_back_string:
                        libs.cli.cli.message(["## Where to clone repos? [Give full path of the directory (~ is allowed)]"])
                        if not main_path_writable:
                            libs.cli.cli.message([the_path + " is not writable!"])
                        the_path = ""
                        option = ""
                        if title == "":
                            title = libs.common.pathery(["~"],False)
                        while (option != "[HERE!]") and (option != libs.cli.variables.go_back_string):
                            options = libs.common.scanerella(title,False,True)
                            options_filtered = []
                            main_path_writable = True
                            try:
                                f = open(libs.common.pathery([title, "test.txt"],False), "a")
                                f.close()
                                Path.unlink(libs.common.pathery([title, "test.txt"],False))
                            except:
                                main_path_writable = False
                            options_filtered.append("..")
                            for elem in options:
                                if elem.split("/")[-1][0] != ".":
                                    options_filtered.append(elem)
                            options_filtered.append(libs.cli.variables.go_back_string)
                            options_filtered.sort()
                            if main_path_writable:
                                options_filtered.insert(0,"[HERE!]")
                            option = questionary.select(title, options_filtered).ask()
                            if option == "..":
                                title = "/".join(title.split("/")[:-1])
                                if title == "":
                                    title = "/"
                            elif option != "[HERE!]":
                                if option != libs.cli.variables.go_back_string:
                                    title = libs.common.pathery([title,option],False)
                            print(option)

                        if option != libs.cli.variables.go_back_string:

                            the_path = libs.common.pathery([title, prefix],False)
                            the_path_a = libs.common.pathery([the_path, "stk-assets"],False)
                            the_path_b = libs.common.pathery([the_path, da_recipe_name],False)
                            suffix = ""
                            if Path(the_path_b).is_dir() and config["code"]["release"] == "tags":
                                path_b_valid = True
                            while not path_b_valid:
                                if not(Path(the_path_b).is_dir()) and not(Path(the_path_b).exists()):
                                    path_b_valid = True
                                else:
                                    libs.cli.cli.message(["## Add a suffix to path? [$ to go back previous step]"])
                                    libs.cli.cli.message([the_path_b + " already exists!"])
                                    the_path_b = libs.common.pathery([the_path, da_recipe_name], False)
                                    suffix = input(the_path_b+"-")
                                    if suffix == "$":
                                        break
                                    else:
                                        the_path_b = the_path_b + "-" + suffix
                            if suffix != "$":
                                if path_b_valid and not path_a_valid:
                                    if (Path(the_path_a).is_dir() and Path(the_path_a).exists()):
                                        libs.cli.cli.message(["## Are you sure to continue?"])
                                        libs.cli.cli.message([the_path_a + " already exists!"])
                                        answer = input('[N to go back previous step, any key to continue] ')
                                        if answer != "N" and answer != "n" :
                                            path_a_valid = True
                                    elif not(Path(the_path_a).is_dir()) and Path(the_path_a).exists():
                                        libs.cli.cli.message(["## Back to previous step"])
                                        libs.cli.cli.message([the_path_a + " already exists!"])
                                    else:
                                        path_a_valid = True
                    if option == libs.cli.variables.go_back_string:
                        stop_now = True

                    if not stop_now:
                        if (config["assets"]["type"] == "archive") or (config["code"]["type"] == "archive") or (config["code"]["release"] != "none"):
                            Path(the_path).mkdir(parents=True, exist_ok=True)

                        libs.variables.ustkl_config.add_section(new_p_name)

                        libs.variables.ustkl_config.set(new_p_name,
                                                        'type', da_recipe_name)

                        libs.variables.ustkl_config.set(new_p_name,
                                                        'stk-version', str(config["recipe"]["stk-version"]))

                        if config["assets"]["type"] == "standard":
                            if Path(the_path_a).exists():
                                svnupdate(the_path_a)
                            else:
                                svncollect(config["assets"]["type"], the_path_a)

                        if config["assets"]["type"] == "git":
                            if Path(the_path_a).exists():
                                gitupdate(the_path_a, "assets")
                            else:
                                gitclone(config["assets"]["url"], the_path_a, "# Installing assets")

                        if config["assets"]["type"] != "none":
                            libs.variables.ustkl_config.set(new_p_name,
                                                    'assets_path', the_path_a)



                        if config["code"]["type"] == "git":

                            the_url = config["code"]["url"]

                            if config["code"]["release"] == "tags":
                                if the_url == "standard":
                                    the_url = "https://github.com/supertuxkart/stk-code.git"
                                libs.cli.cli.message(
                                    libs.common.dl_file(
                                        "https://api.github.com/repos/"+the_url.split("/")[-2]+"/"+the_url.split("/")[-1].replace(".git","")+"/releases",
                                        "releases",".json","tmp_files")
                                    )
                                with open(libs.common.pathery(["assets","tmp_files","releases.json"])) as jsonfile:
                                    releases_file = json.load(jsonfile)

                                tags = []
                                level_one = []

                                for first_level in range(0,len(releases_file)):
                                    if "preview" not in releases_file[first_level]["tag_name"] and "1.5-rc1" not in releases_file[first_level]["tag_name"]:
                                        add = False
                                        for second_level in range(0,len(releases_file[first_level]["assets"])):
                                            if "linux" in releases_file[first_level]["assets"][second_level]["name"]:
                                                add = True
                                        if add:
                                            tags.append(releases_file[first_level]["tag_name"])
                                            level_one.append(first_level)


                                title = "Which release?".upper()
                                options = tags
                                option = questionary.select(title, options).ask()
                                index = options.index(option)

                                the_release = tags[index]

                                files = []
                                urls = []

                                for second_level in range(0,len(releases_file[level_one[index]]["assets"])):
                                    if "linux" in releases_file[level_one[index]]["assets"][second_level]["name"]:
                                        files.append(releases_file[level_one[index]]["assets"][second_level]["browser_download_url"].split("/")[-1])
                                        urls.append(releases_file[level_one[index]]["assets"][second_level]["browser_download_url"])


                                title = "Which file?".upper()
                                options = files
                                option = questionary.select(title, options).ask()
                                index = options.index(option)

                                the_file_url = urls[index]
                                the_file_ext = files[index].replace(the_release,"")[files[index].replace(the_release,"").find("."):]
                                the_file_name = files[index].replace(the_file_ext,"")

                                if Path(the_path_b,the_file_name).is_dir():
                                    libs.cli.cli.message(["## ALREADY INSTALLED ?!?!", libs.common.pathery([the_path_b, the_file_name],False)+" already exists!", "aborting!"])
                                else:
                                    libs.cli.cli.message(
                                        libs.common.dl_file(
                                            the_file_url,
                                            the_release,
                                            the_file_ext,
                                            "tmp_files")
                                        )

                                    Path(the_path_b).mkdir(parents=True, exist_ok=True)

                                    libs.variables.ustkl_config.set(new_p_name,
                                                                    'name', config["recipe"]["name"]+" ("+the_file_name+")")

                                    if "tar" in the_file_ext:
                                        command = ["tar", "-xf", libs.common.pathery(["assets","tmp_files",the_release+the_file_ext]), "-C", the_path_b]
                                        messengerella = ["","# Uncompress "]
                                        libs.cli.cli.run(command, messengerella)

                                    messengerella = ["","# Remove package ",libs.common.pathery(["assets","tmp_files",the_release+the_file_ext])]

                                    try:
                                        Path.unlink(libs.common.pathery(["assets","tmp_files",the_release+the_file_ext]))
                                        messengerella.append("OK!")
                                    except:
                                        messengerella.append("Error removing archive file")

                                    libs.cli.cli.message(messengerella)

                                    libs.variables.ustkl_config.set(new_p_name,
                                                                    'bin_path',
                                                                    libs.common.pathery([the_path_b,the_file_name,"bin","supertuxkart"], False)
                                                                    )

                                    libs.variables.ustkl_config.set(new_p_name,
                                                            'data_path',
                                                            libs.common.pathery([the_path_b,the_file_name,"data"], False)
                                                            )


                            else:
                                gitclone(the_url, the_path_b, "# Retrieving code")


                                libs.variables.ustkl_config.set(new_p_name,
                                                            'code_path', the_path_b)

                                libs.variables.ustkl_config.set(new_p_name,
                                                                'name', config["recipe"]["name"]+" "+suffix)

                                try:
                                    if config["code"]["branch"] != "none":
                                        gitbranch(config["code"]["branch"], the_path_b)
                                except:
                                    pass

                                try:
                                    if config["code"]["commit"] != "none":
                                        gitcommithash(config["code"]["commit"], the_path_b)

                                except:
                                    pass

                                try:
                                    if config["code"]["patch"] != "none":
                                        patcheroo(config["code"]["patch"], the_path_b)
                                except:
                                    pass

                                compileroo(config["code"]["cmake_options"], the_path_b)

                                libs.variables.ustkl_config.set(new_p_name,
                                                                'bin_path', libs.common.pathery([
                                                                    the_path_b,"cmake_build","bin","supertuxkart"],False))

                                libs.variables.ustkl_config.set(new_p_name,
                                                        'data_path', libs.common.pathery([
                                                                    the_path_b,"data"],False))

                            config_save = True

                        else:
                            pass # not implemented

            if config_save:
                libs.common.save_config()
            else:
                libs.variables.ustkl_config.remove_section(new_p_name)

        case "update":
            try:
                config = yaml.safe_load(open(libs.common.pathery(["assets","recipes",libs.variables.ustkl_config.get(da_recipe_name,'type')+".yaml"])))

            except:
                libs.cli.cli.message(["Recipe not found!!!"])
                stop_now = True

            if not stop_now:

                the_path_a = libs.variables.ustkl_config.get(da_recipe_name,'assets_path')
                the_path_b = libs.variables.ustkl_config.get(da_recipe_name,'code_path')

                if config["assets"]["type"] == "standard":
                    svnupdate(the_path_a)

                elif config["assets"]["type"] == "git" and config["assets"]["updatable"]:
                    gitupdate(the_path_a, "assets")

                if config["code"]["type"] == "git" and config["code"]["updatable"]:
                    gitupdate(the_path_b, "code")

                    try:
                        if config["code"]["branch"] != "none":
                            gitbranch(config["code"]["branch"], the_path_b)
                    except:
                        pass

                    try:
                        if config["code"]["patch"] != "none":
                            patcheroo(config["code"]["patch"], the_path_b)
                    except:
                        pass

                    compileroo(config["code"]["cmake_options"], the_path_b)

        # except:
        #     libs.cli.cli.message(["Recipe not found!!!"])
    print()


def gitclone(the_url, the_path, the_message):
    if the_url == "standard":
        the_url = "https://github.com/supertuxkart/stk-code.git"
    command = ["git", "clone", the_url, the_path]
    messengerella = ["",the_message]
    libs.cli.cli.run(command, messengerella)

def gitbranch(the_branch, the_path):
    command = ["git", "-C", the_path, "checkout", the_branch]
    messengerella = ["","# Following branch "+the_branch]
    libs.cli.cli.run(command, messengerella)

def gitcommithash(the_hash, the_path):
    command = ["git", "-C", the_path, "checkout", the_hash]
    messengerella = ["","# Go to commit "+the_hash]
    libs.cli.cli.run(command, messengerella)

def gitupdate(the_path, the_type):
    command = ["git", "-C", the_path, "reset", "--hard"]
    messengerella = ["","# Reverting "+the_type]
    libs.cli.cli.run(command, messengerella)

    command = ["git", "-C", the_path, "pull"]
    messengerella = ["","# Updating "+the_type]
    libs.cli.cli.run(command, messengerella)


def svncollect(the_url, the_path):
    if the_url == "standard":
        the_url = "https://svn.code.sf.net/p/supertuxkart/code/stk-assets"
    command = ["svn", "co", the_url, the_path]
    messengerella = ["","# Installing assets"]
    libs.cli.cli.run(command, messengerella)


def svnupdate(the_path):
    command = ["svn", "revert", "--recursive", the_path]
    messengerella = ["","# Reverting assets"]
    libs.cli.cli.run(command, messengerella)

    command = ["svn", "up", the_path]
    messengerella = ["","# Updating assets"]
    libs.cli.cli.run(command, messengerella)


def patcheroo(patch_list, the_path):
    for elem in patch_list:
        libs.cli.cli.message(
            libs.common.dl_file(patch_list[elem],elem,".patch","tmp_files")
            )
        command = ["git", "-C", the_path, "apply", libs.common.pathery(["assets","tmp_files",elem+".patch"])]
        messengerella = ["","# Applying patch "+elem]
        libs.cli.cli.run(command, messengerella)


def compileroo(cmake_optionellas, the_path):

    Path(the_path,"cmake_build").mkdir(parents=True, exist_ok=True)

    command = ["cmake"]
    if cmake_optionellas != "none":
        command.append(cmake_optionellas)
    command.append("-B"+libs.common.pathery([the_path,"cmake_build"],False))
    command.append("-S"+the_path)
    messengerella = ["","# Configuring"]

    libs.cli.cli.run(command, messengerella)

    command = ["make", "-C", libs.common.pathery([the_path,"cmake_build"],False), "-j"+libs.cli.cli.get_nproc()]
    messengerella = ["","# Compiling"]
    libs.cli.cli.run(command, messengerella)

