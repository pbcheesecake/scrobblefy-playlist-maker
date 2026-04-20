import spotipy
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from ttkbootstrap import *
from ttkbootstrap.constants import *
import re
from datetime import datetime, timezone
import io
from contextlib import redirect_stderr
from PIL import Image, ImageTk
import base64

class ExportWindow:
    def __init__(self, songList: str, parent):
        self.root: Tk = parent.root
        self.sp: spotipy.Spotify = parent.sp

        self.songList = re.split("',|\",", songList)
        self.playlistNameVar = StringVar()
        self.playlistVisVar = BooleanVar(value=False)
        self.playlistNewVar = BooleanVar(value=True)
        self.playlistURLVar = StringVar()
        self.imgPath: str
        self.encodedImgString: str
        self.pic: ImageTk.PhotoImage

        self.exportWindow = Toplevel(self.root)
        self.exportWindow.geometry(f'{int(parent.root.winfo_screenwidth()*.25)}x{int(parent.root.winfo_screenheight()*.6)}')
        self.exportWindow.title("Export to Spotify")
        self.exportWindow.wait_visibility()
        self.exportWindow.grab_set()
        self.exportWindow.columnconfigure(0, weight=1)
        self.exportWindow.rowconfigure(0, weight=1)
        self.exportWindow.resizable(False, False)

        exportFrame = Frame(self.exportWindow, padding = 10)
        exportFrame.columnconfigure(0, weight=1)
        exportFrame.rowconfigure(0, weight=1)
        exportFrame.rowconfigure(1, weight=10)
        exportFrame.rowconfigure(2, weight=1)
        exportFrame.rowconfigure(3, weight=1)
        exportFrame.grid(sticky=NSEW)

        playlistFrame = Frame(exportFrame)
        playlistFrame.grid(column = 0, row = 0, sticky=NSEW)
        playlistFrame.columnconfigure(0, weight=1)
        playlistFrame.columnconfigure(1, weight=1)
        playlistFrame.columnconfigure(2, weight=3)
        playlistFrame.columnconfigure(3, weight=3)
        playlistFrame.rowconfigure(0, weight=1)
        playlistFrame.rowconfigure(1, weight=1)
        playlistFrame.rowconfigure(2, weight=1)
        playlistFrame.rowconfigure(3, weight=1)
        playlistFrame.rowconfigure(4, weight=1)
        playlistFrame.rowconfigure(5, weight=1)
        playlistFrame.rowconfigure(6, weight=1)
        playlistFrame.rowconfigure(7, weight=1)
        playlistFrame.rowconfigure(8, weight=1)
        playlistFrame.rowconfigure(9, weight=1)
        playlistFrame.rowconfigure(10, weight=1)

        playlistNewStatusLabel = Label(playlistFrame, text = "Create new playlist or add to existing?")
        playlistNewTrue = Radiobutton(playlistFrame, text = "New", variable = self.playlistNewVar, value = True, command=self.renderNew)
        playlistNewFalse = Radiobutton(playlistFrame, text = "Existing", variable = self.playlistNewVar, value = False, command=self.renderPrev)
        playlistNewStatusLabel.grid(column = 0, row = 0, sticky = EW, columnspan = 4, pady=5)
        playlistNewTrue.grid(column = 0, row = 1, sticky = W, pady=5)
        playlistNewFalse.grid(column = 1, row = 1, sticky = W, pady=5)

        self.playlistNewNameLabel = Label(playlistFrame, text = "New playlist name:")
        self.playlistNewNameInput = Entry(playlistFrame, textvariable=self.playlistNameVar)
        self.playlistDescLabel = Label(playlistFrame, text = "Playlist description (optional):")
        self.playlistDescText = Text(playlistFrame, width = 30, height = 5, wrap = WORD)
        self.playlistDescScrollbar = Scrollbar(playlistFrame, orient=VERTICAL, command=self.playlistDescText.yview)
        self.playlistDescText.configure(yscrollcommand=self.playlistDescScrollbar.set)
        self.playlistNewNameLabel.grid(column = 0, row = 2, sticky = EW, columnspan = 4, pady=5)
        self.playlistNewNameInput.grid(column = 0, row = 3, sticky = EW, columnspan = 4, pady=5)
        self.playlistDescLabel.grid(column = 0, row = 4, sticky = EW, columnspan = 4, pady=5)
        self.playlistDescText.grid(column = 0, row = 5, sticky = EW, columnspan = 4, pady=5)
        self.playlistDescScrollbar.grid(column = 3, row = 5, sticky = (E, NS), pady=5)

        self.playlistURLLabel = Label(playlistFrame, text = "Enter URL of existing playlist:")
        self.playlistURLInput = Entry(playlistFrame, textvariable=self.playlistURLVar)

        self.playlistVisLabel = Label(playlistFrame, text = "Make playlist public or private? (Note: this only affects visibility on profile)")
        self.playlistVisPublic = Radiobutton(playlistFrame, text = "Public", variable = self.playlistVisVar, value = True)
        self.playlistVisPrivate = Radiobutton(playlistFrame, text = "Private", variable = self.playlistVisVar, value = False)
        self.playlistVisLabel.grid(column = 0, row = 6, sticky = EW, columnspan = 4, pady=5)
        self.playlistVisPublic.grid(column = 0, row = 7, sticky = W, pady=5)
        self.playlistVisPrivate.grid(column = 1, row = 7, sticky = W, pady=5)

        self.playlistImgHeader = Label(playlistFrame, text = "Add image for playlist (optional)")
        self.playlistImgFrame = Frame(playlistFrame, width = 170, height = 170, relief = "solid", padding = 8)
        self.playlistImgFrame.grid_propagate(False)
        self.playlistImgLabel = Label(self.playlistImgFrame, text = "No image selected.")
        self.playlistImgAddButton = Button(playlistFrame, name = "addimage", text = "Add Image", padding=5, command=self.findImage)
        
        self.playlistImgHeader.grid(column = 0, row = 8, sticky = EW, columnspan = 4, pady=5)
        self.playlistImgFrame.grid(column = 0, row = 9, sticky = W, columnspan = 4)
        self.playlistImgLabel.grid(column = 0, row = 0, sticky = NSEW, columnspan = 4)
        self.playlistImgAddButton.grid(column = 0, row = 10, sticky = W, columnspan = 4, pady=5)

        exportProgressFrame = Frame(exportFrame)
        exportProgressFrame.grid(column = 0, row = 2, sticky=NSEW)
        exportProgressFrame.columnconfigure(0, weight = 1)
        exportProgressFrame.rowconfigure(0, weight = 1)
        exportProgressFrame.rowconfigure(1, weight = 1)

        self.exportProgressLabel = Label(exportProgressFrame, text = "Creating playlist...")
        self.exportProgressbar = Progressbar(exportProgressFrame, orient=HORIZONTAL, length=300, mode='determinate', maximum = len(self.songList), bootstyle="success")

        buttonFrame = Frame(exportFrame)
        buttonFrame.grid(column = 0, row = 3, sticky=NSEW)
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)
        buttonFrame.columnconfigure(2, weight=1)

        cancelExportButton = Button(buttonFrame, name = "cancel", text = "Cancel", padding=5, bootstyle="danger", command=self.closeWindow)
        confirmExportButton = Button(buttonFrame, name = "confirm", text = "Confirm and Export", padding=5, bootstyle="success", command=self.exportPlaylist)
        cancelExportButton.grid(column = 0, row = 0, sticky = (S,EW))
        confirmExportButton.grid(column = 2, row = 0, sticky = (S,EW))

    def closeWindow(self):
        self.root.update()
        self.exportWindow.destroy()

    def exportPlaylist(self):
        #print(self.songList)
        self.iterator = 0
        self.itemsToAdd = []
        try: self.encodeImage()
        except:
            self.exportProgressLabel.configure(text = "Image format not accepted. Please pick a different one and try again.")
            self.exportWindow.update()
            return
        self.exportProgressLabel.grid(column = 0, row = 0, pady = 5, sticky = EW)
        if self.playlistNameVar.get() == "":
            self.exportProgressLabel.configure(text = "Please add a name for your playlist before continuing!")
            self.exportWindow.update()
            return
        self.exportProgressbar.grid(column = 0, row = 1, pady = 5, sticky = EW)
        self.addSong()
        

    def renderNew(self):
        self.playlistURLLabel.grid_remove()
        self.playlistURLInput.grid_remove()

        """self.playlistNewNameLabel.grid(column = 0, row = 2, sticky = EW, columnspan = 4, pady=5)
        self.playlistNewNameInput.grid(column = 0, row = 3, sticky = EW, columnspan = 4, pady=5)
        self.playlistDescLabel.grid(column = 0, row = 4, sticky = EW, pady=5)
        self.playlistDescText.grid(column = 0, row = 5, sticky = EW, columnspan = 4, pady=5)
        self.playlistDescScrollbar.grid(column = 3, row = 5, sticky = (E, NS), pady=5)
        self.playlistVisLabel.grid(column = 0, row = 6, sticky = EW, columnspan = 4)
        self.playlistVisPublic.grid(column = 0, row = 7, sticky = W)
        self.playlistVisPrivate.grid(column = 1, row = 7, sticky = W)
        self.playlistImgHeader.grid(column = 0, row = 8, sticky = EW, columnspan=4, pady=5)
        self.playlistImgFrame.grid(column = 0, row = 9, sticky = W)
        self.playlistImgLabel.grid(column = 0, row = 0, sticky = NSEW)
        self.playlistImgAddButton.grid(column = 0, row = 10, sticky = W, pady=5)"""

        self.playlistNewNameLabel.grid()
        self.playlistNewNameInput.grid()
        self.playlistDescLabel.grid()
        self.playlistDescText.grid()
        self.playlistDescScrollbar.grid()
        self.playlistVisLabel.grid()
        self.playlistVisPublic.grid()
        self.playlistVisPrivate.grid()
        self.playlistImgHeader.grid()
        self.playlistImgFrame.grid()
        self.playlistImgLabel.grid()
        self.playlistImgAddButton.grid()

    def renderPrev(self):
        self.playlistNewNameLabel.grid_remove()
        self.playlistNewNameInput.grid_remove()
        self.playlistDescLabel.grid_remove()
        self.playlistDescText.grid_remove()
        self.playlistDescScrollbar.grid_remove()
        self.playlistVisLabel.grid_remove()
        self.playlistVisPublic.grid_remove()
        self.playlistVisPrivate.grid_remove()
        self.playlistImgHeader.grid_remove()
        self.playlistImgFrame.grid_remove()
        self.playlistImgLabel.grid_remove()
        self.playlistImgAddButton.grid_remove()

        self.playlistURLLabel.grid(column = 0, row = 2, sticky = EW, columnspan = 4)
        self.playlistURLInput.grid(column = 0, row = 3, sticky = EW, columnspan = 4)

    def addSong(self):
        song = self.songList[self.iterator]
        formattedSong = song[2:]
        if self.iterator == len(self.songList) - 1:
            formattedSong = formattedSong[:-2]
        if len(formattedSong)>2:
            songArtist, songTitle = formattedSong.split(" - ", maxsplit = 1)
            self.exportProgressLabel.configure(text = f"Finding {songTitle} by {songArtist}...")
            errOutput = io.StringIO()
            with redirect_stderr(errOutput):
                try: searchRes = dict(self.sp.search(q = f"track:\"{songTitle}\" artist:\"{songArtist}\"", type="track", limit = 1))
                except spotipy.exceptions.SpotifyException as e:
                    if e.http_status == 429:
                        waitTime = int(errOutput.getvalue().replace("Your application has reached a rate/request limit. Retry will occur after: ", "").split()[0])
                        waitHr = waitTime // 3600
                        waitMin = waitTime % 3600 // 60
                        waitSec = waitTime % 60
                        self.exportProgressLabel.configure(text = f"Spotify rate limit reached. Please try again in {waitHr} hours, {waitMin} minutes and {waitSec} seconds.")
                        self.exportProgressbar.grid_remove()
                        self.playlistImgLabel.config(image=self.pic)
                        self.exportWindow.update()
                        return
            trackDict = dict(searchRes.get("tracks"))
            itemsDict = dict(trackDict.get("items")[0])
            itemID = itemsDict.get("uri")
            self.itemsToAdd.append(itemID)
            self.exportProgressbar.step()
            self.exportWindow.update()
        self.iterator += 1
        if self.iterator < len(self.songList):
            self.exportWindow.after(ms = 750, func = self.addSong)
        else:
            self.exportProgressLabel.configure(text = "Creating playlist...")
            self.playlistImgLabel.config(image=self.pic)
            self.exportWindow.update()
            if self.playlistNewVar.get():
                newDesc = str(self.playlistDescText.get("1.0", "end")).replace("\n", "")
                if newDesc == "":
                    tZone = datetime.now(timezone.utc).astimezone().tzinfo
                    self.sp.current_user_playlist_create(name=self.playlistNameVar.get(), public=self.playlistVisVar.get(), description=f"Playlist generated by Top Song Grabber on {datetime.now(tz = tZone)}.")
                else:
                    self.sp.current_user_playlist_create(name=self.playlistNameVar.get(), public=self.playlistVisVar.get(), description=newDesc)
                self.playlist_url = self.sp.current_user_playlists(limit=1)["items"][0]["external_urls"]["spotify"]
            else:
                self.playlist_url = self.playlistURLVar.get().split("?", maxsplit=1)[0]
            try: 
                self.sp.playlist_upload_cover_image(playlist_id=self.playlist_url, image_b64=self.encodedImgString)
            except:
                self.exportProgressLabel.configure(text = "Error updating playlist image! Skipping...")
                self.exportProgressbar.grid_remove()
                self.exportWindow.update()
                self.exportWindow.after(1500)
            self.exportProgressLabel.configure(text = "Almost done! Adding songs to playlist...")
            self.exportWindow.update()
            self.exportWindow.after(ms = 2000, func = self.addItems)
            self.closeTime = 3
            self.exportProgressLabel.configure(text = "Playlist creation complete! Closing window in "+str(self.closeTime)+" seconds.")
            self.exportProgressbar.grid_remove()
            self.exportWindow.after(ms = 1000, func = self.updateCloseTime)

    def addItems(self):
        errOutput = io.StringIO()
        with redirect_stderr(errOutput):
            try: 
                for i in range(0, len(self.itemsToAdd), 100):
                    self.sp.playlist_add_items(playlist_id=self.playlist_url, items=self.itemsToAdd[i:i+100])
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    waitTime = errOutput.getvalue().replace("Your application has reached a rate/request limit. Retry will occur after: ", "").split()[0]
                    waitHr = waitTime // 3600
                    waitMin = waitTime % 3600 // 60
                    waitSec = waitTime % 60
                    self.exportProgressLabel.configure(text = f"Spotify rate limit reached. Please try again in {waitHr} hours, {waitMin} minutes and {waitSec} seconds.")
                    self.exportProgressbar.grid_remove()
                    self.exportWindow.update()
                    return
            
    def updateCloseTime(self):
        if self.closeTime == 1:
            self.closeWindow()
        else:
            self.closeTime -= 1
            self.exportProgressLabel.configure(text = f"Playlist creation complete! Closing window in {self.closeTime} seconds.")
            self.exportWindow.after(ms = 1000, func = self.updateCloseTime)

    def findImage(self):
        fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        self.imgPath = filedialog.askopenfilename(filetypes=fileTypes)
        if len(self.imgPath):
            img = Image.open(self.imgPath)
            img = img.resize((150, 150))
            self.pic = ImageTk.PhotoImage(img)
            self.playlistImgLabel.config(image=self.pic)

    def compressImage(self, img: Image.ImageFile):
        quality = 95
        while quality > 10:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", optimize=True, quality=quality)
            if buffer.tell() / 1024 <= 200:
                return buffer
            quality -= 5
        return buffer
    
    def encodeImage(self):
        if len(self.imgPath):
            img = Image.open(self.imgPath)
            if self.imgPath.lower().endswith(".png"):
                rgb_img = img.convert('RGB')
                buffer = io.BytesIO()
                rgb_img.save(buffer, format="JPEG", quality=95)
                img = Image.open(buffer)
            imgBuffer = self.compressImage(img = img)
            imgBytes = imgBuffer.getvalue()
            self.encodedImgString = base64.b64encode(imgBytes).decode('utf-8')