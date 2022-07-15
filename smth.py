from tkinter import *
import tkinter.font as font
import random
# import ASTRG as astg
# import ASTDG as astdg
# import ASTNFG as astnfg
import pyautogui as py
import keyboard as key


class ChoseWichGame(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.Dobbels = Button(self, text="Dobbels game", padx=50, pady=10)
        self.Dobbels.grid(row=1, column=1)
        self.Regular = Button(self, text="Regular", padx=50, pady=10)
        self.Regular.grid(row=1, column=2)
        self.lD = Button(self, text="leaderboard", padx=38, pady=10)
        self.lD.grid(row=2, column=2)
        self.noFlag = Button(self, text="No Flag", padx=50, pady=10)
        self.noFlag.grid(row=1, column=3)
        self.Regular.bind("<Button-1>", self.BindForRegular)
        self.Dobbels.bind("<Button-1>", self.bindfordobbles)
        self.lD.bind("<Button-1>", self.bindforleaderboard)
        self.noFlag.bind("<Button-1>", self.bindForNoFlag)

    # creates regular game input number screen
    def BindForRegular(self, smth=None):
        self.ISR = InputScreenRegular()

    # creates leaderboard
    def bindforleaderboard(self, event=None):
        self.LD = Leaderboard()

    # a bomb was clicked in the regular game
    def bombwasclickedR(self, event=None):
        self.ISR.bombwasclicked1()

    # you won the regular game
    def wingame(self, event=None):
        self.ISR.wonthegame()

    # a bomb was clicked in the Dobbels game
    def bombwasclickedD(self):
        self.createdobbelsgame(2)

    # you finished the dobbels game
    def CompletedDobbels(self):
        self.createdobbelsgame(3)

    # creates dobble game
    def bindfordobbles(self, event=None):
        self.createdobbelsgame(1)

    def bindForNoFlag(self, event=None):
        self.ISR = InputScreenRegular()
        self.ISR.noFlag = True

    def createdobbelsgame(self, num):
        """different sanariios will yeild different solutions
        1 = start up | will set tile size to 10
        2 = failed   | create a map with the same tile size as before
        3 = move on  | update tile size by one and create map"""
        if communicaterac() < 15:
            if num == 1:
                setracto10()
                self.curdobbelsgame = dobblegame()
                self.curdobbelsgame.CreateTiles(communicaterac(), communicaterac(),
                                 round(0.2 * communicaterac() * communicaterac() - communicaterac() * 0.02))
                self.DGT = SampleApp()
            elif num == 2:
                self.curdobbelsgame.plsquit()
                self.curdobbelsgame = dobblegame()
                self.curdobbelsgame.CreateTiles(communicaterac(), communicaterac(),
                                 round(0.2 * communicaterac() * communicaterac() - communicaterac() * 0.02))
            else:
                updatetilesize()
                self.curdobbelsgame.plsquit()
                self.curdobbelsgame = dobblegame()
                self.curdobbelsgame.CreateTiles(communicaterac(), communicaterac(),
                                 round(0.2 * communicaterac() * communicaterac() - communicaterac() * 0.02))
            print("map created with x and y = " + str(communicaterac()) + " with " + str(
                round(0.2 * communicaterac() * communicaterac() - communicaterac() * 0.02)) + " flags.")
        if communicaterac() == 15:
            self.destroy()


class InputScreenRegular(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # len and wid var switched because of mix up when creating map
        self.noFlag = False
        self.canvas1 = Canvas(self)
        self.inputwid = Entry(self)
        self.inputlen = Entry(self)
        self.inputfla = Entry(self)
        self.inputna = Entry(self)
        self.canvas1.create_text(200, 50, fill="darkblue", font="Times 25 bold", text="MINESWEEPER\n     REGULAR")
        self.canvas1.create_text(75, 140, fill="darkblue", text="length")
        self.canvas1.create_text(75, 170, fill="darkblue", text="width")
        self.canvas1.create_text(75, 200, fill="red", text="flags")
        self.canvas1.create_text(75, 230, fill="darkblue", text="name")
        self.canvas1.create_window(200, 140, window=self.inputwid)
        self.canvas1.create_window(200, 170, window=self.inputlen)
        self.canvas1.create_window(200, 200, window=self.inputfla)
        self.canvas1.create_window(200, 230, window=self.inputna)
        self.canvas1.grid(row=1, column=1)
        self.beginbutton = Button(self, text="!BEGIN!")
        myfont = font.Font(size=30)
        self.beginbutton["font"] = myfont
        self.beginbutton.grid(row=2, column=1)
        self.beginbutton.bind("<Button-1>", self.BindForBeginButton)
        self.c = 0
        self.r = 0
        self.f = 0
        self.n = 0


    def BindForBeginButton(self, event):
        rows = self.inputlen.get()
        columns = self.inputwid.get()
        flags = self.inputfla.get()
        name = self.inputna.get()
        rv1 = int(rows)*int(columns)/100
        rv1 = rv1*5
        if self.SeeIfNumber(rows) is True and self.SeeIfNumber(columns) is True and self.SeeIfNumber(flags) is True and rv1 <= int(flags) and int(rows)<50 and int(columns)<50 and int(flags)<1000:
            self.RG = RegularGame()
            if self.noFlag is False:
                self.RG.CreateTiles(int(rows), int(columns), int(flags))
            else:
                self.RG.CreateTiles(int(rows), int(columns), int(flags), noFlag=True)
            self.T = SampleApp()
            self.c = columns
            self.r = rows
            self.f = flags
            self.n = name

    def SeeIfNumber(self, astr):
        c1 = 0
        try:
            c = int(astr)
            c1 = 1
        except: pass
        if c1 == 1:
            return True

    def bombwasclicked1(self):
        self.RG.cheakifbombed()

    def wonthegame(self):
        self.RG.cheakifbombed()
        if self.noFlag is True:
            print("your score is "+str(self.T.clockfunction.changetime()))
            rav1=self.T.clockfunction.changetime()
            rav1 = rav1.split(":")
            rav1 = int(rav1[0])*3600 + int(rav1[1])*60 + int(rav1[2])
            astg.addvar(self.n, round(((int(self.r) * int(self.c) * 0.5) / int(self.f)) / rav1 * 100))
        else:
            print("your score is " + str(self.T.clockfunction.changetime()))
            rav1 = self.T.clockfunction.changetime()
            rav1 = rav1.split(":")
            rav1 = int(rav1[0]) * 3600 + int(rav1[1]) * 60 + int(rav1[2])
            astnfg.addvar(self.n, round(((int(self.r) * int(self.c) * 0.5) / int(self.f)) / rav1 * 100))



class RegularGame(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.bind("<Key>", self.keypreessed)
        self.MM = movemouse()
        self.bind("<Shift_L>", self.MM.shiftwaspressed)
        self.focus_force()

    def CreateTiles(self, rows, columns, flags, noFlag=None):
        flagcords = []
        for i in range(flags):
            smth1 = random.randint(0, rows - 1)
            smth2 = random.randint(0, columns - 1)
            flagcords.append([smth1, smth2])
        anotherrandomlist=[]

        # create all the buttons
        for i in range(rows):
            arandomlist = []
            for i1 in range(columns):
                if [i, i1] in flagcords:
                    if noFlag is None:
                        a = mybutton(self, i, i1, "  ", 16, 10, rows - 1, columns - 1, flagcords, 1, False, bomb=True)
                    else:
                        a = mybutton(self, i, i1, "  ", 16, 10, rows - 1, columns - 1, flagcords, 1, True, bomb=True)
                else:
                    if noFlag is None:
                        a = mybutton(self, i, i1, "  ", 16, 10, rows - 1, columns - 1, flagcords, 1, False)
                    else:
                        a = mybutton(self, i, i1, "  ", 16, 10, rows - 1, columns - 1, flagcords, 1, True)
                arandomlist.append(a)
            anotherrandomlist.append(arandomlist)
        ClassforallbuttonsR(anotherrandomlist)

        for i in communicateallbutR():
            for i1 in i:
                print(str(i1.r) + " " + str(i1.c))
        c_cg4 = 0
        while c_cg4 == 0:
            heyheyhey = [random.randint(0, rows - 1), random.randint(0, columns - 1)]
            if heyheyhey not in flagcords:
                c_cg4 = 1
        for i in communicateallbutR():
            for i1 in i:
                if i1.r == heyheyhey[0] and i1.c == heyheyhey[1]:
                    i1.change_color()

    def cheakifbombed(self):
        print("hey")
        self.destroy()

    def keypreessed(self, event=None):
        self.MM.keywaspressed()
        if event.char == "j":
            for i in communicateallbutR():
                for i1 in i:
                    i1.recivedn()
        if event.char == "l":
            for i in communicateallbutR():
                for i1 in i:
                    i1.reciveds()
        if event.char == "k":
            for i in communicateallbutR():
                for i1 in i:
                    i1.recivedd()


def ClassforallbuttonsR(alist):
    global allbut
    allbut = alist.copy()


def communicateallbutR():
    global allbut
    return allbut


def cleararea1R(alist):
    # geting objects from list of cords
    for i in alist:
        # opening the allbut list to find a button with the same row and column
        for i1 in allbut:
            # opening the list withing the main list of allbut
            for i2 in i1:
                if i[0] == i2.r and i[1] == i2.c:
                    if i2.ftf is False:
                        return False


def accuallyclearitR(anl):
    for i in anl:
        for i1 in allbut:
            for i2 in i1:
                if i2.r == i[0] and i2.c == i[1]:
                    i2.blowup(1)
                    i2.cleararea(num=1)


def cheakifwinR():
    global allbut
    c1 = 0
    for i in allbut:
        for i1 in i:
            if i1.b is False and i1.rev is False:
                c1 = 1
    if c1 == 0:
        for i in allbut:
            for i1 in i:
                if i1.b is True:
                    i1.change_colory()
                else:
                    i1.change_color()
                i1.B.bind("<Button-1>", app.wingame)
        print("sucsess!")


def showbombs():
    global allbut
    for i in allbut:
        for i1 in i:
            if i1.b is True:
                i1.change_colorr()
            i1.B.bind("<Button-1>", setblowupto1R)

def setblowupto1R(event=None):
    app.bombwasclickedR()


class SampleApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.clock = Label(self, text="")
        myfont = font.Font(size=1000)
        self.clock["font"] = myfont
        self.clock.pack()
        self.clockfunction = self.timer()

        # start the clock "ticking"
        self.update_clock()

    def update_clock(self):
        self.clock.configure(text=self.clockfunction.changetime())
        # call this function again in one second
        self.after(1000, self.update_clock)

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

        def pausetimer(self):
            self.timeron = False


class mybutton():
    def __init__(self, root, row, column, text, len, wid, maxrow, maxcol, bomblist, RoD, fall,bomb=False):
        # defining row and column (they are switched because I made a mistake)
        self.r = row
        self.c = column
        # for future use maybe
        self.t = text
        # length and width
        self.l = len
        self.w = wid
        # if this tile is a bob
        self.b = bomb
        # max cor for rows and max cor for columns
        self.mr = maxrow
        self.mc = maxcol
        # if has been revealed (for flag purposes)
        self.rev = False
        # flag on or off
        self.ftf = False
        # all bombs list
        self.ab = bomblist
        # for reveal purposes
        self.areacleared = False
        self.root = root
        # if thie button is in the regular or dobbles game
        # 1 = regular | 2 = dobbels
        self.rob = RoD
        # hoverin is for mobile, using keyboard inputs to play
        # see if the flag allowed mode is on
        self.fall = fall
        self.hoverin = False
        # selecting color
        if self.r % 2 == 0 and self.c % 2 == 0 or self.r % 2 == 1 and self.c % 2 == 1:
            self.col = "green"
        else:
            self.col = "dark green"
        # the actual button and putting it in
        self.B = Button(self.root, text=self.t, padx=self.l, pady=self.w, bg=self.col)
        self.B.grid(row=self.r, column=self.c)
        self.B.bind("<Button-1>", self.blowup)
        self.B.bind("a", self.blowup)
        self.B.bind("<Button-3>", self.putflag)
        self.B.bind("<Double-Button-1>", self.putflag)
        self.B.bind("s", self.putflag)
        self.B.bind("<Enter>", self.sethoverintoT)
        self.B.bind("<Leave>", self.sethoverintoF)

    def blowup(self, event=None):
        if self.ftf is False:
            # remove the button
            self.B.grid_remove()
            # get the new button's color
            if self.col == "green":
                self.col = "#afb576"
            if self.col == "dark green":
                self.col = "#838a5a"
            if self.b is True:
                self.col = "red"
            # finding how many bombs are nearby
            loc = [
                [self.r + 1, self.c - 1],
                [self.r, self.c - 1],
                [self.r - 1, self.c - 1],
                [self.r - 1, self.c],
                [self.r + 1, self.c],
                [self.r - 1, self.c + 1],
                [self.r, self.c + 1],
                [self.r + 1, self.c + 1]
            ]
            a = 0
            for i in loc:
                if i in self.ab:
                    a = a + 1
            if a != 0:
                self.t = str(a)
            # create the new button and put it in
            self.B = Button(self.root, text=self.t, padx=self.l, pady=self.w, bg=self.col)
            self.B.grid(row=self.r, column=self.c)
            self.B.bind("<Button-1><Button-3>", self.cleararea)
            print("you clicked on " + str(self.r) + " " + str(self.c))
            self.rev = True
            if self.b is True:
                if self.rob == 2:
                    # self.B.bind("<Button-1>", self.delete_all)
                    # self.B.bind("a", self.delete_all)
                    setblowupto1D()
                    print("YOU HAVE CLICKED ON A BOMB AFTER IT HAS BEEN DETONATED")
                else:
                    showbombs()
            self.cleararea(num=1)
            if self.rob == 2:
                cheakifwinD()
            else:
                cheakifwinR()

    def putflag(self, event=None):
        if self.fall == False:
            if self.rev is False:
                if self.ftf is False:
                    self.B.grid_remove()
                    self.B = Button(self.root, text="F", padx=self.l, pady=self.w, bg="orange")
                    self.B.grid(row=self.r, column=self.c)
                    self.B.bind("<Button-1>", self.blowup)
                    self.B.bind("a", self.blowup)
                    self.B.bind("<Button-3>", self.putflag)
                    self.B.bind("s", self.putflag)
                    self.B.bind("<Enter>", self.sethoverintoT)
                    self.B.bind("<Leave>", self.sethoverintoF)
                    self.ftf = True
                elif self.ftf is True:
                    self.B.grid_remove()
                    self.B = Button(self.root, text="  ", padx=self.l, pady=self.w, bg=self.col)
                    self.B.grid(row=self.r, column=self.c)
                    self.B.bind("<Button-1>", self.blowup)
                    self.B.bind("a", self.blowup)
                    self.B.bind("<Button-3>", self.putflag)
                    self.B.bind("s", self.putflag)
                    self.B.bind("<Enter>", self.sethoverintoT)
                    self.B.bind("<Leave>", self.sethoverintoF)
                    self.ftf = False

    def cleararea(self, event=None, num=None):
        if self.areacleared is False and self.ftf is False:
            if num == 1 and self.areacleared is False or num == 2:
                loc = [
                    [self.r + 1, self.c - 1],
                    [self.r, self.c - 1],
                    [self.r - 1, self.c - 1],
                    [self.r - 1, self.c],
                    [self.r + 1, self.c],
                    [self.r - 1, self.c + 1],
                    [self.r, self.c + 1],
                    [self.r + 1, self.c + 1]
                ]
                anotherrandomlist = []
                for i in loc:
                    if i in self.ab:
                        print("found a flag nearby")
                        anotherrandomlist.append(i)
                if self.rob == 1:
                    if cleararea1R(anotherrandomlist) is None:
                        self.areacleared = True
                        accuallyclearitR(loc)
                else:
                    if cleararea1D(anotherrandomlist) is None:
                        self.areacleared = True
                        accuallyclearitD(loc)

    def change_color(self):
        self.B.grid_remove()
        self.B = Button(self.root, text="  ", padx=self.l, pady=self.w, bg="blue")
        self.B.bind("<Button-1>", self.blowup)
        self.B.bind("a", self.blowup)
        self.B.bind("<Button-3>", self.putflag)
        self.B.bind("s", self.putflag)
        self.B.grid(row=self.r, column=self.c)
        self.B.bind("<Enter>", self.sethoverintoT)
        self.B.bind("<Leave>", self.sethoverintoF)

    def change_colorr(self):
        self.B.grid_remove()
        self.B = Button(self.root, text="  ", padx=self.l, pady=self.w, bg="red")
        self.B.bind("<Button-1>", self.blowup)
        self.B.bind("a", self.blowup)
        self.B.bind("<Button-3>", self.putflag)
        self.B.bind("s", self.putflag)
        self.B.grid(row=self.r, column=self.c)
        self.B.bind("<Enter>", self.sethoverintoT)
        self.B.bind("<Leave>", self.sethoverintoF)

    def change_colory(self):
        self.B.grid_remove()
        self.B = Button(self.root, text="  ", padx=self.l, pady=self.w, bg="yellow")
        self.B.bind("<Button-1>", self.blowup)
        self.B.bind("a", self.blowup)
        self.B.bind("<Button-3>", self.putflag)
        self.B.bind("s", self.putflag)
        self.B.grid(row=self.r, column=self.c)
        self.B.bind("<Enter>", self.sethoverintoT)
        self.B.bind("<Leave>", self.sethoverintoF)

    def sethoverintoT(self, event=None):
        self.hoverin = True

    def sethoverintoF(self, event=None):
        self.hoverin = False

    def recivedn(self, event=None):
        if self.hoverin is True:
            self.blowup()

    def reciveds(self, event=None):
        if self.hoverin is True:
            self.putflag()

    def recivedd(self, event=None):
        if self.hoverin is True:
            self.cleararea(num=2)


def updatetilesize():
    global rac
    rac = rac + 1

def setracto10():
    global rac
    rac = 10


def communicaterac():
    global rac
    return rac


def ClassforallbuttonsD(alist):
    global allbut
    allbut = alist.copy()


def communicateallbutD():
    global allbut
    return allbut


def cleararea1D(alist):
    # geting objects from list of cords
    for i in alist:
        # opening the allbut list to find a button with the same row and column
        for i1 in allbut:
            # opening the list withing the main list of allbut
            for i2 in i1:
                if i[0] == i2.r and i[1] == i2.c:
                    if i2.ftf is False:
                        return False


def accuallyclearitD(anl):
    for i in anl:
        for i1 in allbut:
            for i2 in i1:
                if i2.r == i[0] and i2.c == i[1]:
                    i2.blowup(1)
                    i2.cleararea(num=1)


def cheakifwinD():
    global allbut
    c1 = 0
    for i in allbut:
        for i1 in i:
            if i1.b is False and i1.rev is False:
                c1 = 1
    if c1 == 0:
        for i in allbut:
            for i1 in i:
                if i1.b is True:
                    i1.change_colory()
                i1.B.bind("<Button-1>", StartProccesOfNewMapSize)
        print("sucsess!")


def setblowupto1D(event=None):
    app.bombwasclickedD()


def StartProccesOfNewMapSize(event = None):
    app.CompletedDobbels()


class dobblegame(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.MoMo = movemouse()
        self.bind("<Key>", self.MoMo.keywaspressed)
        self.bind("j", self.keywaspressed)
        self.bind("l", self.keywaspressed)

    def CreateTiles(self, rows, columns, flags):
        flagcords = []
        for i in range(flags):
            smth1 = random.randint(0, rows - 1)
            smth2 = random.randint(0, columns - 1)
            flagcords.append([smth1, smth2])
        anotherrandomlist=[]

        # create all the buttons
        for i in range(rows):
            arandomlist = []
            for i1 in range(columns):
                if [i, i1] in flagcords:
                    a = mybutton(self, i, i1, "  ", 16, 10, rows - 1, columns - 1, flagcords, 2, False, bomb=True)
                else:
                    a = mybutton(self, i, i1, "  ", 16, 10, rows - 1, columns - 1, flagcords, 2, False)
                arandomlist.append(a)
            anotherrandomlist.append(arandomlist)
        ClassforallbuttonsD(anotherrandomlist)

        for i in communicateallbutD():
            for i1 in i:
                print(str(i1.r) + " " + str(i1.c))
        c_cg4 = 0
        while c_cg4 == 0:
            heyheyhey = [random.randint(0, rows - 1), random.randint(0, columns - 1)]
            if heyheyhey not in flagcords:
                c_cg4 = 1
        for i in communicateallbutD():
            for i1 in i:
                if i1.r == heyheyhey[0] and i1.c == heyheyhey[1]:
                    i1.change_color()

    def keywaspressed(self, event=None):
        if event.char == "j":
            for i in communicateallbutR():
                for i1 in i:
                    i1.recivedn()
        if event.char == "l":
            for i in communicateallbutR():
                for i1 in i:
                    i1.reciveds()
        if event.char == "k":
            for i in communicateallbutR():
                for i1 in i:
                    i1.recivedd()
    def plsquit(self):
        self.destroy()


class Leaderboard(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        SB = Scrollbar(self)
        SB.pack(side=RIGHT, fill = Y)
        mylist = Listbox(self, yscrollcommand = SB.set)
        a = astg.returnmainlist()
        for person in a:
            mylist.insert(END, str(person.n)+" has "+str(person.s))
        mylist.pack(side=LEFT, fill=BOTH)
        SB.config(command=mylist.yview)


class movemouse():
    def __init__(self):
        position = py.position()
        print(position)
        self.x = position[0]
        print(self.x)
        self.y = position[1]
        print(self.y)
        self.changevar = 20
        self.shifttf = False

    def keywaspressed(self, event=None):
        if not(key.is_pressed("l")) and not(key.is_pressed("j")):
            if key.is_pressed("s") and key.is_pressed("a"):
                # left down
                self.x = self.x - self.changevar
                self.y = self.y + self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("w") and key.is_pressed("d"):
                # right up
                self.x = self.x + self.changevar
                self.y = self.y - self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("a") and key.is_pressed("w"):
                # up left
                self.x = self.x - self.changevar
                self.y = self.y - self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("d") and key.is_pressed("s"):
                # down right
                self.x = self.x + self.changevar
                self.y = self.y + self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("a") and not(key.is_pressed("w")) and not(key.is_pressed("s")) and not(key.is_pressed("d")):
                # left
                self.x = self.x - self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("d") and not(key.is_pressed("a")) and not(key.is_pressed("s")) and not(key.is_pressed("w")):
                # right
                self.x = self.x + self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("w") and not (key.is_pressed("a")) and not (key.is_pressed("s")) and not (key.is_pressed("d")):
                # up
                self.y = self.y - self.changevar
                py.moveTo(self.x, self.y)

            elif key.is_pressed("s") and not (key.is_pressed("a")) and not (key.is_pressed("w")) and not (key.is_pressed("d")):
                # down
                self.y = self.y + self.changevar
                py.moveTo(self.x, self.y)

            else:
                pass

    def shiftwaspressed(self, event=None):
        print("shift was pressed")
        if self.shifttf is True:
            self.changevar = 60
            self.shifttf = False
        else:
            self.changevar = 30
            self.shifttf = True

if __name__ == "__main__":
    global rac
    rac = 0
    allbombs=[]
    app = ChoseWichGame()
    app.mainloop()