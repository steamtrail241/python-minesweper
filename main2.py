from tkinter import *
from tkinter import messagebox
import random, time

bombsList = []
allTiles=[]
bombsNearby = []
mainscreen = 0
regularscreen = 0
doublesscreen = 0
maxRows = 0
maxColumns = 0
xFocus = 0
yFocus = 0


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




class Tile(Button1):

    # color options
    colors = {
        "dark green": "#1b5e02",
        "light green": "#2d8a0a",
        "dark green highlight": "#e34d4e",
        "light green highlight": "#e34d4d",
        "light brown": "#afb576",
        "dark brown": "#838a5a",
    }


    def __init__(self, root, row, column, len, wid, text=" ", bomb=False):
        super().__init__(root, row, column, len, wid, text)

        self.isBomb = bomb

        self.isReveal = False

        self.isFlaged = False

        self.isAreaCleared = False

        self.hover = False

        self.theOne = False

        self.numberOfBombsNearby = text

        r = self.row % 2
        c = self.column % 2

        if (r == 0 and c == 0) or (r == 1 and c == 1):
            self.color = self.colors["dark green"]
            self.foreGround = self.colors["dark green"]
        else:
            self.color = self.colors["light green"]
            self.foreGround = self.colors["light green"]
        
        self.update()
        
        self.button.bind("<Button-1>", self.leftClick)
        self.button.bind("<Button-3>", self.rightClick)


    def leftClick(self, event=None):
        print("["+str(self.row)+","+str(self.column)+"],")
        if not self.isFlaged and not self.isBomb and not self.isReveal:

            if self.isBomb:
                print("your dead")
                for i in bombsList:
                    allTiles[i[0]][i[1]].color = "brown"
                    allTiles[i[0]][i[1]].foreGround = "brown"
                    allTiles[i[0]][i[1]].update()
                for i in allTiles:
                    for i1 in i:
                        i1.button.bind("<Button-1>", destoryGame)

            if self.color == self.colors["light green"] or self.color == self.colors["light green highlight"]:
                self.color = self.colors["light brown"]
                self.foreGround = "black"
                if self.txt == "0":
                    self.foreGround = self.color
            
            if self.color == self.colors["dark green"] or self.color == self.colors["dark green highlight"]:
                self.color = self.colors["dark brown"]
                self.foreGround = "black"
                if self.txt == "0":
                    self.foreGround = self.color
            
            self.update()

            self.isReveal = True
            self.button.bind("<Button-1><Button-3>", self.leftRightClick)
            self.clearAround()
        
        if not self.isFlaged and self.isBomb and not self.isReveal:
            print("your dead")
            for i in bombsList:
                allTiles[i[0]][i[1]].color = "brown"
                allTiles[i[0]][i[1]].foreGround = "brown"
                allTiles[i[0]][i[1]].update()
            for i in allTiles:
                for i1 in i:
                    i1.button.bind("<Button-1>", destoryGame)

    def rightClick(self, event=None):
        if not self.isReveal:
            if not self.isFlaged:
                self.txt = "F"
                self.color = "orange"
                self.len -= 1

                self.update()

                self.isFlaged = True

                self.button.bind("<Button-1>", self.leftClick)
                self.button.bind("<Button-3>", self.rightClick)
            else:
                self.len += 1
                self.isFlaged = False
                self.txt = self.numberOfBombsNearby
                r = self.row%2
                c = self.column%2
                if r == 0 and c == 0 or r == 1 and c == 1:
                    self.color = self.colors["dark green"]
                else:
                    self.color = self.colors["light green"]
                self.update()
                self.button.bind("<Button-1>", self.leftClick)
                self.button.bind("<Button-3>", self.rightClick) 


    def clearAround(self, event=None):
        if self.isReveal is True and self.isAreaCleared is False:
            locations = [
                [self.row + 1, self.column - 1],
                [self.row, self.column - 1],
                [self.row - 1, self.column - 1],
                [self.row - 1, self.column],
                [self.row + 1, self.column],
                [self.row - 1, self.column + 1],
                [self.row, self.column + 1],
                [self.row + 1, self.column + 1]
            ]

            for i in locations:
                if i[0]<0 or i[0]>maxRows-1 or i[1]<0 or i[1]>maxColumns-1:
                    locations[locations.index(i)] = "_"

            if self.numberOfBombsNearby == "0":
                for i in locations:
                    if not i == "_" and not allTiles[i[0]][i[1]].isReveal and not allTiles[i[0]][i[1]].isAreaCleared and not allTiles[i[0]][i[1]].isBomb:
                        try:
                            allTiles[i[0]][i[1]].leftClick()
                        except(RecursionError):
                            break
                self.isAreaCleared = True
    
    def leftRightClick(self, event=None):
        if self.txt != "0":
            begining = time.time()
            locations = [
                [self.row + 1, self.column - 1],
                [self.row, self.column - 1],
                [self.row - 1, self.column - 1],
                [self.row - 1, self.column],
                [self.row + 1, self.column],
                [self.row - 1, self.column + 1],
                [self.row, self.column + 1],
                [self.row + 1, self.column + 1]
            ]

            for i in locations:
                if i[0]<0 or i[0]>maxRows-1 or i[1]<0 or i[1]>maxColumns-1:
                    locations[locations.index(i)] = "_"
            
            checkBombsAreFlaged = True
            for i in locations:
                if i != "_":
                    if allTiles[i[0]][i[1]].isBomb and not allTiles[i[0]][i[1]].isFlaged:
                        checkBombsAreFlaged = False
                        break
            
            if checkBombsAreFlaged:
                for i in locations:
                    if i != "_" and not allTiles[i[0]][i[1]].isBomb:
                        allTiles[i[0]][i[1]].leftClick()
            print(time.time()-begining)

    def highlight(self, event=None):

        checkChange = False
        if self.color == self.colors["dark green"]:
            self.color = self.colors["dark green highlight"]
            self.foreGround = self.colors["dark green highlight"]
            checkChange = True
        if self.color == self.colors["light green"]:
            self.color = self.colors["light green highlight"]
            self.foreGround = self.colors["light green highlight"]
            checkChange = True
        if self.color == self.colors["dark green highlight"] and not checkChange:
            self.color = self.colors["dark green"]
            self.foreGround = self.colors["dark green"]
        if self.color == self.colors["light green highlight"] and not checkChange:
            self.color = self.colors["light green"]
            self.foreGround = self.colors["light green"]
        self.update()
        self.button.bind("<Button-1>", self.leftClick)
        self.button.bind("<Button-3>", self.rightClick)




