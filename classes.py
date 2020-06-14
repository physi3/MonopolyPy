from csv import reader as csvreader
from random import shuffle, randint
from io import StringIO

class Board:
    def __init__(self, filepath="./boards/UK.board"):
        # Loads spaces from board CSV.
        spaces = []

        with open(filepath, 'r') as boardfile:
            splitBoard = boardfile.read().split('&')
            spacesCSV = StringIO(splitBoard[0])
            chances = splitBoard[1].split('\n')[:-1]
            community = splitBoard[2].split('\n')[:-1]

        reader = csvreader(spacesCSV)
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
        self.size = len(self.spaces)

        self.chances = []
        for i in chances:
            self.chances.append(Card(i.split(',')[0],i.split(',')[1]))
        shuffle(self.chances)

        self.community = []
        for i in community:
            self.community.append(Card(i.split(',')[0],i.split(',')[1]))
        shuffle(self.community)


class Card:
    def __init__(self, message, function):
        self.message = message
        self.function = function
    def __repr__(self):
        return self.message + ' ' + self.function
    def actFunction(self, player):
        if '|' in function:
            if function.split('|')[0] == "Money":
                player.money+=int(function.split('|')[1])
            elif function.split('|')[0] == "Move":
                player.move(int(function.split('|')[1]))
            elif function.split('|')[0] == "Directly":
                player.moveDirectly(int(function.split('|')[1]),True)
            elif function.split('|')[0] == "EachPlayer":
                #get money from each player
                pass
        else:
            if function == "Jail":
                #go to jail
                pass
            elif function == "JailFree":
                #getttoyu jail
                pass

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
        self.position = 0
        self.inJail = False
        self.doubleCounter = 0
        self.money = 0

    def passGo(self):
        self.money += 200

    def move(self, board, displacement):
        self.position += displacement
        if self.position < 0:
            self.position += board.size
        if self.position >= board.size:
            self.position -= board.size
            self.passGo()

    def moveDirectly(self, position, collectGo):
        if self.position > position and collectGo:
            self.passGo()
        self.position = position


    def rollDice(self):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        if dice1 == dice2:
            self.doubleCounter += 1
        return dice1 + dice2

    def turn(self, board):
        diceRoll = self.rollDice()
        self.move(board, diceRoll)
        print(diceRoll)
