import pylast
import spotipy
from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import *
from ttkbootstrap.widgets.tableview import *
from ttkbootstrap.constants import *
from pylast import PlayedTrack, TopItem, User
from funcMenu import FuncMenu
import os
#import ttkbootstrap

class MainWindow:
    #functions
    ##button onpress funcs
    def topDefault(self):
        if(self.topDefaultMenu.grid_info()):
            self.topDefaultMenu.grid_forget()
        else:
            self.forgetMenus()
            self.topDefaultMenu.grid(column = 0, row = 1, sticky = EW, pady=10)

    def topTimeframe(self):
        if(self.topTimeframeMenu.grid_info()):
            self.topTimeframeMenu.grid_forget()
        else:
            self.forgetMenus()
            self.topTimeframeMenu.grid(column = 0, row = 3, sticky = EW, pady=10)

    def recentSongs(self):
        if(self.recentSongsMenu.grid_info()):
            self.recentSongsMenu.grid_forget()
        else:
            self.forgetMenus()
            self.recentSongsMenu.grid(column = 0, row = 5, sticky = EW, pady=10)

    def clearSongs(self):
        self.allSongTable.build_table_data(coldata=[
                            {"text": "Title", "width": "400", "stretch": True}, 
                            {"text": "Artist", "width": "300", "stretch": True}, 
                            {"text": "Listens", "width": "100", "stretch": True}
                            ], 
                        rowdata=[])
        self.playlistTable.build_table_data(coldata=[
                            {"text": "Title", "width": "400", "stretch": True}, 
                            {"text": "Artist", "width": "300", "stretch": True}, 
                            {"text": "Listens", "width": "100", "stretch": True}
                            ], 
                        rowdata=[])

    def addSongs(self):
        playlistSongs = []
        for song in self.playlistTable.get_rows():
            playlistSongs.append(song.values)
        songsToAdd = self.allSongTable.get_rows(selected=True)
        for song in songsToAdd:
            added = False
            toAdd = True
            for targets in self.playlistTable.get_rows():
                if song.values == targets.values and not self.dupeCheck:
                    self.openDupes()
                if song.values == targets.values and not added:
                    if self.allowDupes.get():
                        playlistSongs.append(list(song.values))
                        added = True
                    else:
                        toAdd = False
            if not added and toAdd:
                playlistSongs.append(list(song.values))
        self.buildPlaylistTable(playlistSongs)
    
    def getList(self):
        print(self.allSongList)

    def openDupes(self):
        self.dupeCheck = True
        self.createWindow("dupeAsk")

    def openHelp(self):
        self.createWindow("help")

    def exportPlaylist(self):
        self.createWindow("export")

    ##more utility functions
    def forgetMenus(self):
        for menu in self.funcMenus:
            menu.grid_forget()

    def deactivateButtons(self):
        for but in self.funcButtons:
            but.state(['disabled'])
        for but in self.optionButtons:
            but.state(['disabled'])
        for but in self.programButtons:
            but.state(['disabled'])
        self.dupeCheckbox.state(['disabled'])

    def emptyMenus(self):
        self.tdtMenu = None
        self.tfMenu = None
        self.rsMenu = None
        for menu in self.funcMenus:
            while len(menu.children.values()) > 0:
                firstKey = next(iter(menu.children))
                menu.children[firstKey].destroy()
            
    def forgetAllFuncs(self):
        self.clearSongs()
        self.forgetMenus()
        self.deactivateButtons()
        self.emptyMenus()
            
    def activateUserButtons(self):
        try:
            self.root.attributes(topmost=False)
            self.forgetAllFuncs()
            for but in self.funcButtons:
                but.state(['!disabled'])
            self.activateOptionButtons()
            self.topDefaultTimeframeConstructor()
            self.topTimeframeConstructor()
            self.recentSongsConstructor()
        except TclError as e:
            print(f"window die: {e}")

    def activateOptionButtons(self):
        for but in self.optionButtons:
            but.state(['!disabled'])
        self.dupeCheckbox.state(['!disabled'])

    ##func menu constructors
    def topDefaultTimeframeConstructor(self):
        if self.tdtMenu == None:
            self.tdtMenu = FuncMenu(self.topDefaultMenu, self.root, self.user, "topDefaultTimeframe", self.timeframeVar, self.songCountVar, self.allSongList, self.allSongTable)
            self.tdtMenu.setup()

    def topTimeframeConstructor(self):
        if self.tfMenu == None:
            self.tfMenu = FuncMenu(self.topTimeframeMenu, self.root, self.user, "topCustomTimeframe", self.timeframeVar, self.songCountVar, self.allSongList, self.allSongTable)
            self.tfMenu.setup()

    def recentSongsConstructor(self):
        if self.rsMenu == None:
            self.rsMenu = FuncMenu(self.recentSongsMenu, self.root, self.user, "recentSongs", self.timeframeVar, self.songCountVar, self.allSongList, self.allSongTable)
            self.rsMenu.setup()

    ##window opener
    def createWindow(self, winType: str):
        if winType == "login":
            from loginWindow import LoginWindow
            self.loginWindow = LoginWindow(parent=self)
            self.root.wait_window(self.loginWindow.loginWindow)
        elif winType == "export":
            from exportWindow import ExportWindow
            songList = []
            for song in self.playlistTable.get_rows():
                songList.append(list(song.values))
            self.exportWindow = ExportWindow(parent=self, songList=songList)
            self.root.wait_window(self.exportWindow.exportWindow)
        elif winType == "dupeAsk":
            from dupeAskWindow import DupeAskWindow
            self.dupeAskWindow = DupeAskWindow(parent=self, allowDupes=self.allowDupes)
            self.root.wait_window(self.dupeAskWindow.dupeAsk)
        elif winType == "help":
            from helpWindow import HelpWindow
            self.helpWindow = HelpWindow(parent=self)

    def createLogin(self):
        self.deactivateButtons()
        self.createWindow("login")
        self.activateUserButtons()

    ##helper funcs
    def setSelected(self, rows):
        self.curselection = list(rows)

    def createTable(self, dest: Frame):
        return Tableview(dest, 
            coldata=[
                {"text": "Title", "width": "400", "stretch": True}, 
                {"text": "Artist", "width": "300", "stretch": True}, 
                {"text": "Listens", "width": "100", "stretch": True}
                ], 
            rowdata=[], 
            bootstyle=PRIMARY,
            height = 25,
            on_select=self.setSelected)

    def buildPlaylistTable(self, rowData: list[list[str]]):
        self.playlistTable.build_table_data(coldata=[
            {"text": "Title", "width": "400", "stretch": True}, 
            {"text": "Artist", "width": "300", "stretch": True}, 
            {"text": "Listens", "width": "100", "stretch": True}
            ], 
        rowdata=rowData)

    #the program
    def __init__(self, root: Window, sp: spotipy.Spotify | None, network: pylast.LastFMNetwork | None, user: pylast.User | None):
        self.root = root
        self.root.title("Scrobblefy")
        self.root.geometry(f'{int(root.winfo_screenwidth()*.75)}x{int(root.winfo_screenheight()*.8)}')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.interceptClose)
        self.root.place_window_center()

        self.user = user
        self.sp = sp
        self.network = network
        self.dupeAskWindow = None
        self.exportWindow = None
        self.loginWindow = None
        self.helpWindow = None
        
        self.loginBefore = False
        self.dupeCheck = False
        self.allowDupes = BooleanVar(value=False)
        self.timeframeVar = StringVar(value = "7day")
        self.songCountVar = IntVar()
        
        self.allSongList = []
        self.allSongListVar = StringVar()
        self.playlistList = []
        self.playlistListVar = StringVar()
        self.optionButtons = []
        self.programButtons = []

        baseFrame = Frame(self.root, padding = 10)
        baseFrame.columnconfigure(0, weight=5)
        baseFrame.columnconfigure(1, weight=1)
        baseFrame.columnconfigure(2, weight=5)
        baseFrame.rowconfigure(0, weight=1)
        baseFrame.rowconfigure(1, weight=1)
        baseFrame.grid(sticky=NSEW)

        leftColumn = Frame(baseFrame, padding = 10)
        leftColumn.grid(row = 0, column = 0, sticky=(N,EW))
        leftColumn.columnconfigure(0, weight=1)
        leftColumn.rowconfigure(0, weight=1)
        leftColumn.rowconfigure(1, weight=1)
        leftColumn.rowconfigure(2, weight=1)

        buttonColumn = Frame(baseFrame, padding = 10)
        buttonColumn.grid(row = 0, column = 1, sticky = NS)
        buttonColumn.columnconfigure(0, weight=1)
        buttonColumn.rowconfigure(0, weight=1)
        buttonColumn.rowconfigure(1, weight=4)
        buttonColumn.rowconfigure(2, weight=5)

        rightColumn = Frame(baseFrame, padding = 10)
        rightColumn.grid(row = 0, column = 2, sticky=(N,EW))
        rightColumn.columnconfigure(0, weight=1)
        rightColumn.rowconfigure(0, weight=1)
        rightColumn.rowconfigure(1, weight=1)
        rightColumn.rowconfigure(2, weight=1)

        #left column
        allSongLabel = Label(leftColumn, text="Last.fm Results")
        allSongLabel.grid(column = 0, row = 0, sticky = NSEW)
        self.allSongTable = self.createTable(dest=leftColumn)
        self.allSongTable.grid(column = 0, row = 1, sticky = NSEW)

        #center column with add button
        addButtonFrame = Frame(buttonColumn)
        addButtonFrame.grid(column = 0, row = 1, sticky = EW)

        addSongsButton = Button(addButtonFrame, text = "Add Song(s) to Playlist", command=self.addSongs, bootstyle="success")
        self.optionButtons.append(addSongsButton)
        addSongsButton.grid(sticky = NSEW, pady = 2)
        addSongsButton.state(['disabled'])

        #right column
        playlistLabel = Label(rightColumn, text="Playlist")
        playlistLabel.grid(column = 0, row = 0, sticky = NSEW)
        self.playlistTable = self.createTable(dest = rightColumn)
        self.playlistTable.grid(column = 0, row = 1, sticky = NSEW)

        optionsFrame = Frame(rightColumn)
        optionsFrame.rowconfigure(0, weight = 1)
        optionsFrame.rowconfigure(1, weight = 1)
        optionsFrame.rowconfigure(2, weight = 1)
        optionsFrame.columnconfigure(0, weight = 1)
        optionsFrame.columnconfigure(1, weight = 3)
        optionsFrame.grid(column = 0, row = 2, sticky = NSEW)
        dupeFrame = Frame(optionsFrame)
        dupeFrame.grid(row = 0, column = 0, sticky = W)
        dupeCheckboxLabel = Label(dupeFrame, text = "Allow duplicates?")
        self.dupeCheckbox = Checkbutton(dupeFrame, variable=self.allowDupes, padding = 7)
        dupeCheckboxLabel.grid(row = 0, column = 0, sticky = (E, NS), pady = 2)
        self.dupeCheckbox.grid(row = 0, column = 1, sticky = (W, NS), pady = 2)
        self.dupeCheckbox.state(['disabled'])
        exportPlaylistButton = Button(optionsFrame, text = "Export Playlist to Spotify", command=self.exportPlaylist, bootstyle="success")
        exportPlaylistButton.grid(row = 0, column = 1, sticky = EW, pady = 20)
        self.optionButtons.append(exportPlaylistButton)
        backToLoginButton = Button(optionsFrame, text = "Return to Login Screen", command=self.createLogin)
        backToLoginButton.grid(row = 1, column = 0, columnspan=2, sticky = EW)
        self.optionButtons.append(backToLoginButton)
        programHelpButton = Button(optionsFrame, text = "Open Help Window", command=self.openHelp, bootstyle="warning")
        programHelpButton.grid(row = 2, column = 0, columnspan=2, sticky = EW)
        self.optionButtons.append(programHelpButton)
        for but in self.optionButtons:
            but.state(['disabled'])

        #last.fm functions
        funcFrame = Labelframe(leftColumn, padding=10, text = "Last.fm Options")
        funcFrame.grid(column = 0, row = 2, sticky = (N,EW), pady = 10)
        funcFrame.columnconfigure(0, weight=1)
        i=0 
        while i<7: 
            funcFrame.rowconfigure(i, weight=1); i+=1

        self.funcButtons = []
        topDefaultButton = Button(funcFrame, text = "Get Top Songs from Default Timeframe", command=self.topDefault, padding=2)
        topTimeframeButton = Button(funcFrame, text = "Get Top Songs from Custom Timeframe", command=self.topTimeframe, padding=2)
        recentSongsButton = Button(funcFrame, text = "Get Recent Songs", command=self.recentSongs, padding=2)
        clearListButton = Button(funcFrame, text = "Clear Both Lists", command=self.clearSongs, padding=2, bootstyle="danger")
        self.funcButtons.append(topDefaultButton)
        self.funcButtons.append(topTimeframeButton)
        self.funcButtons.append(recentSongsButton)
        self.funcButtons.append(clearListButton)
        for butTup in enumerate(self.funcButtons):
            but = butTup[1]
            but.grid(column = 0, row = butTup[0]*2, sticky=(N, EW), pady = 2)
            but.state(['disabled'])

        self.funcMenus = []
        self.topDefaultMenu = Frame(funcFrame)
        i=0 
        while i<7: 
            self.topDefaultMenu.columnconfigure(i, weight=1); i+=1
        self.topDefaultMenu.rowconfigure(0, weight=1)
        self.topDefaultMenu.rowconfigure(1, weight=1)
        self.topDefaultMenu.rowconfigure(2, weight=1)

        self.topTimeframeMenu = Frame(funcFrame)
        i=0 
        while i<7: 
            self.topTimeframeMenu.columnconfigure(i, weight=1); i+=1
        self.topTimeframeMenu.rowconfigure(0, weight=1)
        self.topTimeframeMenu.rowconfigure(1, weight=1)
        self.topTimeframeMenu.rowconfigure(2, weight=1)

        self.recentSongsMenu = Frame(funcFrame)
        self.recentSongsMenu.columnconfigure(0, weight=1)
        self.recentSongsMenu.rowconfigure(0, weight=1)
        self.recentSongsMenu.rowconfigure(1, weight=1)
        self.recentSongsMenu.rowconfigure(2, weight=1)

        self.funcMenus.append(self.topDefaultMenu)
        self.funcMenus.append(self.topTimeframeMenu)
        self.funcMenus.append(self.recentSongsMenu)

        self.tdtMenu = None
        self.tfMenu = None
        self.rsMenu = None

        self.createLogin()
        self.loginBefore = True
        
    def start(self):
        self.root.mainloop()

    def interceptClose(self):
        if(".cache" in os.listdir(".")):
            os.remove(".cache")
        self.root.destroy()