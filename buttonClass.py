from tkinter import *
import random

# ========================================================================================================================================
# for remembering home scren button values
# ========================================================================================================================================
class Button1():
    def __init__(self, root2, row, column, len, wid, text=" ", color="white") -> None:
        
        print(root2)
        # row, column, text, length, width, background color, root, and button (object)
        self.r = row
        self.c = column
        self.t = text
        self.l = len
        self.w = wid
        self.col = color

        self.root2 = root2

        self.B = Button(self.root2, text=self.t, padx=self.l, pady=self.w, bg=self.col)
        print(3)
        self.B.grid(row=self.c, column=self.r)

    def update(self):
        self.B.grid_remove()
        self.B = Button(self.root2, text=self.t, padx=self.l, pady=self.w, bg=self.col)
        self.B.grid(row=self.c, column=self.r)

# ========================================================================================================================================
# the tile that is used in game
# ========================================================================================================================================
class Tile(Button1):

    # max row and column numbers
    mr = 0
    mc = 0

    # where the bombs are
    bomblist = []
    
    # no flag mode boolean
    flagMode = False

    # doubles game mode boolean
    double = False

    # color options
    colors = {
        "dark green": "#1b5e02",
        "light green": "#2d8a0a",
        "dark green highlight": "#025e49",
        "light green highlight": "#0a8a75",
        "light brown": "#afb576",
        "dark brown": "#838a5a",
    }

    def __init__(self, root, row, column, len, wid, maxrow, maxcol, bomb=False, text=" ") -> None:
        print(root)

        super().__init__(root, row, column, len, wid)
        
        # bomb boolean
        self.b = bomb

        # the max amount of rows and columns
        self.mr = maxrow
        self.mc = maxcol

        # revealed tile boolean
        self.rev = False

        # flaged boolean
        self.flaged = False

        # area cleard boolean
        self.ac = False

        # hovering over tile boolean
        self.hover = False

        # # set doubles mode boolean
        # self.double = RoD

        # # set "no Flag" mode boolean
        # self.double = fall

        # selects colors based on tile position
        if self.r % 2 == 0 and self.c % 2 == 0 or self.r % 2 == 1 and self.c % 2 == 1:
            self.col = self.colors["dark green"]
        else:
            self.col = self.colors["light green"]
        
        
        # self.B.bind("<Enter>", self.sethoverintoT)
        # self.B.bind("<Leave>", self.sethoverintoF)

        # update button to change color
        self.update()
        self.B.bind("<Button-1>", self.leftClick)
        self.B.bind("a", self.leftClick)
        self.B.bind("<Button-3>", self.rightClick)
        self.B.bind("s", self.rightClick)

    # ========================================================================================================================================
    # user left clicked tile
    def leftClick(self, event=None):

        print("you clicked on"+str(self.r)+" "+str(self.c))
        # if "no flag" mode is off and tile is not a bomb
        if self.flaged is False and self.b is False and self.rev is False:

            # change the color of tile before tile is updated
            if self.col == self.colors["light green"] or self.col == self.colors["light green highlight"]:
                self.col = self.colors["light brown"]
            
            if self.col == self.colors["dark green"] or self.col == self.colors["dark green highlight"]:
                self.col = self.colors["dark brown"]

            # find how many bombs are nearby
            locations = [
                [self.r + 1, self.c - 1],
                [self.r, self.c - 1],
                [self.r - 1, self.c - 1],
                [self.r - 1, self.c],
                [self.r + 1, self.c],
                [self.r - 1, self.c + 1],
                [self.r, self.c + 1],
                [self.r + 1, self.c + 1]
            ]

            # see if any coordinates are bombs
            bombs = 0
            for i in locations:
                if i in self.bomblist:
                    bombs += 1
            if bombs != 0:
                self.t = str(bombs)
                self.l -= 2
            
            self.update()

            # self.B.bind("<Button-1><Button-3>", self.cleararea)
            self.rev = True
        
        # if tile is a bomb
        if self.b is True:
            
            # if doubles mode is true
            if self.double is True:
                self.showbombs(2)
                print("user has click on a bomb")

            else:
                # self.showbombs()
                pass

        self.clearAround()
    
    # ========================================================================================================================================
    # user right clicked tile
    def rightClick(self, event=None):
        
        # if "no flag" Mode is on and tile is not revealed
        if self.flagMode is False  and self.rev is False:

            # if tile dosn't have a flag on it
            if self.flaged is False:
                self.t = "F"
                self.col="orange"
                self.l -= 2

                self.update()

                self.flaged = True

                self.B.bind("<Button-1>", self.leftClick)
                self.B.bind("a", self.leftClick)
                self.B.bind("<Button-3>", self.rightClick)
                self.B.bind("s", self.rightClick)
                # self.B.bind("<Enter>", self.sethoverintoT)
                # self.B.bind("<Leave>", self.sethoverintoF)
            
            elif self.flaged is True:
                self.flaged = False
                self.l += 2
                self.t = " "
                if self.r % 2 == 0 and self.c % 2 == 0 or self.r % 2 == 1 and self.c % 2 == 1:
                    self.col = self.colors["dark green"]
                else:
                    self.col = self.colors["light green"]
                self.update()
                self.B.bind("<Button-1>", self.leftClick)
                self.B.bind("a", self.leftClick)
                self.B.bind("<Button-3>", self.rightClick)
                self.B.bind("s", self.rightClick)
                # self.B.bind("<Enter>", self.sethoverintoT)
                # self.B.bind("<Leave>", self.sethoverintoF)

    def clearAround(self, event=None):
        if self.rev is True:
            locations = [
                [self.r + 1, self.c - 1],
                [self.r, self.c - 1],
                [self.r - 1, self.c - 1],
                [self.r - 1, self.c],
                [self.r + 1, self.c],
                [self.r - 1, self.c + 1],
                [self.r, self.c + 1],
                [self.r + 1, self.c + 1]
            ]

            c1 = 0

            for i in locations:
                for i1 in self.bomblist:
                    if i == i1:
                        if allTiles[i[0]][i[1]].b is True and allTiles[i[0]][i[1]].flaged is False:
                            c1 = 1
            if c1 == 0:
                for i in locations:
                    for i1 in allTiles:
                        for i2 in i1:
                            if i2.r == i[0] and i2.c == i[1] and i2.rev is False:
                                i2.leftClick()
            



root1 = Tk()
B = Button(root1, text=" ", padx=10, pady=10, bg="white")
B.grid(row=1, column = 1)
print(root1)

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

allTiles = []

for i in range(20):
    mini = []
    for i1 in range(20):
        if [i, i1] in allbombs:
            newButton = Tile(root1, i, i1, 16, 10, 10, 10, bomb=True)
            newButton.bomblist = allbombs
            mini.append(newButton)
        else:
            newButton = Tile(root1, i, i1, 16, 10, 10, 10)
            newButton.bomblist = allbombs
            mini.append(newButton)
    allTiles.append(mini)

allTiles[0][0].bomblist = allbombs
allTiles[0][0].mr = 10
allTiles[0][0].mc = 10

print(allbombs)

root1.mainloop()