from tkinter import *
from tkinter import messagebox
from tkinter import Entry
import random

from tkinter import Button
from tkinter import Entry
from tkinter import Tk

bombsList = []
allTiles = []
bombsNearby = []
mainscreen = 0
regularscreen = 0
doublesscreen = 0
maxRows = 0
maxColumns = 0
bombcount = 20
xFocus = 0
yFocus = 0
gameOver = False


# ====================================================================================================================================================
# Button class
# ====================================================================================================================================================
class Button1():
    """
    A class to represent a button that a user can click

    Attributes:
        root (object): the window object
        row (int): the row that this button is in
        column (int): the column that this button is in
        len (int): the length for the button
        wid (int): the width for the button
        txt (str, optinal): the text for the button to display
        color (str, optinal):
            the background color for the button to display
        fg (str, optinal): the text color for the button to display
        leftClick (function, optinal):
            the function to call when the button is left clicked
        Enter (function, optinal):
            the function to call when the user cursor enters the button
        Leave (function, optinal):
            the function to call when the user cursor leaves the button

    Methods:
        update(): updates the button to match the attributes
    """
    def __init__(self, root, row, column, len, wid, text=" ", color="white", fg="black", leftClick=None, Enter=None, Leave=None):
        self.root, self.row, self.column, self.len = root, row, column, len
        self.width, self.txt, self.color, self.foreGround = wid, text, color, fg

        self.button = Button(
            self.root,
            text=self.txt,
            padx=self.len,
            pady=self.width,
            bg=self.color,
            fg=self.foreGround
        )

        # Put the button on the window at the column and row that was given
        self.button.grid(row=self.row+1, column=self.column)
        self.button.bind("<Button-1>", leftClick)
        self.button.bind("<Enter>", Enter)
        self.button.bind("<Leave>", Leave)

    def update(self):
        """
        updates the button to match the attributes


        """
        self.button.config(
            text=self.txt,
            padx=self.len,
            pady=self.width,
            bg=self.color,
            fg=self.foreGround
        )


