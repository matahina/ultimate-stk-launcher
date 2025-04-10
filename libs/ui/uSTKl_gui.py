# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Ultimate STK Launcher"), pos = wx.DefaultPosition, size = wx.Size( 800,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 800,700 ), wx.DefaultSize )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook6 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP )
        self.m_panel1 = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        gSizer3 = wx.GridSizer( 1, 2, 5, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Profile:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer7.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND|wx.LEFT, 5 )

        m_choice1Choices = [ _(u"GIT"), _(u"NORMAL"), _(u"KIMDEN") ]
        self.m_choice1 = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( 0 )
        bSizer7.Add( self.m_choice1, 1, wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )

        self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Powerup:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        bSizer7.Add( self.m_staticText2, 0, wx.ALL|wx.EXPAND|wx.LEFT, 5 )

        m_choice2Choices = [ _(u"STANDARD"), _(u"RANDOM"), _(u"CAKE") ]
        self.m_choice2 = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
        self.m_choice2.SetSelection( 0 )
        bSizer7.Add( self.m_choice2, 1, wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )

        self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Additional options:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        bSizer7.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND|wx.LEFT, 5 )


        bSizer8.Add( bSizer7, 0, wx.EXPAND, 5 )

        gSizer31 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_checkBox1 = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"Drivelines"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer31.Add( self.m_checkBox1, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND, 5 )

        self.m_checkBox2 = wx.CheckBox( self.m_panel1, wx.ID_ANY, _(u"Checklines"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer31.Add( self.m_checkBox2, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND, 5 )


        bSizer8.Add( gSizer31, 0, 0, 5 )


        bSizer8.Add( ( 0, 20), 1, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, _(u"Start!"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.m_button2.SetDefault()

        self.m_button2.SetBitmap( wx.NullBitmap )
        bSizer6.Add( self.m_button2, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer8.Add( bSizer6, 0, wx.EXPAND, 5 )

        bSizer81 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self.m_panel1, wx.ID_ANY, _(u"Terminal:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        bSizer81.Add( self.m_staticText8, 0, wx.ALL|wx.EXPAND, 5 )

        m_choice3Choices = [ _(u"No terminal") ]
        self.m_choice3 = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
        self.m_choice3.SetSelection( 0 )
        bSizer81.Add( self.m_choice3, 0, wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )


        bSizer8.Add( bSizer81, 0, wx.ALIGN_TOP|wx.EXPAND, 5 )


        gSizer3.Add( bSizer8, 1, wx.EXPAND|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5 )

        sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"Addonery!") ), wx.VERTICAL )

        gSizer32 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_staticText4 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"No addon track to update"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( 1 )

        gSizer32.Add( self.m_staticText4, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_button21 = wx.Button( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"Update"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer32.Add( self.m_button21, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText5 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"No new addon track to install"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        gSizer32.Add( self.m_staticText5, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_button3 = wx.Button( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"Install"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer32.Add( self.m_button3, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText6 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"Powerups seem okay"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        gSizer32.Add( self.m_staticText6, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_button4 = wx.Button( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer32.Add( self.m_button4, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_staticText7 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"No Git/SVN update found"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        gSizer32.Add( self.m_staticText7, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_button5 = wx.Button( sbSizer8.GetStaticBox(), wx.ID_ANY, _(u"Manage"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer32.Add( self.m_button5, 1, wx.ALL|wx.ALIGN_RIGHT, 5 )


        sbSizer8.Add( gSizer32, 0, wx.EXPAND, 5 )


        gSizer3.Add( sbSizer8, 0, wx.EXPAND, 5 )


        bSizer3.Add( gSizer3, 1, wx.EXPAND, 5 )


        self.m_panel1.SetSizer( bSizer3 )
        self.m_panel1.Layout()
        bSizer3.Fit( self.m_panel1 )
        self.m_notebook6.AddPage( self.m_panel1, _(u"Welcome"), False )
        self.m_panel2 = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer71 = wx.BoxSizer( wx.VERTICAL )

        self.m_grid1 = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )

        # Grid
        self.m_grid1.CreateGrid( 0, 0 )
        self.m_grid1.EnableEditing( True )
        self.m_grid1.EnableGridLines( True )
        self.m_grid1.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
        self.m_grid1.EnableDragGridSize( False )
        self.m_grid1.SetMargins( 0, 0 )

        # Columns
        self.m_grid1.EnableDragColMove( False )
        self.m_grid1.EnableDragColSize( True )
        self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Rows
        self.m_grid1.EnableDragRowSize( False )
        self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

        # Label Appearance

        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer71.Add( self.m_grid1, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, _(u"Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer71.Add( self.m_button6, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer71 )
        self.m_panel2.Layout()
        bSizer71.Fit( self.m_panel2 )
        self.m_notebook6.AddPage( self.m_panel2, _(u"Addon Manager"), False )
        self.m_panel3 = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_notebook6.AddPage( self.m_panel3, _(u"Profile Manager"), False )
        self.m_panel4 = wx.Panel( self.m_notebook6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer82 = wx.BoxSizer( wx.VERTICAL )

        self.m_treeCtrl1 = wx.TreeCtrl( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        bSizer82.Add( self.m_treeCtrl1, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button7 = wx.Button( self.m_panel4, wx.ID_ANY, _(u"Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer82.Add( self.m_button7, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_panel4.SetSizer( bSizer82 )
        self.m_panel4.Layout()
        bSizer82.Fit( self.m_panel4 )
        self.m_notebook6.AddPage( self.m_panel4, _(u"Who's online?"), True )

        bSizer2.Add( self.m_notebook6, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, _(u"      /\\_)o<        💜💜💜💜💜💜💜💜💜 WELCOME TO THE Ultimate STK Launcher 💜💜💜💜💜💜💜💜💜\n     |      \\\n     | O . O|\n      \\_____/\n"), wx.DefaultPosition, wx.Size( -1,155 ), wx.TE_MULTILINE|wx.TE_READONLY )
        self.m_textCtrl3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_textCtrl3.SetForegroundColour( wx.Colour( 255, 255, 254 ) )
        self.m_textCtrl3.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
        self.m_textCtrl3.SetMinSize( wx.Size( -1,155 ) )
        self.m_textCtrl3.SetMaxSize( wx.Size( -1,155 ) )

        bSizer2.Add( self.m_textCtrl3, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.goo )
        self.m_button21.Bind( wx.EVT_BUTTON, self.go_tab_addon )
        self.m_button3.Bind( wx.EVT_BUTTON, self.go_tab_addon )
        self.m_button4.Bind( wx.EVT_BUTTON, self.pup_refresh )
        self.m_button5.Bind( wx.EVT_BUTTON, self.go_tab_profiles )
        self.m_button6.Bind( wx.EVT_BUTTON, self.updatery )
        self.m_button7.Bind( wx.EVT_BUTTON, self.uponline )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def goo( self, event ):
        event.Skip()

    def go_tab_addon( self, event ):
        event.Skip()


    def pup_refresh( self, event ):
        event.Skip()

    def go_tab_profiles( self, event ):
        event.Skip()

    def updatery( self, event ):
        event.Skip()

    def uponline( self, event ):
        event.Skip()


