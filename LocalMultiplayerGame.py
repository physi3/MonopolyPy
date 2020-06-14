import classes

def Game:
    def __init__(self, playerCount,boardFilePath="./boards/UK.board"):
        self.players = [classes.Player() for _ in range(playerCount)]
        self.board = classes.Board(boardFilePath)
