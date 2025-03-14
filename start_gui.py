# -*- coding: utf-8 -*-

import libs.ui.uSTKl_gui
from threading import Thread

from libs.threads import *

import wx,sys

from libs.version import __version__

import subprocess

import pandas as pd


import os
from urllib import request


import threading
import time


from configparser import ConfigParser

import libs.settings
import libs.helpers
import libs.common








from os import listdir
from os.path import isfile, join


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


















class LaunchApp(libs.ui.uSTKl_gui.MainFrame):
    def __init__(self,parent):
        libs.ui.uSTKl_gui.MainFrame.__init__(self,parent)

        self.m_button2.SetBitmap( wx.Bitmap( u"libs/ui/supertuxkart_16.png", wx.BITMAP_TYPE_ANY ) )

        self.m_grid1.HideRowLabels()
        self.m_grid1.HideColLabels()
        self.m_grid1.SetCellHighlightPenWidth(0)
        self.m_grid1.SetCellHighlightROPenWidth(0)
        self.pup_list()

        names = []
        for name in libs.settings.ustkl_config.sections():
            names.append(libs.settings.ustkl_config.get(name, 'name'))
        self.m_choice1.SetItems(names)
        self.m_choice1.SetSelection(0)
        self.m_choice1.Bind(wx.EVT_CHOICE, self.OnChoice1)

        version = 0
        if libs.settings.ustkl_config.get(libs.settings.ustkl_config.sections()[0], 'type') == "git2":
            if "STK2" in p_up_list:
                version = 2

        self.pup_list_update(version)

        term_apps = ["konsole","gnome-terminal","yakuake","guake","terminator","tilda","terminology","xterm","pantheon-terminal","deepin-terminal","mauikit-terminal","xfce4-terminal","lxterminal","xfterm4"]
        terminals = []

        if "KDE" in libs.settings.de_name:
            if [s for s in os.listdir('/usr/bin') if "konsole" in s] != []:
                terminals.append("konsole")
                term_apps.remove("konsole")
        if "GNOME" in libs.settings.de_name:
            if [s for s in os.listdir('/usr/bin') if "gnome-terminal" in s] != []:
                terminals.append("gnome-terminal")
                term_apps.remove("gnome-terminal")

        for elem in term_apps:
            if [s for s in os.listdir('/usr/bin') if elem in s] != []:
                terminals.append(elem)

        self.m_choice3.AppendItems( terminals )
        self.m_choice3.SetSelection(0)



        self.m_button21.Disable()
        self.m_button3.Disable()
        self.m_button5.Disable()
        self.Bind(EVT_UPDATE_FILES, self.OnUpdateFiles)
        self.Bind(EVT_GEARS, self.OnGears)
        self.Bind(EVT_ADDONERY, self.OnAddonery)
        self.Bind(EVT_ADDONUPD, self.OnAddonupd)

        self.RefreshAddons()

    def RefreshAddons(self):


        self.m_button21.Disable()
        self.m_button3.Disable()
        self.m_button6.Disable()

        self.m_staticText4.SetLabel(libs.helpers.quantity(0,"update"))
        self.m_staticText5.SetLabel(libs.helpers.quantity(0,"install"))


        worker = AddoneryThread(self)
        worker.start()

    def OnAddonupd(self, evt):
        for elem in evt.GetValue():
            if "Could not retrieve" in elem or "Error" in elem:
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.m_textCtrl3.AppendText(elem)
            if "Could not retrieve" in elem or "Error" in elem:
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            self.m_textCtrl3.AppendText("\n")
        if libs.settings.lock > 1:
            self.m_textCtrl3.AppendText('...\n')
        libs.settings.lock = libs.settings.lock -1

    def OnAddonery(self, evt):
        self.m_button2.Enable()
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.m_textCtrl3.AppendText("\n## Downloading addon list in ".upper())
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
        self.m_textCtrl3.AppendText(libs.settings.orig_directory+"/tmp_files/\n")
        for elem in evt.GetValue():
            if "Could not retrieve" in elem:
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.m_textCtrl3.AppendText(elem)
            if "Could not retrieve" in elem:
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            self.m_textCtrl3.AppendText("\n")
            while self.m_grid1.GetNumberRows()>0:
                self.m_grid1.DeleteRows(0)
            while self.m_grid1.GetNumberCols()>0:
                self.m_grid1.DeleteCols(0)
            self.m_button6.Enable()
        if libs.settings.addon_lib.upd_track != [] or libs.settings.addon_lib.to_inst_track != [] or libs.settings.addon_lib.upd_arena != [] or libs.settings.addon_lib.to_inst_arena != []:
            self.m_button6.SetLabel("Apply changes")
            self.m_grid1.AppendCols(7)
            self.m_grid1.HideCol(4)
            self.m_grid1.HideCol(5)
            self.m_grid1.HideCol(6)
            self.m_staticText4.SetLabel(libs.helpers.quantity(len(libs.settings.addon_lib.upd_track)+len(libs.settings.addon_lib.upd_arena),"update"))
            if len(libs.settings.addon_lib.upd_track)+len(libs.settings.addon_lib.upd_arena) > 0:
                self.m_button21.Enable()
            else:
                self.m_button21.Disable()
            self.m_staticText5.SetLabel(libs.helpers.quantity(len(libs.settings.addon_lib.to_inst_track)+len(libs.settings.addon_lib.to_inst_arena),"install"))
            if len(libs.settings.addon_lib.to_inst_track)+len(libs.settings.addon_lib.to_inst_arena) > 0:
                self.m_button3.Enable()
            else:
                self.m_button3.Disable()
        else:
            self.m_button6.SetLabel("Refresh")
        if libs.settings.addon_lib.upd_track != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> Track Updates".upper())
            for elem in libs.settings.addon_lib.upd_track:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.helpers.break_line(libs.settings.addon_lib.avail_tracks[elem][1],80)+"\n\n"+libs.helpers.break_line(libs.settings.addon_lib.avail_tracks[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.helpers.break_line(libs.settings.addon_lib.avail_tracks[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.settings.addon_lib.avail_tracks[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"track")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"update")
        if libs.settings.addon_lib.to_inst_track != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> New Tracks".upper())
            for elem in libs.settings.addon_lib.to_inst_track:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.helpers.break_line(libs.settings.addon_lib.avail_tracks[elem][1],80)+"\n\n"+libs.helpers.break_line(libs.settings.addon_lib.avail_tracks[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.helpers.break_line(libs.settings.addon_lib.avail_tracks[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.settings.addon_lib.avail_tracks[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"track")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"install")
        if libs.settings.addon_lib.upd_arena != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> Arena Updates".upper())
            for elem in libs.settings.addon_lib.upd_arena:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.helpers.break_line(libs.settings.addon_lib.avail_arenas[elem][1],80)+"\n\n"+libs.helpers.break_line(libs.settings.addon_lib.avail_arenas[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.helpers.break_line(libs.settings.addon_lib.avail_arenas[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.settings.addon_lib.avail_arenas[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"arena")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"update")
        if libs.settings.addon_lib.to_inst_arena != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> New Arenas".upper())
            for elem in libs.settings.addon_lib.to_inst_arena:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.helpers.break_line(libs.settings.addon_lib.avail_arenas[elem][1],80)+"\n\n"+libs.helpers.break_line(libs.settings.addon_lib.avail_arenas[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.helpers.break_line(libs.settings.addon_lib.avail_arenas[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.settings.addon_lib.avail_arenas[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"arena")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"install")
        if libs.settings.addon_lib.upd_track != [] or libs.settings.addon_lib.to_inst_track != [] or libs.settings.addon_lib.upd_arena != [] or libs.settings.addon_lib.to_inst_arena != []:
            attr = wx.grid.GridCellAttr()
            attr.SetEditor(wx.grid.GridCellBoolEditor())
            attr.SetRenderer(wx.grid.GridCellBoolRenderer())
            self.m_grid1.SetColAttr(3,attr)
            for i in range(0,6):
                if i !=3:
                    for j in range(0,self.m_grid1.GetNumberRows()):
                        self.m_grid1.SetReadOnly(j, i, True)
            for i in range(0,self.m_grid1.GetNumberCols()):
                self.m_grid1.AutoSizeColumn(i)
            for i in range(0,self.m_grid1.GetNumberRows()):
                self.m_grid1.AutoSizeRow(i)
            self.m_grid1.ShowScrollbars(wx.SHOW_SB_DEFAULT,wx.SHOW_SB_DEFAULT)

    def updatery(self,event):
        self.m_button6.Disable()
        self.m_button2.Disable()
        workers = []
        for i in range(0,self.m_grid1.GetNumberRows()):
            res = self.m_grid1.GetCellValue(i,3)
            if res == "1":
                workers.append(AddonupdThread(self,int(self.m_grid1.GetCellValue(i,4)),self.m_grid1.GetCellValue(i,5),self.m_grid1.GetCellValue(i,6)))

        if workers != []:
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.m_textCtrl3.AppendText("\n## Downloading addon files in ".upper())
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            self.m_textCtrl3.AppendText(libs.settings.orig_directory+"/tmp_files/\n")
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.m_textCtrl3.AppendText("\n## Then moving addon files in ".upper())
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            self.m_textCtrl3.AppendText(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/\n')
            self.m_textCtrl3.AppendText('...\n')

        for worker in workers:
            libs.settings.lock = libs.settings.lock +1
            worker.start()

        self.RefreshAddons()


    def go_tab_addon( self, event ):
        self.m_notebook6.SetSelection(1)

    def go_tab_profiles( self, event ):
        self.m_notebook6.SetSelection(2)

    def pup_list(self):
        onlyfiles = [f for f in os.listdir(libs.settings.orig_directory+"/tmp_files/") if os.path.isfile(os.path.join(libs.settings.orig_directory+"/tmp_files/", f))]

        pos = 0
        for elem in libs.settings.assets_data["name"]:
            if elem+".xml" in onlyfiles:
                libs.settings.assets_data.loc[pos, "downloaded"] = "Y"
            pos = pos+1

        powerups = list(set(libs.settings.assets_data["id"]))
        powerups.remove("")

        for elem in powerups:
            if "" in list(libs.settings.assets_data.where(libs.settings.assets_data["id"] == elem).dropna()["downloaded"]):
                for i in list(libs.settings.assets_data.where(libs.settings.assets_data["id"] == elem).dropna()["downloaded"].index):
                    libs.settings.assets_data.loc[i, "downloaded"] = ""

    def pup_refresh(self, evt):
        self.m_button4.Disable()
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.m_textCtrl3.AppendText("\n## Downloading powerup files in ".upper())
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
        self.m_textCtrl3.AppendText(libs.settings.orig_directory+"/tmp_files/\n")
        workers = []
        for index,row in libs.settings.assets_data[["url","name"]].iterrows():
            workers.append(UpdateFilesThread(self, row["name"], row["url"]))
        for worker in workers:
            worker.start()

    def OnUpdateFiles(self, evt):
        if "Could not retrieve" in evt.GetValue():
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.RED))
        self.m_textCtrl3.AppendText(evt.GetValue())
        if "Could not retrieve" in evt.GetValue():
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
        self.m_button4.Enable()
        self.OnChoice1(evt)


    def OnChoice1(self,event):
        profile_answer = self.m_choice1.GetString( self.m_choice1.GetSelection() )
        num=0
        for i in range(0,len(libs.settings.ustkl_config.sections())):
            if libs.settings.ustkl_config.get(libs.settings.ustkl_config.sections()[i],"name") == profile_answer:
                num=i
        if libs.settings.ustkl_config.get(libs.settings.ustkl_config.sections()[num], 'type') == "git2":
            self.pup_list_update(2)
        else:
            self.pup_list_update(0)

    def pup_list_update( self, version ):
        self.pup_list()
        a2 = libs.settings.assets_data.where(libs.settings.assets_data["downloaded"] == "Y")
        a2 = a2.fillna("")

        p_up_list = list(dict.fromkeys(a2["id"]))
        p_up_list.remove("")

        p_up_final_list = []

        if version != 2:
            if "STK2" in p_up_list:
                p_up_list.remove("STK2")
            p_up_final_list = p_up_list
        elif "STK2" in p_up_list:
            p_up_final_list.append("STK2")

        self.m_choice2.SetItems(p_up_final_list)
        self.m_choice2.SetSelection(0)


    def goo( self, event ):
        self.m_button2.Disable()
        self.m_button6.Disable()
        suffix = ""
        profile_answer = self.m_choice1.GetString( self.m_choice1.GetSelection() )
        num=0
        for i in range(0,len(libs.settings.ustkl_config.sections())):
            if libs.settings.ustkl_config.get(libs.settings.ustkl_config.sections()[i],"name") == profile_answer:
                num=i
        profile_id = libs.settings.ustkl_config.sections()[num]
        if self.m_checkBox1.IsChecked():
            suffix = " --track-debug "
        if self.m_checkBox2.IsChecked():
            suffix = suffix + " --check-debug "
        if self.m_choice2.IsEmpty():
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.m_textCtrl3.AppendText("\nYOU NEED TO CHOOSE A POWERUP\n")
            self.m_textCtrl3.AppendText("Try refreshing powerups.\n")
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            self.m_button2.Enable()
            self.m_button6.Disable()
        else:
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.m_textCtrl3.AppendText("\n## Am gonna make your dreams come true...\n".upper())
            self.m_textCtrl3.AppendText("\n## New data is in\n".upper())
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            libs.settings.data_relocation = libs.common.relocate_data(libs.settings.ustkl_config.get(profile_id, 'data_path'))
            self.m_textCtrl3.AppendText(libs.settings.data_relocation+"\n")
            if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_id)]:
                libs.settings.assets_relocation = libs.common.relocate_data(libs.settings.ustkl_config.get(profile_id, 'svn_path'))
                self.m_textCtrl3.AppendText(libs.settings.assets_relocation+"\n")
            os.chdir(libs.settings.orig_directory+"/my_files/")
            self.m_textCtrl3.AppendText("chdir "+ os.path.dirname( libs.settings.orig_directory+"/my_files/" )+"\n")

            filelist = []
            revert_list = []

            path = libs.settings.orig_directory+"/my_files/"

            # os.system("chmod o+r "+settings.orig_directory+"/my_files/*")
            # os.system("chmod o+r "+settings.orig_directory+"/tmp_files/*")

            for root, dirs, files in os.walk(libs.settings.orig_directory+"/my_files/"):
                for file in files:
                    filelist.append(os.path.join(root,file).replace(path,""))

            filelist.remove(".placeholder")

            for name in filelist:
                if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_id)] and ( (name[0:name.find("/",1)].replace("/","") in issvn) ):
                    commnd = "rm "+libs.settings.assets_relocation+"/"+name
                    sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
                    sw_out=sw.stdout.decode("utf-8").replace('\n','')

                    self.m_textCtrl3.AppendText(commnd+"\n")
                    if sw_out != "":
                        self.m_textCtrl3.AppendText(sw_out+"\n")

                    commnd = "cp --parents "+name+" "+libs.settings.assets_relocation
                    sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
                    sw_out=sw.stdout.decode("utf-8").replace('\n','')

                    self.m_textCtrl3.AppendText(commnd+"\n")
                    if sw_out != "":
                        self.m_textCtrl3.AppendText(sw_out+"\n")
                else:
                    commnd = "rm "+libs.settings.data_relocation+"/"+name
                    sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
                    sw_out=sw.stdout.decode("utf-8").replace('\n','')

                    self.m_textCtrl3.AppendText(commnd+"\n")
                    if sw_out != "":
                        self.m_textCtrl3.AppendText(sw_out+"\n")

                    commnd = "cp --parents "+name+" "+libs.settings.data_relocation
                    sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
                    sw_out=sw.stdout.decode("utf-8").replace('\n','')

                    self.m_textCtrl3.AppendText(commnd+"\n")
                    if sw_out != "":
                        self.m_textCtrl3.AppendText(sw_out+"\n")


            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.m_textCtrl3.AppendText("\n## Using the choosen powerup file\n".upper())
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))

            powerup_id = self.m_choice2.GetString( self.m_choice2.GetSelection())

            p_up_file_name = list(libs.settings.assets_data['name'].where(libs.settings.assets_data['id'] == powerup_id).where(libs.settings.assets_data['type'] == "powerup").dropna())
            pfile = p_up_file_name[0]+".xml"
            kart_file_name = list(libs.settings.assets_data['name'].where(libs.settings.assets_data['id'] == powerup_id).where(libs.settings.assets_data['type'] == "kart").dropna())
            if kart_file_name == []:
                kfile="kart_characteristics_orig.xml"
            else:
                kfile = kart_file_name[0]+".xml"

            os.chdir(libs.settings.data_relocation)
            self.m_textCtrl3.AppendText("chdir "+ libs.settings.data_relocation+"\n")

            commnds = ["rm powerup.xml",
                       "rm kart_characteristics.xml",
                       "cp "+libs.settings.orig_directory+"/tmp_files/"+pfile+" powerup.xml",
                       "cp "+libs.settings.orig_directory+"/tmp_files/"+kfile+" kart_characteristics.xml"]

            for commnd in commnds:
                sw = subprocess.run(commnd, shell =True, stdout=subprocess.PIPE)
                sw_out=sw.stdout.decode("utf-8").replace('\n','')

                self.m_textCtrl3.AppendText(commnd+"\n")
                if sw_out != "":
                    self.m_textCtrl3.AppendText(sw_out+"\n")


            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.m_textCtrl3.AppendText("\n## Running\n".upper())
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))

            os.chdir(os.path.dirname(libs.settings.ustkl_config.get(profile_id, 'bin_path')  ))
            self.m_textCtrl3.AppendText("chdir "+ os.path.dirname( libs.settings.ustkl_config.get(profile_id, 'bin_path')  )+"\n")
            suffixbis = ""
            # suffixbis = " | tee -a "+libs.settings.orig_directory+"/logs/"+echo_file+".log"
            prefix = ""
            if 'svn_path' in [row[0] for row in libs.settings.ustkl_config.items(profile_id)]:
                prefix = prefix + 'export SUPERTUXKART_ASSETS_DIR="'+libs.settings.assets_relocation+'" ; '

            prefix = prefix + 'export SUPERTUXKART_DATADIR="'+libs.settings.data_relocation[:-6]+'" ; '
            if libs.settings.ustkl_config.get(profile_id, 'type') == "other":
                prefix = prefix + "export SYSTEM_LD_LIBRARY_PATH=\"$LD_LIBRARY_PATH\";export LD_LIBRARY_PATH=\"$DIRNAME/lib:$LD_LIBRARY_PATH\" ; "
            commnd = [prefix+"."+libs.settings.ustkl_config.get(profile_id, 'bin_path').replace(os.path.dirname( libs.settings.ustkl_config.get(profile_id, 'bin_path')  ),'') + suffix + suffixbis]
            commnd.append(os.path.dirname( libs.settings.ustkl_config.get(profile_id, 'bin_path') ))
            commnd.append(libs.settings.ustkl_config.get(profile_id, 'bin_path').replace(os.path.dirname( libs.settings.ustkl_config.get(profile_id, 'bin_path')  ),''))

            self.m_textCtrl3.AppendText(commnd[0]+"\n")
            # os.system("echo '========================  '"+echo_file+"'  ========================' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
            # os.system("."+config.get(profile_answer, 'bin_path').replace(os.path.dirname( config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
            # os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.settings.orig_directory+"/logs/"+echo_file+".log")




            worker = GearsThread(self,self.m_choice3.GetString( self.m_choice3.GetSelection()),commnd,[])
            worker.start()

    def OnGears(self, evt):

        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.m_textCtrl3.AppendText("\n## Removing tmp data files\n".upper())
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))

        self.m_textCtrl3.AppendText("rm -R "+libs.settings.data_relocation)
        shutil.rmtree(libs.settings.data_relocation)
        if libs.settings.assets_relocation != []:
            self.m_textCtrl3.AppendText("rm -R "+libs.settings.assets_relocation)
            shutil.rmtree(libs.settings.assets_relocation)

        libs.settings.assets_relocation = ""
        libs.settings.data_relocation = ""
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.m_textCtrl3.AppendText("\n## Dooooone =D\n".upper())
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))

        self.m_button2.Enable()

        self.RefreshAddons()


if __name__ == "__main__":
    libs.settings.init()
    app = wx.App(False)
    frame = LaunchApp(None)
    frame.m_statusBar1.SetStatusText("Version: "+__version__, 0)
    frame.Show(True)
    app.MainLoop()