# =====================================================================
# Tile for minesweeper games
# =====================================================================
class Tile(Button1):
    """
    used to represent a tile in a game of minesweeper.

    Attributes:
        all the attributes that the Button1() class has
        isBomb (bool): if the tile is a bomb
        isReveal (bool): if the tile is uncovered
        isFlaged (bool): if the tile is flaged
        isAreaCleared (bool):
            if the tile has already cleared the area around it
        hover (bool): if the cursor is hovering over this tile
        numberOfBombsNearby (int): the number of bombs nearby
        lightTiles (bool): if the tile is a light tile

    Methods:
        leftClick(event=None): When the user left clicks the tile.
        rightClick(event=None): When the user right clicks the tile.
        clearAround(event=None): Clears the tiles around this tile.
        leftRightClick(event=None):
            Called when user presses left and right at the same time.
        highlight(event=None):
            Highlights and de-highlights tile based on where cursor is.
    """

    # color options
    colors = {
        "dark green": "#1b5e02",
        "light green": "#2d8a0a",
        "dark green highlight": "#e34d4e",
        "light green highlight": "#e34d4d",
        "light brown": "#afb576",
        "dark brown": "#838a5a",
        "cyan": "#1fdecb",
    }

    def __init__(self, root, row, column, len, wid, text=" ", lightTile=False, bomb=False):
        """
        Initializes the button object.

        Args:
            root (Tk): Window object
            row (int): the row that the tile it is on
            column (int): the column that the tile is on
            len (int): length of the tile
            wid (int): the width of the tile
            text (str): the string for the tile to represent
            light_tile (bool): if the tile is a light tile
            bomb (bool): if the tile is a bomb
        """
        super().__init__(root, row, column, len, wid, text)

        self.isBomb = bomb

        self.isReveal = self.isFlaged = self.isAreaCleared = self.hover = False

        self.theOne = False

        self.numberOfBombsNearby = int(text)

        self.txt = " "

        self.lightTiles = lightTile

        if self.lightTiles:
            self.color = self.colors["light green"]
            self.foreGround = self.colors["light green"]
        else:
            self.color = self.colors["dark green"]
            self.foreGround = self.colors["dark green"]

        self.update()

        self.button.bind("<Button-1>", self.leftClick)
        self.button.bind("<Button-3>", self.rightClick)

    def leftClick(self, event=None):
        """
        When the user left clicks the tile.

        Once left clicked, change the color to the brown background
        color, update the tile, and try to clear the tiles around it

        Args:
            event (Tk)(optional): Tk event
        """
        if not self.isFlaged and not self.isBomb and not self.isReveal:

            # change tile color based on it's position in checkerboard pattern
            if self.color == self.colors["light green"] or self.color == self.colors["light green highlight"]:
                self.color = self.colors["light brown"]
                self.foreGround = "black"
                if self.numberOfBombsNearby != 0:
                    self.txt = self.numberOfBombsNearby
                    self.len -= 2

            if self.color == self.colors["dark green"] or self.color == self.colors["dark green highlight"]:
                self.color = self.colors["dark brown"]
                self.foreGround = "black"
                if self.numberOfBombsNearby != 0:
                    self.txt = self.numberOfBombsNearby
                    self.len -= 2

            # updates changes in color to UI
            self.update()

            self.isReveal = True

            # adds clear around (based on flags) to tile
            self.button.bind("<Button-1><Button-3>", self.leftRightClick)

            # calls clear around (based on if there are bombs around tile)
            self.clearAround()

        # checks if user clicked on a bomb
        if not self.isFlaged and self.isBomb and not self.isReveal:
            global gameOver
            gameOver = True
            print("your dead")

            # changes all tiles that are bombs to a brown color
            for i in bombsList:
                allTiles[i[0]][i[1]].color = "brown"
                allTiles[i[0]][i[1]].foreGround = "brown"
                allTiles[i[0]][i[1]].update()

            # binds all Tiles to destory game when clicked
            for i in allTiles:
                for i1 in i:
                    i1.button.bind("<Button-1>", destoryGame)

    def rightClick(self, event=None):
        """
        When the user right clicks the tile.

        Add or remove the flag from this tile

        Args:
            event (Tk)(optional): Tk event
        """
        if not self.isReveal:

            # if tile is not flaged
            if not self.isFlaged:

                """
                change color to orange, text to "F" and bind
                appropriate functions
                """
                self.txt = "F"
                self.color = "orange"
                self.len -= 2
                self.foreGround = "black"

                self.update()

                self.isFlaged = True

                self.button.bind("<Button-1>", self.leftClick)
                self.button.bind("<Button-3>", self.rightClick)
            else:

                """
                change length back, set flagged variable to false,
                change text back, change original color back,
                bind appropriate functions
                """
                self.len += 2
                self.isFlaged = False
                self.txt = " "
                if self.lightTiles:
                    self.color = self.colors["light green"]
                else:
                    self.color = self.colors["dark green"]
                self.update()
                self.button.bind("<Button-1>", self.leftClick)
                self.button.bind("<Button-3>", self.rightClick)

    def clearAround(self, event=None):
        """
        Clears the tiles around this tile.

        Checks to see if there are any bombs around this tile and if it
        is it will go and clear the tiles around itself.

        Args:
            event (Tk)(optional): Tk event
        """
        if self.isReveal is True and self.isAreaCleared is False and self.numberOfBombsNearby != 9:

            self.isAreaCleared = True

            # lists co-ordinates of tiles next to this tile
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

            locations = [i for i in locations if not (i[0] < 0 or
                         i[0] > maxRows-1 or i[1] < 0 or i[1] > maxColumns-1)]

            # checks if this tile has no bombs around it
            if self.numberOfBombsNearby != 0:
                return

            for i in locations:
                t = allTiles[i[0]][i[1]]
                if not t.isReveal and not t.isAreaCleared and not t.isBomb:
                    try:
                        t.clearAround()
                        t.leftClick()
                    except (RecursionError):
                        print("recursion")
                        print(i)

    def leftRightClick(self, event=None):
        """
        Called when user presses left and right at the same time.

        Checks to see if all the bombs around this tile (if any) are all
        flaged and if it is it will go and clear the tiles around
        itself.

        Args:
            event (Tk)(optional): Tk event
        """
        if self.numberOfBombsNearby != 0 and self.isReveal and not self.isFlaged:

            # lists co-ordinates of tiles next to this tile
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

            locations = [i for i in locations if not (i[0] < 0 or
                         i[0] > maxRows-1 or i[1] < 0 or i[1] > maxColumns-1)]

            # Checks that all tiles that are bombs around this tile are flaged
            check_flaged = True
            for i in locations:
                t = allTiles[i[0]][i[1]]
                if t.isBomb and not t.isFlaged:
                    check_flaged = False
                    break

            # Clears tiles around this tile
            if check_flaged:
                # Clear tiles around this tile if they are not a bomb
                [allTiles[i[0]][i[1]].leftClick()
                 for i in locations if not allTiles[i[0]][i[1]].isBomb]

    def highlight(self, event=None):
        """
        Highlights and de-highlights tile based on where cursor is.

        this is for when the user used WASD and JL to play the game and
        the userneeds to know where their cursor is.

        Args:
            event (Tk)(optional): Tk event
        """
        change = False
        if self.color == self.colors["dark green"]:
            self.color = self.colors["dark green highlight"]
            self.foreGround = self.colors["dark green highlight"]
            change = True

        if self.color == self.colors["light green"]:
            self.color = self.colors["light green highlight"]
            self.foreGround = self.colors["light green highlight"]
            change = True
        
        if change is False:

            if self.color == self.colors["dark green highlight"]:
                self.color = self.colors["dark green"]
                self.foreGround = self.colors["dark green"]
            if self.color == self.colors["light green highlight"]:
                self.color = self.colors["light green"]
                self.foreGround = self.colors["light green"]

            if self.color == self.colors["dark brown"] or self.color == self.colors['light brown']:
                self.color = self.colors["cyan"]
                self.foreGround = self.colors["cyan"]
                if self.numberOfBombsNearby == "0":

                    if not self.lightTiles:
                        self.foreGround = self.colors["dark green"]
                    else:
                        self.foreGround = self.colors["light green"]
                change = True

            if self.color == self.colors["cyan"]:

                if not self.lightTiles:
                    self.color = self.colors["dark brown"]
                    self.foreGround = "black"
                    if self.numberOfBombsNearby == "0":
                        self.foreGround = self.colors["dark brown"]
                else:
                    self.color = self.colors["light brown"]
                    self.foreGround = "black"
                    if self.numberOfBombsNearby == "0":
                        self.foreGround = self.colors["light brown"]

        self.update()
        self.button.bind("<Button-1>", self.leftClick)
        self.button.bind("<Button-3>", self.rightClick)