class MainScreen(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.doublesButton = Button1(
            self,
            0, 0,
            50, 10,
            text="doubles game",
            leftClick=self.leftClickDouble,
            Enter=self.enterDouble,
            Leave=self.leaveDouble,
        )

        self.regularButton = Button1(
            self,
            0, 1,
            50, 10,
            text="Reguar Game",
            leftClick=self.leftClickRegular,
            Enter=self.enterRegular,
            Leave=self.leaveRegular,
        )

        self.mainloop()
    

    def leftClickDouble(self, event=None):
        pass


    def enterDouble(self, event=None):
        pass


    def leaveDouble(self, even=None):
        pass


    def leftClickRegular(self, event=None):
        startRegular(25, 40, 100)


    def enterRegular(self, event=None):
        pass


    def leaveRegular(self, event=None):
        pass





def startRegular(row, column, bombs):
    global regularscreen
    global bombsList
    global bombsNearby
    global allTiles
    global maxRows
    global maxColumns
    global xFocus
    global yFocus

    maxRows = row
    maxColumns = column
    
    bombsList = []

    for i in range(bombs):
        check1 = False
        while check1 is False:

            smth1 = random.randint(0, row-1)
            smth2 = random.randint(0, column-1)

            if [smth1, smth2] not in bombsList:
                bombsList.append([smth1, smth2])
                check1 = True
    
    allTiles = []
    print(bombsList)
    bombsNearby = []

    for i in range(row):
        mini = []
        for i1 in range(column):
            locations = [
                [i + 1, i1 - 1],
                [i, i1 - 1],
                [i - 1, i1 - 1],
                [i - 1, i1],
                [i + 1, i1],
                [i - 1, i1 + 1],
                [i, i1 + 1],
                [i + 1, i1 + 1]
            ]
            numberOfBombsNearbyForEachTile = 0
            for i2 in locations:
                if i2 in bombsList:
                    numberOfBombsNearbyForEachTile += 1
            
            mini.append(numberOfBombsNearbyForEachTile)
        bombsNearby.append(mini)
    
    regularscreen = RegularScreen()
    regularscreen.initialize(row, column)

    check2 = 0
    while check2 != -1:
        num1 = random.randint(0, row-1)
        num2 = random.randint(0, column-1)
        if allTiles[num1][num2].txt == "0":
            originalColor = allTiles[num1][num2].color
            allTiles[num1][num2].color = "blue"
            allTiles[num1][num2].foreGround = "blue"
            allTiles[num1][num2].update()
            allTiles[num1][num2].color = originalColor
            allTiles[num1][num2].button.bind("<Button-1>", allTiles[num1][num2].leftClick)
            # allTiles[num1][num2].theOne = True
            xFocus = num1
            yFocus = num2
            check2 = -2
        check2 += 1
        if check2>row*column*10:
            break
    if check2==row*column*10+1:
        print("not available")
    print(allTiles)
    timer = Timer()
    regularscreen.updateTitle(timer, 5)
    regularscreen.checkWin()


def keyWasPressed(key):
    global xFocus
    global yFocus
    xPrev = xFocus
    yPrev = yFocus
    match(key):
        case "j":
            allTiles[xFocus][yFocus].leftClick()
        case "w":
            xFocus -= 1
        case "a":
            yFocus -= 1
        case "s":
            xFocus += 1
        case "d":
            yFocus += 1
        case "l":
            allTiles[xFocus][yFocus].rightClick()
        case other:
            pass
    allTiles[xFocus][yFocus].highlight()
    allTiles[xPrev][yPrev].highlight()

def destoryGame(event=None):
    regularscreen.destroy()



class RegularScreen(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.bind("<Key>", self.keyPressed)
        self.bind("<space>", self.spacePressed)
        self.bind("<Tab><space>", self.tabSpacePressed)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.windowCloseEvent)


    def initialize(self, row, column, event=None):
        print(bombsList)
        for i in range(row):
            mini = []
            for i1 in range(column):
                if [i, i1] in bombsList:
                    newTile = Tile(self, i, i1, 8, 4, text="9", bomb=True)
                    mini.append(newTile)
                else:
                    newTile = Tile(self, i, i1, 8, 4, text=str(bombsNearby[i][i1]))
                    mini.append(newTile)
            allTiles.append(mini)


    def keyPressed(self, event):
        print(event.char)
        keyWasPressed(event.char)
    

    def spacePressed(self, event=None):
        keyWasPressed("space")
    

    def tabSpacePressed(self, event=None):
        keyWasPressed("tabspace")
    

    def updateTitle(self, timerObj, num):

        flags = len(bombsList)
        for i in allTiles:
            for i1 in i:
                if i1.isFlaged:
                    flags -= 1
        
        if num == 5:
            timerObj.changeTime()
            num = 0
        num += 1

        self.title(timerObj.returnTime()+"  |  "+str(flags)+" flags")
        self.after(200, self.updateTitle, timerObj, num)
    

    def checkWin(self, event=None):
        checkWin = True
        for i in allTiles:
            for i1 in i:
                if not i1.isBomb and not i1.isReveal:
                    checkWin = False
                    break
        if checkWin:
            for i in allTiles:
                for i1 in i:
                    if not i1.isBomb:
                        i1.color = "blue"
                        i1.foreGround = "blue"
                        i1.update()
                        i1.button.bind("<Button-1>", destoryGame)
        else:
            self.after(100, self.checkWin)
    

    def windowCloseEvent(self, event=None):
        check = False
        for i in allTiles:
            for i1 in i:
                if not i1.isBomb and i1.isReveal:
                    check = True
        if check:
            if messagebox.askokcancel("you sure?", "you are not finished this game\nare you sure you would like to exit"):
                self.destroy()
        else:
            self.destroy()



class Timer():
    def __init__(self):
        self.timeron = True
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def changeTime(self):
        if self.timeron is True:
            self.seconds = self.seconds + 1
        if self.seconds == 60:
            self.minutes = self.minutes + 1
            self.seconds = 0
        if self.minutes == 60:
            self.hours = self.hours + 1
            self.minutes = 0

        return self.returnTime()
    
    def returnTime(self):
        seconds = self.seconds
        if self.seconds < 10:
            seconds = str("0" + str(self.seconds))
        minutes = self.minutes
        if self.minutes < 10:
            minutes = str("0" + str(self.minutes))
        hours = self.hours
        if self.hours < 10:
            hours = str("0" + str(self.hours))
        return str(str(hours) + ":" + str(minutes) + ":" + str(seconds))
    
    def pauseTimer(self):
        self.timeron = False

mainscreen = MainScreen()

