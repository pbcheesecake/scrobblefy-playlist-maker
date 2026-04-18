from pylast import TopItem, User
from ttkbootstrap import *
from ttkbootstrap.constants import *
import re
import time
import datetime
from calendar import timegm
from pylast import WSError

class FuncMenu:
    def __init__(self, parent: Frame, root: Tk, user: User, menu: str, timeframeVar: StringVar, songCountVar: int | None, allSongList: list[TopItem], allSongListVar: StringVar, weightedList: list[TopItem]):
        self.parent = parent
        self.root = root
        self.user = user
        self.menu = menu
        self.timeframeVar = timeframeVar
        self.songCountVar = songCountVar
        self.allSongList = allSongList
        self.allSongListVar = allSongListVar
        self.weightedList = weightedList
        formattedStartTime = time.strftime('%m/%d/%Y', time.gmtime(int(self.user.get_registered())))
        formattedEndTime = time.strftime('%m/%d/%Y', time.gmtime(time.time()))
        timeStartList = formattedStartTime.split("/")
        timeEndList = formattedEndTime.split("/")
        self.startDate = datetime.datetime.fromtimestamp(int(self.user.get_registered()))
        self.endDate = datetime.datetime.now()
        self.startDateMonthVar = IntVar(value=int(timeStartList[0]))
        self.startDateDayVar = IntVar(value=int(timeStartList[1]))
        self.startDateYearVar = IntVar(value=int(timeStartList[2]))
        self.endDateMonthVar = IntVar(value=int(timeEndList[0]))
        self.endDateDayVar = IntVar(value=int(timeEndList[1]))
        self.endDateYearVar = IntVar(value=int(timeEndList[2]))
        self.dateErrorLabel = None

    def check_num(self, newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 3
    
    def check_date(self, newval):
        return datetime.datetime.fromtimestamp(int(self.user.get_registered())) < newval < datetime.datetime.now()
    
    def removeLeadingZeros(self, num):
        strnum = str(num)
        for i in range(len(strnum)):
            if strnum[i] != '0':
                res = strnum[i::]
                return int(res)
        return 0
    
    def clearSongs(self):
        self.allSongListVar.set([])

    def parseTime(self, date: datetime):
        return int(datetime.datetime.timestamp(date))
    
    def getTops(self, event):
        #default options: overall, 7day, 1month, 3month, 6month, 12month
        songList = []
        self.allSongList.clear()
        self.weightedList.clear()
        if self.songCountVar.get() == 0:
            tops = self.user.get_top_tracks(period = self.timeframeVar.get())
        else:
            self.songCountVar.set(self.removeLeadingZeros(self.songCountVar.get()))
            tops = self.user.get_top_tracks(period = self.timeframeVar.get(), limit = self.songCountVar.get())
        self.clearSongs()
        for song in tops:
            songList.append(str(song[0])+": "+str(song[1])+" listens")
            self.allSongList.append(song)
            self.weightedList.append(song)
        self.allSongListVar.set(songList)

    def getTopsFromDates(self, event):
        self.dateErrorLabel.grid_remove()
        songList = []
        self.allSongList.clear()
        self.weightedList.clear()
        try:
            startTime = self.parseTime(self.startDateSelector.get_date())
            endTime = self.parseTime(self.endDateSelector.get_date())
            if(self.check_date(self.startDateSelector.get_date()) and self.check_date(self.endDateSelector.get_date())):
                if self.songCountVar.get() == 0:
                    tops = self.user.get_weekly_track_charts(startTime, endTime)
                else:
                    self.songCountVar.set(self.removeLeadingZeros(self.songCountVar.get()))
                    tops = self.user.get_weekly_track_charts(startTime, endTime)
                    while len(tops)>self.songCountVar.get():
                        tops.pop()
                self.clearSongs()
                for song in tops:
                    songList.append(str(song[0])+": "+str(song[1])+" listens")
                    self.allSongList.append(song)
                    self.weightedList.append(song)
                self.allSongListVar.set(songList)
                self.dateErrorLabel.grid_forget()
            else:
                raise ValueError
        except ValueError:
            Label.configure(self.dateErrorLabel, text="Dates out of range! Enter valid dates.")
            self.dateErrorLabel.grid(column = 0, row = 2, columnspan = 7)
        except WSError:
            Label.configure(self.dateErrorLabel, text="Last.fm error, try again in a couple seconds.")
            self.dateErrorLabel.grid(column = 0, row = 2, columnspan = 7)

    def getRecents(self, event):
        songList = []
        self.allSongList.clear()
        self.weightedList.clear()
        if self.songCountVar.get() == 0:
            recents = self.user.get_recent_tracks()
        else:
            recents=self.user.get_recent_tracks(self.songCountVar.get())
        self.clearSongs()
        for song in recents:
            songList.append(str(song[0]))
            topItemSong = TopItem(song.track, 1)
            self.allSongList.append(topItemSong)
            self.weightedList.append(topItemSong)
        self.allSongListVar.set(songList)
        
    def setup(self):
        check_num_wrapper = (self.root.register(self.check_num), '%P')
        
        songCountLabel = Label(self.parent, text="# of songs (use 0 for all):")
        retrieveButton = Button(self.parent, text = "Retrieve", padding = 10)
        widgetSeparator = Separator(self.parent, orient=HORIZONTAL)

        if self.menu == "topDefaultTimeframe":
            timeframeLabel = Label(self.parent, text="Choose timeframe:")
            timeframeLabel.grid(row = 0, columnspan = 7)

            tDToneweek = Radiobutton(self.parent, text = "7 Days", variable = self.timeframeVar, value = "7day")
            tDTonemonth = Radiobutton(self.parent, text = "1 Month", variable = self.timeframeVar, value = "1month")
            tDTthreemonth = Radiobutton(self.parent, text = "3 Months", variable = self.timeframeVar, value = "3month")
            tDTsixmonth = Radiobutton(self.parent, text = "6 Months", variable = self.timeframeVar, value = "6month")
            tDToneyear = Radiobutton(self.parent, text = "1 Year", variable = self.timeframeVar, value = "12month")
            tDToverall = Radiobutton(self.parent, text = "All Time", variable = self.timeframeVar, value = "overall")
            
            tDToneweek.grid(column = 0, row = 1, columnspan = 1)
            tDTonemonth.grid(column = 1, row = 1, columnspan = 1)
            tDTthreemonth.grid(column = 2, row = 1, columnspan = 1)
            tDTsixmonth.grid(column = 3, row = 1, columnspan = 1)
            tDToneyear.grid(column = 4, row = 1, columnspan = 1)
            tDToverall.grid(column = 5, row = 1, columnspan = 1)

            retrieveButton.bind('<Button-1>', self.getTops)

        elif self.menu == "topCustomTimeframe":
            startDateLabel = Label(self.parent, text="Start Date (MM/DD/YYYY):")
            startDateLabel.grid(column = 0, row = 0, columnspan = 3)

            endDateLabel = Label(self.parent, text="End Date (MM/DD/YYYY):")
            endDateLabel.grid(column = 4, row = 0, columnspan = 3)

            self.startDateSelector = DateEntry(master=self.parent, dateformat="%m/%d/%y", startdate=self.startDate)
            dateSeparator = Separator(self.parent, orient=VERTICAL)
            self.endDateSelector = DateEntry(master=self.parent, dateformat="%m/%d/%y", startdate=self.endDate)

            self.startDateSelector.grid(sticky = NSEW, column = 0, row = 1, columnspan = 3)
            dateSeparator.grid(sticky = NS, column = 3, row = 0, rowspan = 2)
            self.endDateSelector.grid(sticky = NSEW, column = 4, row = 1, columnspan = 3)

            self.dateErrorLabel = Label(self.parent, text="", bootstyle="danger")

            retrieveButton.bind('<Button-1>', self.getTopsFromDates)

        elif self.menu == "recentSongs":
            retrieveButton.bind('<Button-1>', self.getRecents)
            songCountLabel.configure(text = "# of songs (using 0 gives 10):")

        
        widgetSeparator.grid(sticky = EW, columnspan = 7, pady = 5)
        songCountLabel.grid(sticky = EW, columnspan = 7)
        songCountSpinbox = Spinbox(self.parent, from_=0, to=999, textvariable=self.songCountVar, validate='key', validatecommand=check_num_wrapper)
        songCountSpinbox.grid(sticky = EW, columnspan = 7)
        retrieveButton.grid(columnspan = 7)
