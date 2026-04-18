import pylast
import spotipy
from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import *
from ttkbootstrap.constants import *
from pylast import PlayedTrack, TopItem, User
from funcMenu import FuncMenu
import os
#import ttkbootstrap

class MainWindow:
    #functions
    ##old funcs
    def printTracks(self, tracks: list[PlayedTrack] | list[TopItem], lim: int | None = None):
        if isinstance(tracks[0], PlayedTrack):
            self.printRecents(tracks)
        else:
            if lim == None:
                self.printTops(tracks)
            else:
                self.printTops(tracks, lim)

    def printRecents(self, tracks: list[PlayedTrack]):
        for i in enumerate(tracks):
            print(i[1][0])
            self.allSongList.append(i[1][0])
        self.allSongListVar.set(self.allSongList)

    def printTops(self, tracks: list[PlayedTrack], lim: int | None = None):
        if lim == None:
            for i in enumerate(tracks):
                print(str(i[1][0]) + ": " + str(i[1][1]) + " listens")
        else:
            i = 0
            while i < lim and i < len(tracks):
                print(str(tracks[i][0]) + ": " + str(tracks[i][1]) + " listens")
                i+=1

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
        self.allSongListVar.set([])
        self.playlistListVar.set([])

    def addSongs(self):
        plLVTemp = []
        songIndices = self.allSongListbox.curselection()
        for songInd in songIndices:
            if self.allSongList[songInd] in self.playlistList and not self.dupeCheck:
                self.openDupes()
            if self.allSongList[songInd] in self.playlistList and self.allowDupes.get():
                self.playlistList.append(self.allSongList[songInd])
            if self.allSongList[songInd] not in self.playlistList:
                self.playlistList.append(self.allSongList[songInd])
        for song in self.playlistList:
            plLVTemp.append(song.item)
        self.playlistListVar.set(plLVTemp)

    def removeSongs(self):
        plLVTemp = []
        songIndices = list(self.playlistListbox.curselection())
        songIndices.reverse()
        for songInd in songIndices:
            self.playlistList.pop(songInd)
        for song in self.playlistList:
            plLVTemp.append(song.item)
        self.playlistListVar.set(plLVTemp)

    def moveSongsUp(self):
        plLVTemp = []
        newCursorList = []
        offset = False
        songIndices = list(self.playlistListbox.curselection())
        for songInd in songIndices:
            idxTarget = songInd - 1
            if offset:
                pass
            elif idxTarget == -1:
                idxTarget = len(self.playlistList) - 1
                self.playlistList = list(self.playlistList[1:] + [self.playlistList[songInd]])
                offset = True
            else:
                self.playlistList[songInd], self.playlistList[idxTarget] = self.playlistList[idxTarget], self.playlistList[songInd]
            newCursorList.append(idxTarget)
        for song in self.playlistList:
            plLVTemp.append(song.item)
        self.playlistListVar.set(plLVTemp)
        self.playlistListbox.select_clear(0, len(self.playlistList))
        for target in newCursorList:
            self.playlistListbox.select_set(target)
    
    def moveSongsDown(self):
        plLVTemp = []
        newCursorList = []
        offset = False
        songIndices = list(self.playlistListbox.curselection())
        songIndices.reverse()
        for songInd in songIndices:
            idxTarget = songInd + 1
            if offset:
                pass
            elif idxTarget == len(self.playlistList):
                idxTarget = 0
                self.playlistList = list([self.playlistList[songInd]] + self.playlistList[:-1])
                offset = True
            else:
                self.playlistList[songInd], self.playlistList[idxTarget] = self.playlistList[idxTarget], self.playlistList[songInd]
            newCursorList.append(idxTarget)
        for song in self.playlistList:
            plLVTemp.append(song.item)
        self.playlistListVar.set(plLVTemp)
        self.playlistListbox.select_clear(0, len(self.playlistList))
        for target in newCursorList:
            self.playlistListbox.select_set(target)

    def sortSongsAlphTitle(self, list: list[TopItem], type: str):
        tempList = []
        if sorted(list, key=lambda song : song.item.title.lower()) == list:
            list.sort(key=lambda song : song.item.title.lower(), reverse=True)
        else: list.sort(key=lambda song : song.item.title.lower())
        for song in list:
            tempList.append(str(song.item))
        if type == "allSongList":
            self.allSongListVar.set(tempList)
            self.allSongListbox.select_clear(0, len(self.allSongList))
        elif type == "playlistList":
            self.playlistListVar.set(tempList)
            self.playlistListbox.select_clear(0, len(self.playlistList))

    def sortSongsAlphArtist(self, list: list[TopItem], type: str):
        tempList = []
        if sorted(list, key=lambda song : str(song.item.artist).lower()) == list:
            list.sort(key=lambda song : str(song.item.artist).lower(), reverse=True)
        else: list.sort(key=lambda song : str(song.item.artist).lower())
        for song in list:
            tempList.append(str(song.item))
        if type == "allSongList":
            self.allSongListVar.set(tempList)
            self.allSongListbox.select_clear(0, len(self.allSongList))
        elif type == "playlistList":
            self.playlistListVar.set(tempList)
            self.playlistListbox.select_clear(0, len(self.playlistList))

    def weightedSort(self):
        tempList = []
        if self.allSongList == self.weightedList: self.allSongList.reverse()
        else: 
            self.allSongList.clear()
            for song in self.weightedList:
                self.allSongList.append(song)
        for song in self.allSongList:
            tempList.append(str(song[0])+": "+str(song[1])+" listens")
        self.allSongListVar.set(tempList)
        self.allSongListbox.select_clear(0, len(self.allSongList))
    
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
        for but in self.playlistButtons:
            but.state(['disabled'])
        for but in self.songListButtons:
            but.state(['disabled'])
        for but in self.programButtons:
            but.state(['disabled'])

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
            self.activateSongButtons()
            self.activatePlaylistButtons()
            self.activateProgramButtons()
            self.topDefaultTimeframeConstructor()
            self.topTimeframeConstructor()
            self.recentSongsConstructor()
        except TclError as e:
            print(f"window die: {e}")

    def activateSongButtons(self):
        for but in self.songListButtons:
            but.state(['!disabled'])

    def activatePlaylistButtons(self):
        for but in self.playlistButtons:
            but.state(['!disabled'])

    def activateProgramButtons(self):
        for but in self.programButtons:
            but.state(['!disabled'])

    ##func menu constructors
    def topDefaultTimeframeConstructor(self):
        if self.tdtMenu == None:
            self.tdtMenu = FuncMenu(self.topDefaultMenu, self.root, self.user, "topDefaultTimeframe", self.timeframeVar, self.songCountVar, self.allSongList, self.allSongListVar, self.weightedList)
            self.tdtMenu.setup()

    def topTimeframeConstructor(self):
        if self.tfMenu == None:
            self.tfMenu = FuncMenu(self.topTimeframeMenu, self.root, self.user, "topCustomTimeframe", self.timeframeVar, self.songCountVar, self.allSongList, self.allSongListVar, self.weightedList)
            self.tfMenu.setup()

    def recentSongsConstructor(self):
        if self.rsMenu == None:
            self.rsMenu = FuncMenu(self.recentSongsMenu, self.root, self.user, "recentSongs", self.timeframeVar, self.songCountVar, self.allSongList, self.allSongListVar, self.weightedList)
            self.rsMenu.setup()

    ##window opener
    def createWindow(self, winType: str):
        if winType == "login":
            from loginWindow import LoginWindow
            self.loginWindow = LoginWindow(parent=self)
            self.root.wait_window(self.loginWindow.loginWindow)
        elif winType == "export":
            from exportWindow import ExportWindow
            self.exportWindow = ExportWindow(parent=self, songList=self.playlistListVar.get())
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

    #the program
    def __init__(self, root: Window, sp: spotipy.Spotify | None, network: pylast.LastFMNetwork | None, user: pylast.User | None):
        self.root = root
        self.root.title("Scrobblefy")
        self.root.geometry('1300x900')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.interceptClose)

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
        self.weightedList: list[TopItem] = []
        self.playlistList = []
        self.playlistListVar = StringVar()
        self.songListButtons = []
        self.playlistButtons = []
        self.programButtons = []

        baseFrame = Frame(self.root, padding = 10)
        baseFrame.columnconfigure(0, weight=3)
        baseFrame.columnconfigure(1, weight=1)
        baseFrame.columnconfigure(2, weight=3)
        baseFrame.rowconfigure(0, weight=1)
        baseFrame.rowconfigure(1, weight=2)
        baseFrame.grid(sticky=NSEW)

        leftColumn = Frame(baseFrame, padding = 10)
        leftColumn.grid(row = 0, column = 0, sticky=NW)
        leftColumn.columnconfigure(0, weight=1, minsize=200)
        leftColumn.columnconfigure(1, weight=1)
        leftColumn.rowconfigure(1, weight=1)

        buttonColumn = Frame(baseFrame, padding = 10)
        buttonColumn.grid(row = 0, column = 1, sticky = NS)
        buttonColumn.columnconfigure(0, weight=1, minsize=200)
        buttonColumn.rowconfigure(0, weight=1)
        buttonColumn.rowconfigure(1, weight=1)
        buttonColumn.rowconfigure(2, weight=1)
        buttonColumn.rowconfigure(3, weight=8)

        rightColumn = Frame(baseFrame, padding = 10)
        rightColumn.grid(row = 0, column = 2, sticky=NE)
        rightColumn.columnconfigure(0, weight=1)
        rightColumn.rowconfigure(0, weight=1)

        #left column
        allSongLabel = Label(leftColumn, text="Last.fm Results")
        allSongLabel.grid(column = 0, row = 0, sticky = NSEW)
        self.allSongListbox = Listbox(leftColumn, listvariable=self.allSongListVar, width = 80, height = 30, selectmode = EXTENDED)
        self.allSongListbox.grid(column = 0, row = 1, sticky = NSEW)
        self.allSongListboxScrollbar = Scrollbar(leftColumn, orient=VERTICAL, command=self.allSongListbox.yview)
        self.allSongListboxScrollbar.grid(column = 1, row = 1, sticky=NS)
        self.allSongListbox.configure(yscrollcommand=self.allSongListboxScrollbar.set)

        #center column with buttons
        songListButtonFrame = Labelframe(buttonColumn, text="Results List Options:")
        songListButtonFrame.grid(sticky=(N,EW))
        addSongsButton = Button(songListButtonFrame, text = "Add Song(s) to Playlist", command=self.addSongs)
        self.songListButtons.append(addSongsButton)
        sortSongsAlphTitleButton = Button(songListButtonFrame, text = "Sort Songs by Title", command=lambda: self.sortSongsAlphTitle(self.allSongList, "allSongList"))
        self.songListButtons.append(sortSongsAlphTitleButton)
        sortSongsAlphArtistButton = Button(songListButtonFrame, text = "Sort Songs by Artist", command=lambda: self.sortSongsAlphArtist(self.allSongList, "allSongList"))
        self.songListButtons.append(sortSongsAlphArtistButton)
        weightedSortButton = Button(songListButtonFrame, text = "Sort Songs by Listens", command=lambda: self.weightedSort())
        self.songListButtons.append(weightedSortButton)
        printListButton = Button(songListButtonFrame, text = "Print List", command=lambda: self.getList())
        self.songListButtons.append(printListButton)
        for but in self.songListButtons:
            but.grid(sticky = NSEW)
            but.state(['disabled'])

        playlistButtonFrame = Labelframe(buttonColumn, text="Playlist Options:")
        playlistButtonFrame.grid(column = 0, row = 1, sticky=(N,EW))
        removeSongsButton = Button(playlistButtonFrame, text = "Remove Song(s) from Playlist", command=self.removeSongs)
        self.playlistButtons.append(removeSongsButton)
        moveSongsUpButton = Button(playlistButtonFrame, text = "Move Song(s) Up", command=self.moveSongsUp)
        self.playlistButtons.append(moveSongsUpButton)
        moveSongsDownButton = Button(playlistButtonFrame, text = "Move Song(s) Down", command=self.moveSongsDown)
        self.playlistButtons.append(moveSongsDownButton)
        sortPlaylistAlphTitleButton = Button(playlistButtonFrame, text = "Sort Songs by Title", command=lambda: self.sortSongsAlphTitle(self.playlistList, "playlistList"))
        self.playlistButtons.append(sortPlaylistAlphTitleButton)
        sortPlaylistAlphArtistButton = Button(playlistButtonFrame, text = "Sort Songs by Artist", command=lambda: self.sortSongsAlphArtist(self.playlistList, "playlistList"))
        self.playlistButtons.append(sortPlaylistAlphArtistButton)
        openDupesButton = Button(playlistButtonFrame, text = "Open Duplicate Option Menu", command=self.openDupes)
        self.playlistButtons.append(openDupesButton)
        exportPlaylistButton = Button(playlistButtonFrame, text = "Export Playlist to Spotify", command=self.exportPlaylist, bootstyle="success")
        self.playlistButtons.append(exportPlaylistButton)
        for but in self.playlistButtons:
            but.grid(sticky = NSEW)
            but.state(['disabled'])

        programButtonFrame = Labelframe(buttonColumn, text = "Program Options")
        programButtonFrame.grid(column = 0, row = 2, sticky = (N,EW))
        backToLoginButton = Button(programButtonFrame, text = "Return to Login Screen", command=self.createLogin)
        self.programButtons.append(backToLoginButton)
        programHelpButton = Button(programButtonFrame, text = "Open Help Window", command=self.openHelp)
        self.programButtons.append(programHelpButton)
        for but in self.programButtons:
            but.grid(sticky = NSEW)
            but.state(['disabled'])

        #right column
        playlistLabel = Label(rightColumn, text="Playlist")
        playlistLabel.grid(column = 0, row = 0, sticky = NSEW)
        self.playlistListbox = Listbox(rightColumn, listvariable=self.playlistListVar, width = 80, height = 30, selectmode=EXTENDED)
        self.playlistListbox.grid(column = 0, row = 1)
        self.playlistListboxScrollbar = Scrollbar(rightColumn, orient=VERTICAL, command=self.playlistListbox.yview)
        self.playlistListboxScrollbar.grid(column = 1, row = 1, sticky=NS)
        self.playlistListbox.configure(yscrollcommand=self.playlistListboxScrollbar.set)

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
            but.grid(column = 0, row = butTup[0]*2, sticky=(N, EW))
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