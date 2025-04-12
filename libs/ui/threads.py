# -*- coding: utf-8 -*-

# gui threads

import wx
import threading
import subprocess
import libs.common
import libs.variables
import time
import psutil, os

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
        self._answer = []

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        self._answer = libs.common.dl_file(self._url,self._name)
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
            process = subprocess.run('konsole --noclose -e /bin/bash --rcfile <(echo "'+self._the_command[0]+'")', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
            try:
                running_stk = False
                process = [proc.pid for proc in psutil.process_iter() if proc.name() == self._the_command[2].replace("/","")]
                for elem in process:
                    time.sleep(0.25)
                    try:
                        os.kill(elem,0)
                        running_stk = True
                    except:
                        pass
            except:
                pass

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
        while libs.variables.lock > 0:
            pass

        self._answer=libs.common.update_addon_database()

        evt = AddoneryEvent(myEVT_ADDONERY, -1, value=self._answer)
        wx.PostEvent(self._parent, evt)




myEVT_ONLINERY = wx.NewEventType()
EVT_ONLINERY = wx.PyEventBinder(myEVT_ONLINERY, 1)
class OnlineryEvent(wx.PyCommandEvent):
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


class OnlineryThread(threading.Thread):
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
        while libs.variables.lock > 0:
            pass

        self._answer=libs.common.update_online_database()

        evt = OnlineryEvent(myEVT_ONLINERY, -1, value=self._answer)
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

        self._answer = libs.common.get_addon(self._the_index,self._the_type,self._the_method)


        evt = AddonupdEvent(myEVT_ADDONUPD, -1, value=self._answer)
        wx.PostEvent(self._parent, evt)

        # libs.variables.lock = libs.variables.lock -1


