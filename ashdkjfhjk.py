
def clearAround(row, column, event=None):
    """
    Clears the tiles around this tile.

    Args:
        event (Tk)(optional): Tk event
    """

    # lists co-ordinates of tiles next to this tile
    locations = [
        [row + 1, column - 1],
        [row, column - 1],
        [row - 1, column - 1],
        [row - 1, column],
        [row + 1, column],
        [row - 1, column + 1],
        [row, column + 1],
        [row + 1, column + 1]
    ]

    # # removes non-existant tiles
    # for i in locations:
    #     if i[0] < 0 or i[0] > maxRows-1 or i[1] < 0 or i[1] > maxColumns-1:
    #         locations[locations.index(i)] = "_"

    locations = []

    # checks if this tile has no bombs around it and clears tiles near it
    for i in locations:
        if not i == "_" and not allTiles[i[0]][i[1]].isReveal and not allTiles[i[0]][i[1]].isAreaCleared and not allTiles[i[0]][i[1]].isBomb:
            try:
                allTiles[i[0]][i[1]].clearAround()
                allTiles[i[0]][i[1]].leftClick()
            except (RecursionError):
                print("recursion")
                print(i)
    isAreaCleared = True