from tkinter import Button, Entry, StringVar, Tk

asjkdfhk = 0

class mywindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.myEnteryText = StringVar(self, value="20")
        self.myEntery = Entry(self, textvariable=self.myEnteryText)
        self.myEntery.grid(row=0, column=0)
        self.mybutton = Button(self, padx=10, pady=10)
        self.mybutton.bind("<Button-1>", self.thingy)
        self.mybutton.grid(row=0, column=1)
        self.updater()
        self.mainloop()
    
    def thingy(self, event=None):
        self.myEntery.delete(0, 100)
        self.myEntery.insert(-1, str(asjkdfhk))
    
    def updater(self, event=None):
        change()
        self.after(1000, self.updater)


def change(event=None):
    global asjkdfhk
    asjkdfhk += 1

hasjkdf = mywindow()

class Button1():
    def __init__(self, root, row, column, len, wid, text=" ", color="white", fg="black", leftClick=None, Enter=None, Leave=None):
        self.root = root
        self.row = row
        self.column = column
        self.len = len
        self.width = wid
        self.txt = text
        self.color = color
        self.foreGround = fg

        self.button = Button(
            self.root,
            text=self.txt,
            padx=self.len,
            pady=self.width,
            bg=self.color,
            fg=self.foreGround
        )

        self.button.grid(row=self.row+1, column=self.column)
        self.button.bind("<Button-1>", leftClick)
        self.button.bind("<Enter>", Enter)
        self.button.bind("<Leave>", Leave)
    

    def update(self):
        self.button.grid_remove()
        self.button = Button(
            self.root,
            text=self.txt,
            padx=self.len,
            pady=self.width,
            bg=self.color,
            fg=self.foreGround
        )
        self.button.grid(row=self.row+1, column=self.column)

class Inputer():
    def __init__(self, root, row, column, padx, pady, defaultText):
        self.root = root
        self.row = row
        self.column = column
        self.x = padx
        self.y = pady
        self.contains = defaultText

        self.entry = Entry(self.root)
        self.entry.insert(self.contains)
        self.entry.grid(row=self.row, column=self.column)
    
    def update(self):
        self.entry.grid_remove()
        self.entry = Entry(self.root)
        self.entry.insert(self.contains)
        self.entry.grid(row=self.row, column=self.column)
    
    def changeAmount(self, event=None):
        pass
