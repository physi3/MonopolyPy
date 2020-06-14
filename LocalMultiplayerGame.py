import classes

class Game:
    def __init__(self, playerCount,boardFilePath="./boards/UK.board"):
        self.players = [classes.Player() for _ in range(playerCount)]
        self.board = classes.Board(boardFilePath)
    def turn(self,playerIndex):
        # rollDice
        # display new space
        # give options
        # if money due, pay Rent
        # give option to buy
        # pay tax if on tax
        # if on go to jail, go to jail
        # (give option to trade)
        # give option to mortgage
        # give option to quit
        pass
