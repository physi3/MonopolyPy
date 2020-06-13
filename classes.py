from csv import reader as csvreader
from random import randint

class Board:
    def __init__(self, filepath="./boards/UK.board"):
        # Loads spaces from board CSV.
        spaces = []

        with open(filepath, 'r') as boardfile:
            reader = csvreader(boardfile)
            header = [*map(str.lower, next(reader))]

            # Expected values: name, type, set.
            values = ("name", "type", "set")
            order = [header.index(s) for s in values]
            for row in reader:
                # Keyword access to data.
                row = {value: row[i] for value, i in zip(values, order)}
                # Check the type of space.
                space = None
                t = row["type"].lower()
                if t == "property":
                    space = Property(row["name"], row["set"])
                elif t == "special":
                    space = Special(row["name"])
                else:
                    raise Exception(f"'{t}' is an invalid type! ({filepath})")

                # Add the space to the board.
                spaces.append(space)
            self.spaces = spaces


class Space:
    name = ''


class Property(Space):
    def __init__(self, name, colour):
        self.name = name
        self.set = colour

    def __repr__(self):
        return f"<Property '{self.name}'>"


class Special(Space):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Special '{self.name}'>"


class Player:
    def __init__(self):
        self.name = ''
        self.position = 0
        self.inJail = False
        self.doubleCounter = 0

    def move(self, board, displacement):
        self.position += displacement
        if self.position < 0:
            self.position += board.size
        if self.position >= board.size:
            self.position -= board.size

    def moveDirectly(self, position):
        self.position = position

    def rollDice():
        dice1 = randint(1,6)
        dice2 = randint(1,6)
        if dice1 == dice2:
            self.doubleCounter+=1
        return dice1+dice2

    def turn(self, board):
