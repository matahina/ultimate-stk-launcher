# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# python start_gui.py
# to launch the gui version

import libs.ui.ui
import wx
import libs.common
import libs.variables

if __name__ == "__main__":
    libs.variables.init()
    app = wx.App(False)
    frame = libs.ui.ui.LaunchApp(None)
    frame.m_statusBar1.SetStatusText("Version: "+libs.variables.version, 0)
    frame.Show(True)
    app.MainLoop()
