import wx
import threading
import os
from urllib import request
import subprocess
import libs.settings
from lxml import etree
import xml.etree.ElementTree as ET
import shutil
import zipfile
import libs.helpers
import time

myEVT_UPDATE_FILES = wx.NewEventType()

EVT_UPDATE_FILES = wx.PyEventBinder(myEVT_UPDATE_FILES, 1)


class UpdateFilesEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value


class UpdateFilesThread(threading.Thread):
    def __init__(self, parent, name, url):
        """
        @param parent: The gui object that should recieve the value
        @param value: value to 'calculate' to
        """
        threading.Thread.__init__(self)
        self._parent = parent
        self._name = name
        self._url = url
        self._answer = ""

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        self._answer = self._answer + "\n# " + self._name
        try:
            request.urlretrieve(self._url, libs.settings.orig_directory+"/tmp_files/"+self._name+".xml")
        except:
            self._answer = self._answer + "\n" + "Could not retrieve " + self._url + "\n"
        else:
            self._answer = self._answer + "\n" + "OK " + self._url + "\n"
        evt = UpdateFilesEvent(myEVT_UPDATE_FILES, -1, value=self._answer)
        wx.PostEvent(self._parent, evt)



myEVT_GEARS = wx.NewEventType()
EVT_GEARS = wx.PyEventBinder(myEVT_GEARS, 1)
class GearsEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value