# ====================================================================================================================================================
# Input boxes with or without buttons to change value
# ====================================================================================================================================================
class Inputer():
    """Input boxes with buttons to select Row Column and Name."""

    def __init__(self, root, row, column, padx, pady,
                 defaultText, limit, boxes=False):
        """
        Initialize inputer class.

        Args:
            root (tk): the window object
            row (int): the row you want the input box to be on
            column (int): the column you want the input box to be on
            padx (int): the length of the input box
            pady (int): the hight of the input box
            defaultText (str): the default text for the input box
        """
        self.root = root
        self.row = row
        self.column = column
        self.x = padx
        self.y = pady
        self.contains = int(defaultText)
        self.limit = limit

        self.entry = Entry(self.root)
        self.entry.grid(row=row, column=column+3)

        if boxes:
            self.leftChange10 = Button1(
                root,
                row-1, column,
                10, 0,
                text="<<<",
                leftClick=lambda event: self.changeAmount(-10)
            )

            self.leftChange5 = Button1(
                root,
                row-1, column + 1,
                12, 0,
                text="<<",
                leftClick=lambda event: self.changeAmount(-5)
            )

            self.leftChange1 = Button1(
                root,
                row-1, column + 2,
                14, 0,
                text="<",
                leftClick=lambda event: self.changeAmount(-1)
            )

            self.rightChange1 = Button1(
                root,
                row-1, column + 4,
                14, 0,
                text=">",
                leftClick=lambda event: self.changeAmount(1)
            )

            self.rightChange5 = Button1(
                root,
                row-1, column + 5,
                12, 0,
                text=">>",
                leftClick=lambda event: self.changeAmount(5)
            )

            self.rightChange10 = Button1(
                root,
                row-1, column + 6,
                10, 0,
                text=">>>",
                leftClick=lambda event: self.changeAmount(10)
            )

        self.update()

    def update(self):
        """Update the text inside the input box."""
        self.entry.delete(0, 100)
        self.entry.insert(-1, str(self.contains))

    def changeAmount(self, amount):
        """
        Change the amount by an amount.

        Args:
            amount (int): the amount to change by
        """
        if self.entry.get().isnumeric():
            test = self.contains + amount
            if test > self.limit:
                self.contains = self.limit
            elif test < 0:
                self.contains = 0
            else:
                self.contains = test
            print("changed by:"+str(amount))
            self.update()
        else:
            self.root.title("that isn't a number please try again")
            self.update()


