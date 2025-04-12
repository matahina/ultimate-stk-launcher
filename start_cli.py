#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python start_cli.py
# to launch the cli version

import os
import setproctitle
import libs.cli.cli
import libs.variables

if __name__ == "__main__":
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
        libs.cli.cli.initialize()

    libs.cli.cli.message(["## Let's Go!"])
    libs.variables.ustkl_config.read(libs.variables.orig_directory+"/magic_libs.variables.ustkl_config.ini")

    libs.cli.cli.powerup_update()
    libs.cli.cli.addons()
    os.chdir(libs.variables.orig_directory)
    libs.cli.cli.menu()
