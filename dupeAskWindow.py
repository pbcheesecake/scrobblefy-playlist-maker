from tkinter import *
from tkinter.ttk import *

class DupeAskWindow:
    def __init__(self, allowDupes: BooleanVar, parent):
        self.root = parent.root
        style = Style()
        style.configure(style="G.TButton", foreground="green")
        style.configure(style="R.TButton", foreground="red")

        self.allowDupes = allowDupes
        self.dupeAsk = Toplevel(self.root)
        self.dupeAsk.geometry("400x100")
        self.dupeAsk.attributes(topmost=True)
        self.dupeAsk.title("Allow duplicates?")
        self.dupeAsk.wait_visibility()
        self.dupeAsk.grab_set()

        dupeFrame = Frame(self.dupeAsk, padding = 10)
        dupeFrame.columnconfigure(0, weight=1)
        dupeFrame.columnconfigure(1, weight=1)
        dupeFrame.rowconfigure(0, weight=1)
        dupeFrame.rowconfigure(1, weight=1)
        dupeFrame.grid(sticky=NSEW)

        dupeLabel = Label(dupeFrame, text = "You have selected duplicates of one or more song. Allow duplicates? (This will be remembered for this playlist.)", wraplength=380, anchor=CENTER)
        dupeLabel.grid(column = 0, row = 0, sticky = NSEW, columnspan=2)

        dupeAllowButton = Button(dupeFrame, name = "allow", text = "Allow", padding=10, style="G.TButton")
        dupeDisallowButton = Button(dupeFrame, name = "disallow", text = "Disallow", padding=10, style="R.TButton")
        dupeAllowButton.bind('<Button-1>', self.checkButForDupes)
        dupeDisallowButton.bind('<Button-1>', self.checkButForDupes)
        dupeAllowButton.grid(column = 0, row = 1, sticky = EW)
        dupeDisallowButton.grid(column = 1, row = 1, sticky = EW)

    def checkButForDupes(self, event: Event):
        if event.widget.winfo_name() == "allow":
            self.allowDupes.set(True)
        else: self.allowDupes.set(False)
        self.dupeAsk.destroy()