class MainScreen(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # creates a button to start doubles game
        self.doublesButton = Button1(
            self,
            0, 0,
            50, 10,
            text="doubles game",
            leftClick=self.leftClickDouble,
            Enter=self.enterDouble,
            Leave=self.leaveDouble,
        )
        self.doublesButton.button.bind("<mutton-1", None)

        # creats a button to start regular game
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

    # user left clicked the double game button
    def leftClickDouble(self, event=None):
        pass

    # mouse entered the double game button
    def enterDouble(self, event=None):
        pass

    # mouse left the double game button
    def leaveDouble(self, even=None):
        pass

    # user left clicked the regular game button
    def leftClickRegular(self, event=None):
        startRegularInputs()

    # mouse entered the regular game button
    def enterRegular(self, event=None):
        pass

    # mouse left the regular game button
    def leaveRegular(self, event=None):
        pass


def startRegularInputs():
    asdfasdfsdf = InputRegularScreen()


def startRegular(row, column, bombs):
    global regularscreen
    global bombsList
    global bombsNearby
    global allTiles
    global maxRows
    global maxColumns
    global xFocus
    global yFocus
    global gameOver

    gameOver = False

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
        if allTiles[num1][num2].numberOfBombsNearby == 0:
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
        if check2 > row*column*10:
            break
    if check2 == row*column*10+1:
        print("not available")
    timer = Timer()
    regularscreen.updateTitle(timer, 5)
    regularscreen.checkWin()


def keyWasPressed(key):
    global xFocus
    global yFocus
    global gameOver
    xPrev = xFocus
    yPrev = yFocus
    checkClear = False
    if not gameOver:
        match(key):
            case "j":
                allTiles[xFocus][yFocus].leftClick()
                allTiles[xFocus][yFocus].color = allTiles[xFocus][yFocus].colors["cyan"]
                allTiles[xFocus][yFocus].foreGround = "black"
                allTiles[xFocus][yFocus].update()
                checkClear = True
            case "w":
                if xFocus != 0:
                    xFocus -= 1
            case "a":
                if yFocus != 0:
                    yFocus -= 1
            case "s":
                print(maxRows)
                print(xFocus)
                if xFocus != maxRows-1:
                    xFocus += 1
                else:
                    print("columns aborted")
            case "d":
                print(maxColumns)
                print(yFocus)
                if yFocus != maxColumns - 1:
                    yFocus += 1
                else:
                    print("rows aborted")
            case "l":
                allTiles[xFocus][yFocus].rightClick()
            case "space":
                allTiles[xFocus][yFocus].leftRightClick()
                checkClear = True
            case other:
                pass

        if not checkClear:
            allTiles[xFocus][yFocus].highlight()
            allTiles[xPrev][yPrev].highlight()


def destoryGame(event=None):
    regularscreen.destroy()


class InputRegularScreen(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.rows = Inputer(self, 0, 0, 0, 0, 20, 100, True)
        self.columns = Inputer(self, 1, 0, 0, 0, 20, 100, True)
        self.bombs = Inputer(self, 2, 0, 0, 0, 20, 100, True)
        self.go = Button1(self, 3, 3, 10, 10, "!begin!", leftClick=self.continueToGame)
        self.mainloop()

    def continueToGame(self, event=None):
        rows = self.rows.entry.get()
        columns = self.columns.entry.get()
        bombs = self.bombs.entry.get()
        print(rows)
        print(columns)
        print(bombs)

        if rows.isnumeric() and columns.isnumeric() and bombs.isnumeric():
            rows = int(rows)
            columns = int(columns)
            bombs = int(bombs)
            if rows * columns * 0.1 <= bombs:
                startRegular(rows, columns, bombs)


class RegularScreen(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.bind("<Key>", self.keyPressed)
        self.bind("space", self.spacePressed)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.windowCloseEvent)

    def initialize(self, row, column, event=None):
        for i in range(row):
            mini = []
            for i1 in range(column):
                light = True
                if (i % 2 == 0 and i1 % 2 == 0) or (i % 2 == 1 and i1 % 2 == 1):
                    light = False
                if [i, i1] in bombsList:
                    newTile = Tile(self, i, i1, 9, 4, text="9", lightTile=light, bomb=True)
                    mini.append(newTile)
                else:
                    newTile = Tile(self, i, i1, 9, 4, text=str(bombsNearby[i][i1]), lightTile=light,)
                    mini.append(newTile)
            allTiles.append(mini)

    def keyPressed(self, event):
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

        if allTiles[bombsList[0][0]][bombsList[0][1]].color == "brown":
            check = False

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