class GearsThread(threading.Thread):
    def __init__(self, parent, method="", the_command="", revert_list=[]):
        """
        @param parent: The gui object that should recieve the value
        @param value: value to 'calculate' to
        """
        threading.Thread.__init__(self)
        self._parent = parent
        self._answer = ""
        self._method = method
        self._the_command = the_command
        self._revert_list = revert_list

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        # process = subprocess.run(["/home/petite_fleur/Softs/stk-code/cmake_build/bin/supertuxkart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if self._method == "No terminal":
            process = subprocess.run(self._the_command[0], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        elif self._method == "konsole":
            process = subprocess.run("konsole --noclose -e "+self._the_command[0], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        elif self._method == "gnome-terminal":
            time.sleep(1)
            process = subprocess.run("gnome-terminal -- bash -c '"+self._the_command[0]+"; exec bash'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        elif self._method == "yakuake":
            lal = subprocess.run("SESSION_ID=$(qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.addSession) ; echo $SESSION_ID ; TERMINAL_ID=$(qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.terminalIdsForSessionId $SESSION_ID  ; echo $TERMINAL_ID)", shell =True, stdout=subprocess.PIPE)
            sess_id=lal.stdout.decode("utf-8").replace('\n','')
            lbl = subprocess.run("TERMINAL_ID=$(qdbus org.kde.yakuake /yakuake/sessions org.kde.yakuake.terminalIdsForSessionId "+sess_id+")  ; echo $TERMINAL_ID", shell =True, stdout=subprocess.PIPE)
            term_id=lbl.stdout.decode("utf-8").replace('\n','')

            lcl = subprocess.run('qdbus org.kde.yakuake /yakuake/tabs  setTabTitle '+sess_id+' "SUPERTUXKART"', shell =True, stdout=subprocess.PIPE)
            ldl = subprocess.run('qdbus org.kde.yakuake /yakuake/sessions runCommandInTerminal '+term_id+' "chdir '+self._the_command[1]+'"', shell =True, stdout=subprocess.PIPE)
            lel = subprocess.run('qdbus org.kde.yakuake /yakuake/sessions runCommandInTerminal '+term_id+' "'+self._the_command[0]+'"', shell =True, stdout=subprocess.PIPE)
        time.sleep(3)
        running_stk = True
        while running_stk:
            lfl = subprocess.run("pidof "+self._the_command[2].replace("/",""), shell =True, stdout=subprocess.PIPE)
            process_id=lfl.stdout.decode("utf-8").replace('\n','')
            if process_id == "":
                running_stk = False
            time.sleep(0.01)


        evt = GearsEvent(myEVT_GEARS, -1, value=self._revert_list)
        wx.PostEvent(self._parent, evt)








myEVT_ADDONERY = wx.NewEventType()
EVT_ADDONERY = wx.PyEventBinder(myEVT_ADDONERY, 1)
class AddoneryEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value


class AddoneryThread(threading.Thread):
    def __init__(self, parent):
        """
        @param parent: The gui object that should recieve the value
        @param value: value to 'calculate' to
        """
        threading.Thread.__init__(self)
        self._parent = parent
        self._answer = []

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        while libs.settings.lock > 0:
            pass

        the_url = "https://online.supertuxkart.net/downloads/xml/online_assets.xml"
        try:
            request.urlretrieve(the_url, libs.settings.orig_directory+"/tmp_files/online_assets.xml")
        except:
            self._answer.append("Could not retrieve " + the_url + "\n")
        else:
            self._answer.append("OK " + the_url + "\n")

            libs.settings.addon_lib.init_stk_tree()
            libs.settings.addon_lib.init_mytree()

            libs.settings.addon_lib.init_avail_tracks()
            libs.settings.addon_lib.init_installed_tracks()


            libs.settings.addon_lib.upd_track = []
            libs.settings.addon_lib.to_inst_track = []
            libs.settings.addon_lib.upd_arena = []
            libs.settings.addon_lib.to_inst_arena = []

            if libs.settings.addon_lib.installed_tracks != []:
                list_a = [row[0] for row in libs.settings.addon_lib.avail_tracks]
                list_b = [row[0] for row in libs.settings.addon_lib.installed_tracks]

                indexes_online = []
                indexes_offline = []
                for idx,track in enumerate(list_b):
                    try:
                        indices = ([i for i, x in enumerate(list_a) if x == track])
                        maxi = 0
                        idx_online = 0
                    except:
                        pass
                    else:
                        for i in indices:
                            if int(libs.settings.addon_lib.avail_tracks[i][7])>maxi:
                                maxi = int(libs.settings.addon_lib.avail_tracks[i][7])
                                idx_online = i
                        if maxi > int(libs.settings.addon_lib.installed_tracks[idx][2]):
                            libs.settings.addon_lib.upd_track.append(idx_online)


                list_a = [row[0] for row in libs.settings.addon_lib.avail_tracks]
                list_b = [row[0] for row in libs.settings.addon_lib.installed_tracks]

                list_aa = [row[3] for row in libs.settings.addon_lib.avail_tracks]
                last_avail = max(list_aa)
                list_bb = [row[3] for row in libs.settings.addon_lib.installed_tracks]
                last_installed = max(list_bb)

                new_tracks = []

                if last_avail > last_installed:
                    for i, stamps in enumerate(list_aa):
                        if stamps > last_installed:
                            if not(libs.settings.addon_lib.avail_tracks[i][0] in list_b):
                                new_elem=[i,libs.settings.addon_lib.avail_tracks[i][0],libs.settings.addon_lib.avail_tracks[i][1]]
                                if libs.settings.addon_lib.to_inst_track != []:
                                    if libs.settings.addon_lib.to_inst_track[-1][1] == new_elem[1]:
                                        brrr=libs.settings.addon_lib.to_inst_track.pop()
                                libs.settings.addon_lib.to_inst_track.append(new_elem)
                    libs.settings.addon_lib.to_inst_track=[row[0] for row in libs.settings.addon_lib.to_inst_track]

            libs.settings.addon_lib.init_avail_arenas()
            libs.settings.addon_lib.init_installed_arenas()

            if libs.settings.addon_lib.installed_arenas != []:
                list_a = [row[0] for row in libs.settings.addon_lib.avail_arenas]
                list_b = [row[0] for row in libs.settings.addon_lib.installed_arenas]

                indexes_online = []
                indexes_offline = []
                for idx,arena in enumerate(list_b):
                    try:
                        indices = ([i for i, x in enumerate(list_a) if x == arena])
                        maxi = 0
                        idx_online = 0
                    except:
                        pass
                    else:
                        for i in indices:
                            if int(libs.settings.addon_lib.avail_arenas[i][7])>maxi:
                                maxi = int(libs.settings.addon_lib.avail_arenas[i][7])
                                idx_online = i
                        if maxi > int(libs.settings.addon_lib.installed_arenas[idx][2]):
                            libs.settings.addon_lib.upd_arena.append(idx_online)


                list_a = [row[0] for row in libs.settings.addon_lib.avail_arenas]
                list_b = [row[0] for row in libs.settings.addon_lib.installed_arenas]

                list_aa = [row[3] for row in libs.settings.addon_lib.avail_arenas]
                last_avail = max(list_aa)
                list_bb = [row[3] for row in libs.settings.addon_lib.installed_arenas]
                last_installed = max(list_bb)

                new_arenas = []

                if last_avail > last_installed:
                    for i, stamps in enumerate(list_aa):
                        if stamps > last_installed:
                            if not(libs.settings.addon_lib.avail_arenas[i][0] in list_b):
                                new_elem=[i,libs.settings.addon_lib.avail_arenas[i][0],libs.settings.addon_lib.avail_arenas[i][1]]
                                if libs.settings.addon_lib.to_inst_arena != []:
                                    if libs.settings.addon_lib.to_inst_arena[-1][1] == new_elem[1]:
                                        brrr=libs.settings.addon_lib.to_inst_arena.pop()
                                libs.settings.addon_lib.to_inst_arena.append(new_elem)
                    libs.settings.addon_lib.to_inst_arena=[row[0] for row in libs.settings.addon_lib.to_inst_arena]

        evt = AddoneryEvent(myEVT_ADDONERY, -1, value=self._answer)
        wx.PostEvent(self._parent, evt)








myEVT_ADDONUPD = wx.NewEventType()
EVT_ADDONUPD = wx.PyEventBinder(myEVT_ADDONUPD, 1)
class AddonupdEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value



class AddonupdThread(threading.Thread):
    def __init__(self, parent, the_index, the_type, the_method):
        """
        @param parent: The gui object that should recieve the value
        @param value: value to 'calculate' to
        """
        threading.Thread.__init__(self)
        self._parent = parent
        self._answer = []
        self._the_index = the_index
        self._the_type = the_type
        self._the_method = the_method

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """

        if self._the_type == "track":
            if self._the_method == "install":
                self._answer.append("\n# "+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                try:
                    request.urlretrieve(libs.settings.addon_lib.avail_tracks[self._the_index][2], libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][3]+".zip")
                except:
                    self._answer.append("Could not retrieve " + libs.settings.addon_lib.avail_tracks[self._the_index][2])
                else:
                    self._answer.append("OK " + libs.settings.addon_lib.avail_tracks[self._the_index][2])
                    try:
                        if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0]):
                            shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                    except:
                        self._answer.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                    else:
                        self._answer.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                        try:
                            zip_ref = zipfile.ZipFile(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][3]+".zip","r")
                        except:
                            self._answer.append("Error can't open zip file!")
                        else:
                            try:
                                os.makedirs(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0], exist_ok=True)
                            except:
                                self._answer.append("Error can't create target dir!")
                            else:
                                self._answer.append("Will extract in "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                                try:
                                    zip_ref.extractall(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                                except:
                                    self._answer.append("Error can't extract zip!")
                                else:
                                    try:
                                        brrr=shutil.move(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0], os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    except:
                                        self._answer.append("Error in mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    else:
                                        self._answer.append("Done mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                        try:
                                            os.remove(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][3]+".zip")
                                        except:
                                            self._answer.append("Error removing temporary zip file")
                                        else:
                                            self._answer.append("Success updating "+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                                            try:
                                                replacement = '<track name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][8])+'"/>\n'
                                                #open file1 in reading mode
                                                file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                                #open file2 in writing mode
                                                file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                                #read from file1 and write to file2
                                                for line in file1:
                                                    if "</addons>" in line:
                                                        file2.write(replacement)
                                                    file2.write(line)

                                                #close file1 and file2
                                                file1.close()
                                                file2.close()
                                                os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                                os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            except:
                                                self._answer.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            else:
                                                self._answer.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
            if self._the_method == "update":
                self._answer.append("\n# "+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                try:
                    request.urlretrieve(libs.settings.addon_lib.avail_tracks[self._the_index][2], libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][3]+".zip")
                except:
                    self._answer.append("Could not retrieve " + libs.settings.addon_lib.avail_tracks[self._the_index][2])
                else:
                    self._answer.append("OK " + libs.settings.addon_lib.avail_tracks[self._the_index][2])
                    try:
                        if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0]):
                            shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                    except:
                        self._answer.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                    else:
                        self._answer.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                        try:
                            zip_ref = zipfile.ZipFile(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][3]+".zip","r")
                        except:
                            self._answer.append("Error can't open zip file!")
                        else:
                            try:
                                os.makedirs(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0], exist_ok=True)
                            except:
                                self._answer.append("Error can't create target dir!")
                            else:
                                self._answer.append("Will extract in "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                                try:
                                    zip_ref.extractall(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                                except:
                                    self._answer.append("Error can't extract zip!")
                                else:
                                    try:
                                        brrr=shutil.move(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0], os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    except:
                                        self._answer.append("Error in mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    else:
                                        self._answer.append("Done mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                        try:
                                            os.remove(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_tracks[self._the_index][3]+".zip")
                                        except:
                                            self._answer.append("Error removing temporary zip file")
                                        else:
                                            self._answer.append("Success updating "+libs.settings.addon_lib.avail_tracks[self._the_index][0])
                                            try:
                                                replacement = '<track name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_tracks[self._the_index][8])+'"/>\n'
                                                #open file1 in reading mode
                                                file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                                #open file2 in writing mode
                                                file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                                #read from file1 and write to file2
                                                for line in file1:
                                                    if "track" in line and libs.settings.addon_lib.avail_tracks[self._the_index][0] in line:
                                                        file2.write(replacement)
                                                    else:
                                                        file2.write(line)

                                                #close file1 and file2
                                                file1.close()
                                                file2.close()
                                                os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                                os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            except:
                                                self._answer.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            else:
                                                self._answer.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')

        elif self._the_type == "arena":
            if self._the_method == "install":
                self._answer.append("\n# "+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                try:
                    request.urlretrieve(libs.settings.addon_lib.avail_arenas[self._the_index][2], libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][3]+".zip")
                except:
                    self._answer.append("Could not retrieve " + libs.settings.addon_lib.avail_arenas[self._the_index][2])
                else:
                    self._answer.append("OK " + libs.settings.addon_lib.avail_arenas[self._the_index][2])
                    try:
                        if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0]):
                            shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                    except:
                        self._answer.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                    else:
                        self._answer.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                        try:
                            zip_ref = zipfile.ZipFile(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][3]+".zip","r")
                        except:
                            self._answer.append("Error can't open zip file!")
                        else:
                            try:
                                os.makedirs(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0], exist_ok=True)
                            except:
                                self._answer.append("Error can't create target dir!")
                            else:
                                self._answer.append("Will extract in "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                                try:
                                    zip_ref.extractall(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                                except:
                                    self._answer.append("Error can't extract zip!")
                                else:
                                    try:
                                        brrr=shutil.move(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0], os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    except:
                                        self._answer.append("Error in mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    else:
                                        self._answer.append("Done mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                        try:
                                            os.remove(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][3]+".zip")
                                        except:
                                            self._answer.append("Error removing temporary zip file")
                                        else:
                                            self._answer.append("Success updating "+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                                            try:
                                                replacement = '<arena name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][8])+'"/>\n'
                                                #open file1 in reading mode
                                                file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                                #open file2 in writing mode
                                                file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                                #read from file1 and write to file2
                                                for line in file1:
                                                    if "</addons>" in line:
                                                        file2.write(replacement)
                                                    file2.write(line)

                                                #close file1 and file2
                                                file1.close()
                                                file2.close()
                                                os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                                os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            except:
                                                self._answer.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            else:
                                                self._answer.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
            if self._the_method == "update":
                self._answer.append("\n# "+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                try:
                    request.urlretrieve(libs.settings.addon_lib.avail_arenas[self._the_index][2], libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][3]+".zip")
                except:
                    self._answer.append("Could not retrieve " + libs.settings.addon_lib.avail_arenas[self._the_index][2])
                else:
                    self._answer.append("OK " + libs.settings.addon_lib.avail_arenas[self._the_index][2])
                    try:
                        if os.path.isdir(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0]):
                            shutil.rmtree(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                    except:
                        self._answer.append("Error at rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                    else:
                        self._answer.append("rm -R "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/'+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                        try:
                            zip_ref = zipfile.ZipFile(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][3]+".zip","r")
                        except:
                            self._answer.append("Error can't open zip file!")
                        else:
                            try:
                                os.makedirs(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0], exist_ok=True)
                            except:
                                self._answer.append("Error can't create target dir!")
                            else:
                                self._answer.append("Will extract in "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                                try:
                                    zip_ref.extractall(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                                except:
                                    self._answer.append("Error can't extract zip!")
                                else:
                                    try:
                                        brrr=shutil.move(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0], os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    except:
                                        self._answer.append("Error in mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                    else:
                                        self._answer.append("Done mv "+libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][0]+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/tracks/')
                                        try:
                                            os.remove(libs.settings.orig_directory+"/tmp_files/"+libs.settings.addon_lib.avail_arenas[self._the_index][3]+".zip")
                                        except:
                                            self._answer.append("Error removing temporary zip file")
                                        else:
                                            self._answer.append("Success updating "+libs.settings.addon_lib.avail_arenas[self._the_index][0])
                                            try:
                                                replacement = '<arena name="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][1])+'" id="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][0])+'" designer="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][5])+'" date="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][3])+'" installed="true" installed-revision="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][7])+'" size="'+libs.helpers.parser_of_the_year(libs.settings.addon_lib.avail_arenas[self._the_index][8])+'"/>'
                                                #open file1 in reading mode
                                                file1 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml', 'r')
                                                #open file2 in writing mode
                                                file2 = open(os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2','w')
                                                #read from file1 and write to file2
                                                for line in file1:
                                                    if "arena" in line and libs.settings.addon_lib.avail_arenas[self._the_index][0] in line:
                                                        file2.write(replacement)
                                                    else:
                                                        file2.write(line)

                                                #close file1 and file2
                                                file1.close()
                                                file2.close()
                                                os.system("rm "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                                os.system("mv "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml2'+" "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            except:
                                                self._answer.append("Error updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')
                                            else:
                                                self._answer.append("Success updating "+os.path.expanduser('~')+'/.local/share/supertuxkart/addons/addons_installed.xml')

        evt = AddonupdEvent(myEVT_ADDONUPD, -1, value=self._answer)
        wx.PostEvent(self._parent, evt)

        # libs.settings.lock = libs.settings.lock -1


