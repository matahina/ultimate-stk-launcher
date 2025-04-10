# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# python start_gui.py
# to launch the gui version

import libs.ui.uSTKl_gui
from libs.threads import *
import wx
import os ## !!!!
import libs.common
import libs.variables



class LaunchApp(libs.ui.uSTKl_gui.MainFrame):
    def __init__(self,parent):
        libs.ui.uSTKl_gui.MainFrame.__init__(self,parent)

        self.m_button2.SetBitmap( wx.Bitmap( u"libs/ui/supertuxkart_16.png", wx.BITMAP_TYPE_ANY ) )

        self.m_grid1.HideRowLabels()
        self.m_grid1.HideColLabels()
        self.m_grid1.SetCellHighlightPenWidth(0)
        self.m_grid1.SetCellHighlightROPenWidth(0)

        names = []
        for name in libs.variables.ustkl_config.sections():
            names.append(libs.variables.ustkl_config.get(name, 'name'))
        self.m_choice1.SetItems(names)
        self.m_choice1.SetSelection(0)
        self.m_choice1.Bind(wx.EVT_CHOICE, self.OnChoice1)

        self.pup_list_update()

        term_apps = ["konsole","gnome-terminal","yakuake","guake","terminator","tilda","terminology","xterm","pantheon-terminal","deepin-terminal","mauikit-terminal","xfce4-terminal","lxterminal","xfterm4"]
        terminals = []

        if "KDE" in libs.variables.de_name:
            if [s for s in os.listdir('/usr/bin') if "konsole" in s] != []:
                terminals.append("konsole")
                term_apps.remove("konsole")
        if "GNOME" in libs.variables.de_name:
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
        self.Bind(EVT_ONLINERY, self.OnOnlinery)
        self.Bind(EVT_ADDONUPD, self.OnAddonupd)

        self.RefreshAddons()
        self.RefreshOnline()


    def message_gui(self, text):
        for elem in text:
            if "##" in elem:
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
                self.m_textCtrl3.AppendText("\n"+elem.upper()+"\n")
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            else:
                if "Could not retrieve" in elem or "Error" in elem:
                    self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.RED))
                self.m_textCtrl3.AppendText(elem+"\n")
                self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))

    def RefreshOnline(self):


        worker = OnlineryThread(self)
        worker.start()

    def RefreshAddons(self):


        self.m_button21.Disable()
        self.m_button3.Disable()
        self.m_button6.Disable()

        self.m_staticText4.SetLabel(libs.common.quantity(0,"update"))
        self.m_staticText5.SetLabel(libs.common.quantity(0,"install"))


        worker = AddoneryThread(self)
        worker.start()

    def OnAddonupd(self, evt):
        self.message_gui(evt.GetValue())
        if libs.variables.lock > 1:
            self.m_textCtrl3.AppendText('...\n')
        libs.variables.lock = libs.variables.lock -1

    def OnOnlinery(self, evt):
        self.m_button7.Enable()
        self.message_gui(evt.GetValue())
        self.servernodes = []
        self.subservernodes = []
        self.playernodes = []
        self.rootstring = str(libs.variables.online_db.total_players)+" player"
        if libs.variables.online_db.total_players > 1:
            self.rootstring = self.rootstring + "s"
        self.root = self.m_treeCtrl1.AddRoot(self.rootstring)
        for elem in range(0,len(libs.variables.online_db.servers)):
            self.servernodes.append(self.m_treeCtrl1.AppendItem(self.root,libs.variables.online_db.servers[elem][0]))
            for i in range(1,len(libs.variables.online_db.servers[elem])):
                self.subservernodes.append(self.m_treeCtrl1.AppendItem(self.servernodes[-1],libs.variables.online_db.servers[elem][i]))
            self.subservernodes.append(self.m_treeCtrl1.AppendItem(self.servernodes[-1],"Players"))
            for pelem in libs.variables.online_db.players[elem]:
                self.playernodes.append(self.m_treeCtrl1.AppendItem(self.subservernodes[-1],pelem))
        self.m_treeCtrl1.Expand(self.root)
        # for elem in self.servernodes:
        #     self.m_treeCtrl1.Expand(elem)
        for elem in self.subservernodes:
            self.m_treeCtrl1.Expand(elem)

    def OnAddonery(self, evt):
        self.m_button2.Enable()
        self.message_gui(evt.GetValue())
        while self.m_grid1.GetNumberRows()>0:
            self.m_grid1.DeleteRows(0)
        while self.m_grid1.GetNumberCols()>0:
            self.m_grid1.DeleteCols(0)
        self.m_button6.Enable()
        if libs.variables.addon_lib.upd_track != [] or libs.variables.addon_lib.to_inst_track != [] or libs.variables.addon_lib.upd_arena != [] or libs.variables.addon_lib.to_inst_arena != []:
            self.m_button6.SetLabel("Apply changes")
            self.m_grid1.AppendCols(7)
            self.m_grid1.HideCol(4)
            self.m_grid1.HideCol(5)
            self.m_grid1.HideCol(6)
            self.m_staticText4.SetLabel(libs.common.quantity(len(libs.variables.addon_lib.upd_track)+len(libs.variables.addon_lib.upd_arena),"update"))
            if len(libs.variables.addon_lib.upd_track)+len(libs.variables.addon_lib.upd_arena) > 0:
                self.m_button21.Enable()
            else:
                self.m_button21.Disable()
            self.m_staticText5.SetLabel(libs.common.quantity(len(libs.variables.addon_lib.to_inst_track)+len(libs.variables.addon_lib.to_inst_arena),"install"))
            if len(libs.variables.addon_lib.to_inst_track)+len(libs.variables.addon_lib.to_inst_arena) > 0:
                self.m_button3.Enable()
            else:
                self.m_button3.Disable()
        else:
            self.m_button6.SetLabel("Refresh")
        if libs.variables.addon_lib.upd_track != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> Track Updates".upper())
            for elem in libs.variables.addon_lib.upd_track:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.common.break_line(libs.variables.addon_lib.avail_tracks[elem][1],80)+"\n\n"+libs.common.break_line(libs.variables.addon_lib.avail_tracks[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.common.break_line(libs.variables.addon_lib.avail_tracks[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.variables.addon_lib.avail_tracks[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"track")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"update")
        if libs.variables.addon_lib.to_inst_track != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> New Tracks".upper())
            for elem in libs.variables.addon_lib.to_inst_track:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.common.break_line(libs.variables.addon_lib.avail_tracks[elem][1],80)+"\n\n"+libs.common.break_line(libs.variables.addon_lib.avail_tracks[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.common.break_line(libs.variables.addon_lib.avail_tracks[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.variables.addon_lib.avail_tracks[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"track")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"install")
        if libs.variables.addon_lib.upd_arena != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> Arena Updates".upper())
            for elem in libs.variables.addon_lib.upd_arena:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.common.break_line(libs.variables.addon_lib.avail_arenas[elem][1],80)+"\n\n"+libs.common.break_line(libs.variables.addon_lib.avail_arenas[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.common.break_line(libs.variables.addon_lib.avail_arenas[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.variables.addon_lib.avail_arenas[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"arena")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"update")
        if libs.variables.addon_lib.to_inst_arena != []:
            self.m_grid1.AppendRows(1)
            self.m_grid1.SetCellSize(self.m_grid1.GetNumberRows()-1, 0, 1, 4) #ligne,colonne,hauteur,longueur
            self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1, 0, ">> New Arenas".upper())
            for elem in libs.variables.addon_lib.to_inst_arena:
                self.m_grid1.AppendRows(1)
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,0,libs.common.break_line(libs.variables.addon_lib.avail_arenas[elem][1],80)+"\n\n"+libs.common.break_line(libs.variables.addon_lib.avail_arenas[elem][6],80))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,1,libs.common.break_line(libs.variables.addon_lib.avail_arenas[elem][4],40))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,2,str(round(int(libs.variables.addon_lib.avail_arenas[elem][8])/(1024*1024),1)) + "MB")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,4,str(elem))
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,5,"arena")
                self.m_grid1.SetCellValue(self.m_grid1.GetNumberRows()-1,6,"install")
        if libs.variables.addon_lib.upd_track != [] or libs.variables.addon_lib.to_inst_track != [] or libs.variables.addon_lib.upd_arena != [] or libs.variables.addon_lib.to_inst_arena != []:
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

    def uponline(self,event):
        self.m_button7.Disable()
        self.m_treeCtrl1.DeleteAllItems()
        self.RefreshOnline()

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
            self.m_textCtrl3.AppendText(libs.variables.orig_directory+"/tmp_files/\n")
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
            self.m_textCtrl3.AppendText("\n## Then moving addon files in ".upper())
            self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
            self.m_textCtrl3.AppendText(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/\n')
            self.m_textCtrl3.AppendText('...\n')

        for worker in workers:
            libs.variables.lock = libs.variables.lock +1
            worker.start()

        self.RefreshAddons()


    def go_tab_addon( self, event ):
        self.m_notebook6.SetSelection(1)

    def go_tab_profiles( self, event ):
        self.m_notebook6.SetSelection(2)

    def pup_refresh(self, evt):
        self.m_button4.Disable()
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.m_textCtrl3.AppendText("\n## Downloading powerup files in ".upper())
        self.m_textCtrl3.SetDefaultStyle(wx.TextAttr(wx.WHITE))
        self.m_textCtrl3.AppendText(libs.variables.orig_directory+"/tmp_files/\n")
        workers = []
        for index,row in libs.variables.assets_data[["url","name"]].iterrows():
            workers.append(UpdateFilesThread(self, row["name"], row["url"]))
        for worker in workers:
            worker.start()

    def OnUpdateFiles(self, evt):
        self.message_gui(evt.GetValue())
        self.m_button4.Enable()
        self.OnChoice1(evt)



    def OnChoice1(self,event):
        self.pup_list_update()

    def pup_list_update(self):

        profile_answer = self.m_choice1.GetString( self.m_choice1.GetSelection() )
        num=0
        for i in range(0,len(libs.variables.ustkl_config.sections())):
            if libs.variables.ustkl_config.get(libs.variables.ustkl_config.sections()[i],"name") == profile_answer:
                num=i

        if libs.variables.ustkl_config.get(libs.variables.ustkl_config.sections()[num], 'type') == "git2":
            self.m_choice2.SetItems(libs.common.powerup_list(2))
        else:
            self.m_choice2.SetItems(libs.common.powerup_list(0))

        self.m_choice2.SetSelection(0)


    def goo( self, event ):
        self.m_button2.Disable()
        self.m_button6.Disable()
        suffix = ""
        profile_answer = self.m_choice1.GetString( self.m_choice1.GetSelection() )
        num=0
        for i in range(0,len(libs.variables.ustkl_config.sections())):
            if libs.variables.ustkl_config.get(libs.variables.ustkl_config.sections()[i],"name") == profile_answer:
                num=i
        profile_id = libs.variables.ustkl_config.sections()[num]
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
            powerup_id = self.m_choice2.GetString( self.m_choice2.GetSelection())
            prefix = ""
            suffixbis = ""
            messengerella, prefix = libs.common.starterella(profile_id, powerup_id)

            self.message_gui(messengerella)

            commnd = [prefix+"."+libs.variables.ustkl_config.get(profile_id, 'bin_path').replace(os.path.dirname( libs.variables.ustkl_config.get(profile_id, 'bin_path')  ),'') + suffix + suffixbis]
            commnd.append(os.path.dirname( libs.variables.ustkl_config.get(profile_id, 'bin_path') ))
            commnd.append(libs.variables.ustkl_config.get(profile_id, 'bin_path').replace(os.path.dirname( libs.variables.ustkl_config.get(profile_id, 'bin_path')  ),''))

            self.m_textCtrl3.AppendText(commnd[0]+"\n")
            # os.system("echo '========================  '"+echo_file+"'  ========================' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
            # os.system("."+config.get(profile_answer, 'bin_path').replace(os.path.dirname( config.get(profile_answer, 'bin_path')  ),'') + suffix + suffixbis)
            # os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")
            # os.system("echo '' >>" + libs.variables.orig_directory+"/logs/"+echo_file+".log")




            worker = GearsThread(self,self.m_choice3.GetString( self.m_choice3.GetSelection()),commnd,[])
            worker.start()

    def OnGears(self, evt):

        messengerella = libs.common.enderella()

        self.message_gui(messengerella)

        self.m_button2.Enable()

        self.RefreshAddons()


if __name__ == "__main__":
    libs.variables.init()
    app = wx.App(False)
    frame = LaunchApp(None)
    frame.m_statusBar1.SetStatusText("Version: "+libs.variables.version, 0)
    frame.Show(True)
    app.MainLoop()
