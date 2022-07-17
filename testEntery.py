from tkinter import Button, Entry, StringVar, Tk



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
    def __init__(self, root, row, column, padx, pady, defaultText, limit):
        self.root = root
        self.row = row
        self.column = column
        self.x = padx
        self.y = pady
        self.contains = int(defaultText)
        self.limit = limit

        self.entry = Entry(self.root)

        self.leftChange10 = Button1(
            root,
            row-1, column,
            16, 4,
            text="<<<",
            leftClick=lambda event: self.changeAmount(-10)
        )

        self.leftChange5 = Button1(
            root, 
            row-1, column + 1,
            16, 4,
            text="<<",
            leftClick=lambda event: self.changeAmount(-5)
        )

        self.leftChange1 = Button1(
            root,
            row-1, column + 2,
            16, 4,
            text="<",
            leftClick=lambda event: self.changeAmount(-1)
        )

        self.rightChange1 = Button1(
            root,
            row-1, column + 4,
            16, 4,
            text=">",
            leftClick=lambda event: self.changeAmount(1)
        )

        self.rightChange5 = Button1(
            root,
            row-1, column + 5,
            16, 4,
            text=">>",
            leftClick=lambda event: self.changeAmount(5)
        )

        self.rightChange10 = Button1(
            root,
            row-1, column + 6,
            16, 4,
            text=">>>",
            leftClick=lambda event: self.changeAmount(10)
        )

        self.entry.insert(-1, self.contains)
        self.entry.grid(row=self.row, column=self.column+3)
    
    def update(self):
        self.entry.grid_remove()
        self.entry = Entry(self.root)
        self.entry.insert(str(self.contains))
        self.entry.grid(row=self.row, column=self.column)
    
    def changeAmount(self, amount):
        test = self.contains + amount
        if test > self.limit:
            self.contains = self.limit
        elif test < 0:
            self.contains = 0
        else:
            self.contains = test
        print("changed by:"+str(amount))
        self.entry.delete(0, 100)
        self.entry.insert(-1, str(self.contains))
    
    def thingy(self):
        print("comand was called")


asjkdfhk = 0

class mywindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.kasdfkjhj = Inputer(self, 0, 0, 16, 4, "20", 100)
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