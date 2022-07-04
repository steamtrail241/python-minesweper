from tkinter import *
import random
import time
from turtle import update
import buttons
import timer
from tkinter import messagebox


class Main_S(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.but_D = buttons.Button1(
            self,
            0,
            0,
            50,
            10,
            text="doubles game",
            LC = self.LCbut_D,
            Enter=self.Ebut_D,
            Leave=self.Lbut_D
        )
        self.mainloop()
    
    def LCbut_D(self, event = None):
        print("left clicked")
        RegularMinesweeper()

    def Ebut_D(self, event = None):
        print("hover oever")

    def Lbut_D(self, event = None):
        print("leave button")

class RegularMinesweeper(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.Window_Close)

        allbombs = []

        for i in range(40):

            # creates and checks if position is already a bomb
            check1 = False
            while check1 is False:

                # creates random position
                smth1 = random.randint(0, 20-1)
                smth2 = random.randint(0, 20-1)
                
                #test position
                if [smth1, smth2] not in allbombs:
                    allbombs.append([smth1, smth2])
                    check1 = True
                    print([smth1, smth2])

        allTiles = []

        for i in range(20):
            mini = []
            for i1 in range(20):
                if [i, i1] in allbombs:
                    newButton = buttons.Tile(self, i, i1, 16, 10, 10, 10, bomb=True)
                    newButton.bomblist = allbombs
                    mini.append(newButton)
                else:
                    newButton = buttons.Tile(self, i, i1, 16, 10, 10, 10)
                    newButton.bomblist = allbombs
                    mini.append(newButton)
            allTiles.append(mini)
            mini[0].listOfTiles.append(mini)

        allTiles[0][0].bomblist = allbombs
        allTiles[0][0].mr = 10
        allTiles[0][0].mc = 10
        
        self.T = self.timer()

        self.Navbar = Text(self, padx=228, pady=5, width=25, height=1)
        self.Navbar.insert(INSERT, "00:00:00   |   10 flags")
        self.Navbar.grid(row = 0, column = 0, columnspan = 15)

        self.comunicate = buttons.Tile(self, -1, 15, 16, 1, None, None, None)

        self.Upd()
        self.Upd2()

        self.mainloop()
    
    def Upd(self, event = None):
        self.title(self.T.returntime())
        self.Navbar.grid_remove()
        number_of_flags = 40
        for i in self.comunicate.listOfTiles:
            for i1 in i:
                if i1.flaged:
                    number_of_flags -= 1
        self.Navbar = Text(self, padx=228, pady=5, width=25, height=1)
        self.Navbar.insert(INSERT, self.T.returntime()+"   |   "+str(number_of_flags)+" flags")
        self.Navbar.grid(row = 0, column = 0, columnspan = 15)
        self.T.changetime()
        self.after(1000, self.Upd)
    
    def Upd2(self, event = None):
        self.Navbar.grid_remove()
        number_of_flags = 40
        for i in self.comunicate.listOfTiles:
            for i1 in i:
                if i1.flaged:
                    number_of_flags -= 1
        self.Navbar = Text(self, padx=228, pady=5, width=25, height=1)
        self.Navbar.insert(INSERT, self.T.returntime()+"   |   "+str(number_of_flags)+" flags")
        self.Navbar.grid(row = 0, column = 0, columnspan = 15)
        self.after(100, self.Upd2)
    
    class timer():
        def __init__(self1):
            self1.timeron = True
            self1.seconds = 0
            self1.minutes = 0
            self1.hours = 0

        def changetime(self1):
            if self1.timeron is True:
                self1.seconds = self1.seconds + 1
            if self1.seconds == 60:
                self1.minutes = self1.minutes + 1
                self1.seconds = 0
            if self1.minutes == 60:
                self1.hours = self1.hours + 1
                self1.minutes = 0
            
            return self1.returntime()

        def pausetimer(self1):
            self1.timeron = False
        
        def returntime(self1):
            seconds = self1.seconds
            if self1.seconds < 10:
                seconds = str("0" + str(self1.seconds))
            minutes = self1.minutes
            if self1.minutes < 10:
                minutes = str("0" + str(self1.minutes))
            hours = self1.hours
            if self1.hours < 10:
                hours = str("0" + str(self1.hours))
            return str(str(hours) + ":" + str(minutes) + ":" + str(seconds))
    
    def Window_Close(self, event = None):
        if messagebox.askokcancel("you sure?", "hehehehehshshs"):
            self.destroy()

screen1 = Main_S()