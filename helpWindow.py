from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import *
from ttkbootstrap.constants import *
import webbrowser
#from ttkbootstrap.scrolled import ScrolledFrame

class HelpWindow:
    def __init__(self, parent):
        self.parent = parent
        self.helpWindow = Toplevel(parent.root)
        self.helpWindow.geometry("450x675")
        self.helpWindow.title("Program Help")
        self.helpWindow.wait_visibility()
        self.helpWindow.grab_set()
        self.helpWindow.columnconfigure(0, weight=1)
        self.helpWindow.rowconfigure(0, weight=1)
        self.helpWindow.resizable(False, False)

        helpFrame = Frame(self.helpWindow, padding = 10)
        helpFrame.grid(column = 0, row = 0, sticky = NSEW)
        helpFrame.columnconfigure(0, weight=1)
        helpFrame.rowconfigure(0, weight=1)
        helpFrame.rowconfigure(1, weight=10)
        helpFrame.rowconfigure(2, weight=1)

        helpLabel = Label(helpFrame, text = "Click on the tabs below to get help for particular parts of the program, or click the Help button at the bottom of the window to be taken to an external webpage.")
        helpLabel.grid(column = 0, row = 0, sticky = (NSEW))
        helpLabel.configure(wraplength=self.helpWindow.winfo_width()-20)
        helpNotebook = Notebook(helpFrame)
        helpNotebook.grid(column = 0, row = 1, sticky = NSEW)
        helpButton = Button(helpFrame, name = "help", text = "More Help", padding=5, command=self.openSite)
        helpButton.grid(column = 0, row = 2, sticky=(EW))

        #loginFrame = ScrolledFrame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        loginFrame = Frame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        #helpNotebook.add(loginFrame.container, text = "Logging In")
        helpNotebook.add(loginFrame, text = "Logging In")
        lfmFrame = Frame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        helpNotebook.add(lfmFrame, text = "Last.fm Features")
        #plistFrame = ScrolledFrame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        plistFrame = Frame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        #helpNotebook.add(plistFrame.container, text = "Playlist Creation")
        helpNotebook.add(plistFrame, text = "Playlist Creation")
        exportFrame = Frame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        helpNotebook.add(exportFrame, text = "Exporting to Spotify")
        moreFrame = Frame(helpNotebook, padding = 5, relief = SOLID, width=self.helpWindow.winfo_width()-10)
        helpNotebook.add(moreFrame, text = "More")

        self.configLoginFrame(loginFrame)
        self.configLfmFrame(lfmFrame)
        self.configPlistFrame(plistFrame)
        self.configExportFrame(exportFrame)
        self.configMoreFrame(moreFrame)

    def configLoginFrame(self, loginFrame: Frame):
        loginFrame.columnconfigure(0, weight = 1)
        loginFrame.rowconfigure(0, weight = 2)
        loginFrame.rowconfigure(1, weight = 4)
        loginFrame.rowconfigure(2, weight = 1)
        loginFrame.rowconfigure(3, weight = 2)
        loginFrame.rowconfigure(4, weight = 4)
        loginFrame.rowconfigure(5, weight = 1)
        loginFrame.rowconfigure(6, weight = 1)
        loginFrame.rowconfigure(7, weight = 2)
        loginFrame.rowconfigure(8, weight = 4)
        loginFrame.rowconfigure(9, weight = 1)

        loginGeneralHelpHeader = Label(loginFrame, text = "General", font=("bold"))
        loginGeneralHelpHeader.grid(column = 0, row = 0, sticky = EW)
        loginGeneralHelpLabel = Label(loginFrame, text = "To use this program, you'll need both a Last.fm account to pull listening data from and a Spotify Premium account. (The Last.fm account doesn't have to be yours!)")
        loginGeneralHelpLabel.grid(column = 0, row = 1, sticky = EW)
        loginGeneralHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        loginSep1 = Separator(loginFrame, orient=HORIZONTAL)
        loginSep1.grid(column = 0, row = 2, sticky = EW)

        loginLfmHelpHeader = Label(loginFrame, text = "Last.fm", font=("bold"))
        loginLfmHelpHeader.grid(column = 0, row = 3, sticky = EW)
        loginLfmHelpLabel = Label(loginFrame, text = "To access Last.fm listening data, all you need is the username attached to the account. If you don't have a Last.fm account and would like to create one, click below to get signed up.")
        loginLfmHelpLabel.grid(column = 0, row = 4, sticky = EW)
        loginLfmHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)
        loginLfmHelpButton = Button(loginFrame, text = "Last.fm Website", command=self.openLastfm)
        loginLfmHelpButton.grid(column = 0, row = 5, sticky = EW)

        loginSep2 = Separator(loginFrame, orient=HORIZONTAL)
        loginSep2.grid(column = 0, row = 6, sticky = EW)

        loginSpotifyHelpHeader = Label(loginFrame, text = "Spotify", font=("bold"))
        loginSpotifyHelpHeader.grid(column = 0, row = 7, sticky = EW)
        loginSpotifyHelpLabel = Label(loginFrame, text = "In order to automatically create playlists with Spotify, you'll need Spotify Premium as well as an API application. Your Client ID will be generated for you after filling out your application, and you should use 'http://127.0.0.1:1410/' or another similar local IP address with an open port as your redirect address. To go to the Developer Dashboard to create an API app, click the Spotify Dev button below. For more help creating an API application, click the More Help button at the bottom of the window.")
        loginSpotifyHelpLabel.grid(column = 0, row = 8, sticky = EW)
        loginSpotifyHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)
        loginSpotifyHelpButton = Button(loginFrame, text = "Spotify Dev Dash", command=self.openSpotifyDev)
        loginSpotifyHelpButton.grid(column = 0, row = 9, sticky = EW)

    def openLastfm(self):
        webbrowser.open_new("https://www.last.fm")

    def openSpotifyDev(self):
        webbrowser.open_new("https://developer.spotify.com/dashboard")

    def openSite(self):
        webbrowser.open_new("https://pbcheesecake.neocities.org/about/help/scrobblefy")

    def configLfmFrame(self, lfmFrame: Frame):
        lfmFrame.columnconfigure(0, weight = 1)
        lfmFrame.rowconfigure(0, weight = 2)
        lfmFrame.rowconfigure(1, weight = 4)
        lfmFrame.rowconfigure(2, weight = 1)
        lfmFrame.rowconfigure(3, weight = 2)
        lfmFrame.rowconfigure(4, weight = 4)
        lfmFrame.rowconfigure(5, weight = 1)
        lfmFrame.rowconfigure(6, weight = 2)
        lfmFrame.rowconfigure(7, weight = 4)
        lfmFrame.rowconfigure(8, weight = 1)
        lfmFrame.rowconfigure(9, weight = 2)
        lfmFrame.rowconfigure(10, weight = 4)
        lfmFrame.rowconfigure(11, weight = 1)

        lfmGeneralHelpHeader = Label(lfmFrame, text = "General", font=("bold"))
        lfmGeneralHelpHeader.grid(column = 0, row = 0, sticky = EW)
        lfmGeneralHelpLabel = Label(lfmFrame, text = "All Last.fm requests have a maximum limit of 1000 items. Leaving the # field at 0 will retrieve as many items as possible. However, this size of request will take time, and the program may appear unresponsive for some time while this request processes.")
        lfmGeneralHelpLabel.grid(column = 0, row = 1, sticky = EW)
        lfmGeneralHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        lfmSep1 = Separator(lfmFrame, orient=HORIZONTAL)
        lfmSep1.grid(column = 0, row = 2, sticky = EW)

        lfmTSDTHelpHeader = Label(lfmFrame, text = "Get Top Songs from Default Timeframe", font=("bold"))
        lfmTSDTHelpHeader.grid(column = 0, row = 3, sticky = EW)
        lfmTSDTHelpLabel = Label(lfmFrame, text = "This function retrieves your top songs from one of several default timeframes. These options include 1 week, 1 month, 3 months, 6 months, 1 year, and the entire lifetime of your Last.fm account.")
        lfmTSDTHelpLabel.grid(column = 0, row = 4, sticky = EW)
        lfmTSDTHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        lfmSep2 = Separator(lfmFrame, orient=HORIZONTAL)
        lfmSep2.grid(column = 0, row = 5, sticky = EW)

        lfmTSCTHelpHeader = Label(lfmFrame, text = "Get Top Songs from Custom Timeframe", font=("bold"))
        lfmTSCTHelpHeader.grid(column = 0, row = 6, sticky = EW)
        lfmTSCTHelpLabel = Label(lfmFrame, text = "This function retrieves your top songs between two specified dates. Dates are in MM/DD/YYYY format.")
        lfmTSCTHelpLabel.grid(column = 0, row = 7, sticky = EW)
        lfmTSCTHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        lfmSep3 = Separator(lfmFrame, orient=HORIZONTAL)
        lfmSep3.grid(column = 0, row = 8, sticky = EW)

        lfmGRSHelpHeader = Label(lfmFrame, text = "Get Recent Songs", font=("bold"))
        lfmGRSHelpHeader.grid(column = 0, row = 9, sticky = EW)
        lfmGRSHelpLabel = Label(lfmFrame, text = "This function retrieves songs you've listened to most recently, not including any tracks currently playing.")
        lfmGRSHelpLabel.grid(column = 0, row = 10, sticky = EW)
        lfmGRSHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)
        
    def configPlistFrame(self, plistFrame: Frame):
        plistFrame.columnconfigure(0, weight = 1)
        plistFrame.rowconfigure(0, weight = 2)
        plistFrame.rowconfigure(1, weight = 4)
        plistFrame.rowconfigure(2, weight = 1)
        plistFrame.rowconfigure(3, weight = 2)
        plistFrame.rowconfigure(4, weight = 4)
        plistFrame.rowconfigure(5, weight = 1)
        plistFrame.rowconfigure(6, weight = 2)
        plistFrame.rowconfigure(7, weight = 4)
        plistFrame.rowconfigure(8, weight = 1)
        plistFrame.rowconfigure(9, weight = 2)
        plistFrame.rowconfigure(10, weight = 4)
        plistFrame.rowconfigure(11, weight = 1)

        plistGeneralHelpHeader = Label(plistFrame, text = "General", font=("bold"))
        plistGeneralHelpHeader.grid(column = 0, row = 0, sticky = EW)
        plistGeneralHelpLabel = Label(plistFrame, text = "Once a Last.fm request is complete, songs will populate the left 'Results' box. The songs can be sorted, selected, and added to a playlist by using one of the 'Results List Options' buttons in the center.")
        plistGeneralHelpLabel.grid(column = 0, row = 1, sticky = EW)
        plistGeneralHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        plistSep1 = Separator(plistFrame, orient=HORIZONTAL)
        plistSep1.grid(column = 0, row = 2, sticky = EW)

        plistSelectionHelpHeader = Label(plistFrame, text = "On Song Selection", font=("bold"))
        plistSelectionHelpHeader.grid(column = 0, row = 3, sticky = EW)
        plistSelectionHelpLabel = Label(plistFrame, text = "Songs must be selected in the 'Results' box to be added to a playlist. This can be done in several ways. To select a song, just click on the song you want to select! However, you can also click and drag the mouse or Shift-click two songs to select all songs between the two locations, Ctrl-click (and drag if desired!) to start another selection without erasing current selections, or use Ctrl-A to select all songs. All of these selection options can also be performed in the 'Playlist' box on the right once songs have been added to it.")
        plistSelectionHelpLabel.grid(column = 0, row = 4, sticky = EW)
        plistSelectionHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)
        
        plistSep2 = Separator(plistFrame, orient=HORIZONTAL)
        plistSep2.grid(column = 0, row = 5, sticky = EW)

        plistAdditionHelpHeader = Label(plistFrame, text = "Playlist Management", font=("bold"))
        plistAdditionHelpHeader.grid(column = 0, row = 6, sticky = EW)
        plistAdditionHelpLabel = Label(plistFrame, text = "After the desired songs have been selected, just click 'Add Song(s) to Playlist' in the center column to add them to the playlist! From here, there are several options, including removing undesired songs (must be selected in playlist), moving songs around within the playlist, sorting the playlist, and exporting to Spotify. All of these can be done using the buttons in 'Playlist Options' in the center column.")
        plistAdditionHelpLabel.grid(column = 0, row = 7, sticky = EW)
        plistAdditionHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        plistSep3 = Separator(plistFrame, orient=HORIZONTAL)
        plistSep3.grid(column = 0, row = 8, sticky = EW)

        plistDuplicateHelpHeader = Label(plistFrame, text = "On Duplicates", font=("bold"))
        plistDuplicateHelpHeader.grid(column = 0, row = 9, sticky = EW)
        plistDuplicateHelpLabel = Label(plistFrame, text = "When adding new songs to a playlist, it is possible to add a song that is already in the playlist. In this case, a window will appear prompting you to select whether or not you'd like to allow duplicates. If you change your mind, click the 'Open Duplicate Option Menu' in the center column to switch your choice.")
        plistDuplicateHelpLabel.grid(column = 0, row = 10, sticky = EW)
        plistDuplicateHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

    def configExportFrame(self, exportFrame: Frame):
        exportFrame.columnconfigure(0, weight = 1)
        exportFrame.rowconfigure(0, weight = 2)
        exportFrame.rowconfigure(1, weight = 4)
        exportFrame.rowconfigure(2, weight = 1)
        exportFrame.rowconfigure(3, weight = 2)
        exportFrame.rowconfigure(4, weight = 4)
        exportFrame.rowconfigure(5, weight = 1)
        exportFrame.rowconfigure(6, weight = 2)

        exportGeneralHelpHeader = Label(exportFrame, text = "General", font=("bold"))
        exportGeneralHelpHeader.grid(column = 0, row = 0, sticky = EW)
        exportGeneralHelpLabel = Label(exportFrame, text = "When preparing to export a playlist to Spotify, you can choose whether to create a new playlist or add to an existing playlist. You must have editing access to an existing playlist in order to add songs to it. After choosing a type of playlist and adding the requisite information, just click the 'Confirm and Export' button to start playlist creation!")
        exportGeneralHelpLabel.grid(column = 0, row = 1, sticky = EW)
        exportGeneralHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        exportSep1 = Separator(exportFrame, orient=HORIZONTAL)
        exportSep1.grid(column = 0, row = 2, sticky = EW)

        exportCreationHelpHeader = Label(exportFrame, text = "Creating a New Playlist", font=("bold"))
        exportCreationHelpHeader.grid(column = 0, row = 3, sticky = EW)
        exportCreationHelpLabel = Label(exportFrame, text = "You have access to several aspects of playlist customization when creating a new playlist. These include playlist title, description (will be autofilled if left blank, any newlines in the description will be converted to spaces), cover image, and whether the playlist should be public or private. This only affects whether the playlist is visible on your public profile: sharing the link with others will still allow access. To make a playlist truly private, please use the Spotify interface, as the API cannot do this yet.")
        exportCreationHelpLabel.grid(column = 0, row = 4, sticky = EW)
        exportCreationHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

        exportSep2 = Separator(exportFrame, orient=HORIZONTAL)
        exportSep2.grid(column = 0, row = 5, sticky = EW)

        exportImageHelpHeader = Label(exportFrame, text = "On Playlist Images", font=("bold"))
        exportImageHelpHeader.grid(column = 0, row = 6, sticky = EW)
        exportImageHelpLabel = Label(exportFrame, text = "If no playlist cover image is selected, a default cover will be auto-generated by Spotify. Choosing to upload an image will replace this default cover, but there are limits. Spotify allows playlist covers to be no larger than 4MB, and accepts TIFF, PNG, and JPEG files. However, due to the restrictions of this program, PNG images will be auto-converted to JPEG when selected and compressed to 256KB. Images larger than 256KB can be selected, but they may not retain their quality. If this is an issue for you, the playlist image can always be customized more freely through the official Spotify interface.")
        exportImageHelpLabel.grid(column = 0, row = 7, sticky = EW)
        exportImageHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)

    def configMoreFrame(self, moreFrame: Frame):
        moreFrame.columnconfigure(0, weight = 1)
        moreFrame.rowconfigure(0, weight = 2)
        moreFrame.rowconfigure(1, weight = 4)
        moreFrame.rowconfigure(2, weight = 1)

        moreHelpHeader = Label(moreFrame, text = "Anything else?", font=("bold"))
        moreHelpHeader.grid(column = 0, row = 0, sticky = EW)
        moreHelpLabel = Label(moreFrame, text = "If there's anything else that doesn't make sense or that you feel needs better explanation, please don't hesitate to reach out! My email is phoebecheesecake@gmail.com. I'll try to get back to you or otherwise update things, but I have no clue on how vigilant I'll be on keeping everything up to date. I'd also love to hear any other feedback or recommendations you may have :) Thanks so much for reading all this and using this program!!!")
        moreHelpLabel.grid(column = 0, row = 1, sticky = EW)
        moreHelpLabel.configure(wraplength=self.helpWindow.winfo_width()-35)