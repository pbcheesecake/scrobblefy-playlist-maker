import pylast
#from tkinter import *
#from tkinter.ttk import *
from ttkbootstrap import *
import spotipy
from mainWindow import MainWindow
import tkinter.font as tkFont
import pyglet
pyglet.options['win32_gdi_font'] = True
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(2)

if __name__ == "__main__":
    #initial auth stuff
    API_KEY = "c6507e7ad3ebfeb1b403d2f3fb64754a"
    API_SECRET = "b1e0f12472c2cb4fcec03a25bebed58d"

    username = "cstet23"
    password_hash = "8498a330ac4402a1e89eb9c83703879b"

    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=username,
        password_hash=password_hash,
    )

    sp: spotipy.Spotify | None = None
    user: pylast.User | None = None

    
    root = Window(themename="scrobblefy")

    pyglet.font.add_file("Lexend-Medium.ttf")
    pyglet.font.add_file("Lexend-Light.ttf")
    default_font = tkFont.nametofont("TkDefaultFont")
    text_font = tkFont.nametofont("TkTextFont")
    default_font.config(family="Lexend Medium", size=11)
    text_font.config(family="Lexend Light", size=11)
    #TODO: STYLE EVERYTHING WITH TTKBOOTSTRAP WHAT THE FUCK

    mainWindow = MainWindow(root=root, sp=sp, network=network, user=user)
    mainWindow.start()