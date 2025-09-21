#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python start_cli.py
# to launch the cli version

import setproctitle
import libs.cli.cli
import libs.common
import libs.variables
from pathlib import Path

if __name__ == "__main__":
    libs.variables.init()
    libs.cli.variables.init()

    setproctitle.setproctitle('ult_STK_launch')
    messengerella = []
    messengerella.append("")
    messengerella.append("")
    messengerella.append("")
    messengerella.append("")

    messengerella.append("      /\\_)o<        💜💜💜💜💜💜💜💜💜 WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜")
    messengerella.append("     |      \\")
    messengerella.append("     | O . O|"+"                                  Version: "+libs.variables.version)
    messengerella.append("      \\_____/")
    messengerella.append("")
    libs.cli.cli.message(messengerella)
    input("Press Enter to continue...")

    libs.cli.cli.powerup_update()
    libs.cli.cli.recipes()
    libs.cli.cli.addons()

    if (not(Path(libs.variables.orig_directory,"magic_config.ini").exists()) or Path(libs.variables.orig_directory,"magic_config.ini").stat().st_size == 0):
        libs.cli.cli.initialize()

    libs.cli.cli.message(["## Let's Go!"])
    libs.variables.ustkl_config.read(libs.common.pathery(["magic_libs.variables.ustkl_config.ini"]))

    libs.cli.cli.menu()
