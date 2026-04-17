import pylast
import spotipy
from spotipy.oauth2 import SpotifyPKCE
#from tkinter import *
#from tkinter.ttk import *
from ttkbootstrap import *
from ttkbootstrap.constants import *
import os

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.scope = "playlist-modify-private,playlist-modify-public,playlist-read-private,playlist-read-collaborative,ugc-image-upload"
        self.loginWindow = Toplevel(parent.root)
        self.loginWindow.geometry("450x525")
        self.loginWindow.title("Login to Last.fm and Spotify")
        self.loginWindow.wait_visibility()
        #self.loginWindow.grab_set()
        self.loginWindow.columnconfigure(0, weight=1)
        self.loginWindow.rowconfigure(0, weight=1)
        self.loginWindow.resizable(False, False)
        self.loginWindow.protocol("WM_DELETE_WINDOW", self.interceptClose)

        defaultUser = ""
        defaultClientID = ""
        defaultRedirURI = ""

        self.userToFetchVar = StringVar(value = defaultUser)
        self.clientIDVar = StringVar(value = defaultClientID)
        self.redirURIVar = StringVar(value = defaultRedirURI)

        self.spOK = False
        self.lfmOK = False

        loginFrame = Frame(self.loginWindow, padding = 10)
        loginFrame.columnconfigure(0, weight=1)
        loginFrame.rowconfigure(0, weight=1)
        loginFrame.rowconfigure(1, weight=2)
        loginFrame.rowconfigure(2, weight=1)
        loginFrame.rowconfigure(3, weight=2)
        loginFrame.rowconfigure(4, weight=1)
        loginFrame.rowconfigure(5, weight=1)
        loginFrame.grid(sticky=NSEW)

        loginLabel = Label(loginFrame, text = "Welcome to the Scrobblefy Playlist Maker! Please follow the instructions below to sign in with both Last.fm and Spotify to continue using the program.")
        loginLabel.grid(column = 0, row = 0, sticky=EW)
        loginLabel.configure(wraplength=self.loginWindow.winfo_width()-20)

        lastfmLoginFrame = Frame(loginFrame)
        lastfmLoginFrame.grid(column = 0, row = 1, sticky = NSEW, pady=5)
        lastfmLoginFrame.columnconfigure(0, weight=1)
        lastfmLoginFrame.rowconfigure(0, weight=1)
        lastfmLoginFrame.rowconfigure(1, weight=1)
        lastfmLoginFrame.rowconfigure(2, weight=1)

        self.userToFetchLabel = Label(lastfmLoginFrame, text="Enter last.fm username:")
        self.userToFetch = Entry(lastfmLoginFrame, textvariable=self.userToFetchVar)
        selectUserButton = Button(lastfmLoginFrame, text = "Select User", command=self.selectUser, bootstyle="success")
        self.userToFetchLabel.grid(sticky=NSEW, pady=5)
        self.userToFetch.grid(sticky=EW)
        selectUserButton.grid(sticky=NSEW)

        loginSeparator = Separator(loginFrame, orient=HORIZONTAL)
        loginSeparator.grid(column = 0, row = 2, sticky = EW, pady=5)

        spLoginFrame = Frame(loginFrame)
        spLoginFrame.grid(column = 0, row = 3, sticky = NSEW, pady=5)
        spLoginFrame.columnconfigure(0, weight=3)
        spLoginFrame.columnconfigure(1, weight=1)
        spLoginFrame.columnconfigure(2, weight=3)
        spLoginFrame.rowconfigure(0, weight=1)
        spLoginFrame.rowconfigure(1, weight=1)
        spLoginFrame.rowconfigure(2, weight=1)
        spLoginFrame.rowconfigure(3, weight=1)
        spLoginFrame.rowconfigure(4, weight=1)
        spLoginFrame.rowconfigure(5, weight=1)
        spLoginFrame.rowconfigure(6, weight=1)

        spLoginHeading = Label(spLoginFrame, text = "Due to recent changes made to the Spotify API, you must have your own API key to access Spotify features. This includes a client ID and redirect URI. If you don't have these and/or don't know how to create them, click the help button at the bottom of this window to learn more.")
        spLoginHeading.grid(column = 0, row = 0, sticky = EW, columnspan = 5, pady=5)
        spLoginHeading.configure(wraplength=self.loginWindow.winfo_width()-20)

        clientIDLabel = Label(spLoginFrame, text = "Client ID:")
        clientIDInput = Entry(spLoginFrame, textvariable=self.clientIDVar)
        redirURILabel = Label(spLoginFrame, text = "Redirect URI:")
        redirURIInput = Entry(spLoginFrame, textvariable=self.redirURIVar)

        clientIDLabel.grid(column = 0, row = 1, sticky = EW, pady=5)
        clientIDInput.grid(column = 0, row = 2, sticky = EW)
        redirURILabel.grid(column = 2, row = 1, sticky = EW, pady=5)
        redirURIInput.grid(column = 2, row = 2, sticky = EW)

        verifyButton = Button(spLoginFrame, name = "verify", text = "Verify and Sign In with Spotify", padding=5, bootstyle="success", command=self.setSpotipyInfo)
        verifyButton.grid(column = 0, row = 3, sticky = EW, columnspan = 5)
        self.verifyStatus = Label(spLoginFrame, text = "No user detected.")
        self.verifyStatus.grid(column = 0, row = 4, sticky = EW, columnspan = 5, pady=5)
        self.verifyStatus.configure(wraplength=self.loginWindow.winfo_width()-20)

        self.loginErrorLabel = Label(loginFrame, padding = 10, anchor = CENTER)
        self.loginErrorLabel.grid(column = 0, row = 4, sticky = NSEW, pady=5)

        buttonFrame = Frame(loginFrame)
        buttonFrame.grid(column = 0, row = 5, sticky=(S,EW))
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=5)
        buttonFrame.columnconfigure(2, weight=1)

        exitProgramButton = Button(buttonFrame, name = "cancel", text = "Exit Program", padding=5, bootstyle="danger", command=self.closeProgram)
        helpButton = Button(buttonFrame, name = "help", text = "Help", padding=5, bootstyle="info", command=self.getHelp)
        confirmLoginButton = Button(buttonFrame, name = "confirm", text = "Confirm and Sign In", padding=5, bootstyle="success", command=self.checkCreds)
        exitProgramButton.grid(column = 0, row = 0, sticky = (S,EW))
        helpButton.grid(column = 1, row = 0, sticky = (S,EW))
        confirmLoginButton.grid(column = 2, row = 0, sticky = (S,EW))

        if parent.loginBefore:
            exitProgramButton.configure(text = "Cancel", command = self.closeWindow)

    def getHelp(self):
        from helpWindow import HelpWindow
        self.helpWindow = HelpWindow(parent=self.parent)

    def selectUser(self):
        try:
            self.parent.network.get_user(self.userToFetchVar.get()).get_registered()
        except:
            self.userToFetchLabel.configure(text = "Invalid user! Try again or try another user.")
            self.lfmOK = False
        else:
            self.userToFetchLabel.configure(text = f"User {self.userToFetchVar.get()} found!")
            try:
                self.parent.user = self.parent.network.get_user(self.userToFetchVar.get())
                self.lfmOK = True
            except pylast.WSError:
                self.userToFetchLabel.configure(text = "Last.fm timed out, try again in a few seconds.")
                self.lfmOK = False

    def setSpotipyInfo(self):
        if(".cache" in os.listdir(".")):
            os.remove(".cache")
        try:
            self.parent.sp = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=self.clientIDVar.get(), redirect_uri=self.redirURIVar.get(), scope=self.scope), retries=0, requests_timeout = 10)
            self.verifyStatus.configure(text = "Signed in as " + self.parent.sp.current_user()["display_name"] + "!")
            self.spOK = True
            self.parent.root.attributes(topmost=True)
            self.parent.root.attributes(topmost=False)
            self.loginWindow.attributes(topmost=True)
            self.loginWindow.attributes(topmost=False)
        except spotipy.exceptions.SpotifyOauthError as e:
            self.verifyStatus.configure(text = "User not found. Please double check the validity of your inputs and try again. If this issue persists, check the help window.")
            self.spOK = False

    def interceptClose(self):
        interceptWindow = Toplevel(self.loginWindow)
        interceptWindow.geometry("400x100")
        interceptWindow.attributes(topmost=True)
        interceptWindow.title("Just a second!")
        interceptWindow.wait_visibility()
        interceptWindow.grab_set()
        interceptWindow.columnconfigure(0, weight=1)
        interceptWindow.rowconfigure(0, weight=1)
        interceptWindow.resizable(False, False)

        interceptLabel = Label(interceptWindow, text="Please enter your last.fm username and Spotify API credentials and click Confirm, or use Cancel to close the program. You may close this window to continue.")
        interceptLabel.grid()
        interceptLabel.configure(wraplength=interceptWindow.winfo_width()-10)

    def closeWindow(self):
        self.parent.root.attributes(topmost=True)
        self.loginWindow.destroy()

    def closeProgram(self):
        self.parent.root.destroy()

    def checkCreds(self):
        if self.lfmOK and self.spOK:
            self.closeWindow()
        elif self.lfmOK:
            self.loginErrorLabel.configure(text="Error with Spotify login! Please fix and try again.")
        elif self.spOK:
            self.loginErrorLabel.configure(text="Error with Last.fm login! Please fix and try again.")
        else:
            self.loginErrorLabel.configure(text="Error with Spotify and Last.fm login! Please fix and try again.")


    