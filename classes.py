from csv import reader as csvreader
from random import shuffle, randint
from io import StringIO

class Board:
    def __init__(self, filepath="./boards/UK.board"):
        # Loads spaces from board CSV.
        self.spaces = []
        self.groups = {}
        spaces = []


        with open(filepath, 'r') as boardfile:
            splitBoard = boardfile.read().split('&')
            spacesCSV = StringIO(splitBoard[0])
            chances = splitBoard[1].split('\n')[:-1]
            chests = splitBoard[2].split('\n')[:-1]

        reader = csvreader(spacesCSV)
        header = [*map(str.lower, next(reader))]

        # Expected values: name, type, set.
        values = ("name", "type", "set", "price", "rent", "buildingprice")
        order = [header.index(s) for s in values]
        for row in reader:
            #print(f"DEBUG: {row=}")
            # Keyword access to data.
            row = {value: row[i] for value, i in zip(values, order)}
            t = row["type"].lower()

            # If space is property then create group if it doesn't exist for space's set.
            space = None

            if t in ("site", "station", "utility"):
                # Space is a property.
                # Check if group exists for space's set.
                if row["set"] not in self.groups:
                    # Create the group.
                    #print(f"DEBUG: creating group {row['set']}")
                    self.groups[row["set"]] = Group(row["set"])
                
                # Load space data into specific Property subclass.

                if t == "site":
                    space = Site(row["name"], self.groups[row["set"]], row["price"], [int(x) for x in row["rent"].split('/')], buildingPrice = row["buildingprice"])
                elif t == "station":
                    space = Station(row["name"], self.groups[row["set"]], row["price"], [int(x) for x in row["rent"].split('/')])
                elif t == "utility":
                    space = Utility(row["name"], self.groups[row["set"]], row["price"], [int(x) for x in row["rent"].split('/')])

                # Put the space into the group.
                #print('appending', space, 'to', row["set"])
                self.groups[row["set"]].sites.append(space)
                #print(self.groups[row["set"]].name)
                

            elif t == "special":
                space = Special(row["name"])
            elif t == "cardspace":
                space = CardSpace(row["name"], row["set"])
            else:
                raise Exception(f"'{t}' is an invalid type! ({filepath})")
            


            # Add the space to the board.
            spaces.append(space)


        self.spaces = spaces
        self.size = len(self.spaces)

        # Spaces have been loaded!

        self.chances = []
        for i in chances:
            self.chances.append(Card(i.split(',')[0],i.split(',')[1]))
        shuffle(self.chances)

        self.chests = []
        for i in chests:
            self.chests.append(Card(i.split(',')[0],i.split(',')[1]))
        shuffle(self.chests)

    def drawChance(self, player):
        self.chances[0].actFunction(player)
        card = self.chances[0]
        self.chances.append(self.chances.pop(0))
        return card

    def drawChest(self, player):
        self.chests[0].actFunction(player)
        card = self.chests[0]
        self.chests.append(self.chests.pop(0))
        return card


class Card:
    def __init__(self, message, function):
        self.message = message
        self.function = function
    def __repr__(self):
        return self.message + ' ' + self.function
    def actFunction(self, player):
        if '|' in self.function:
            if self.function.split('|')[0] == "Money":
                player.money+=int(self.function.split('|')[1])
            elif self.function.split('|')[0] == "Move":
                player.move(int(self.function.split('|')[1]))
            elif self.function.split('|')[0] == "Directly":
                player.moveDirectly(int(self.function.split('|')[1]),True)
            elif self.function.split('|')[0] == "EachPlayer":
                # Get money from each player.
                pass
        else:
            if self.function == "Jail":
                # Go to jail
                pass
            elif self.function == "JailFree":
                # Out of jail
                pass

class Space:
    spaceType = None
    name = ''

    def __repr__(self):
        return f"<Space {self.spaceType=} {self.name=}>"


class Property(Space):
    spaceType = "property"
    propertyType = None

    def __init__(self, name, group, price, rent):
        self.name = name
        self.group = group
        self.owner = None
        self.price = int(price)
        self.rents = []

    def calcRent(self, client):
        return self.price


class Site(Property):
    propertyType = 'site'

    def __init__(self, *args, buildingPrice):
        super().__init__(*args)
        self.houses = 0
        self.buildingPrice = buildingPrice
        

    def calcRent(self, client):
        pass


class Utility(Property):
    propertyType = 'utility'
    def calcRent(self, client):
        pass


class Station(Property):
    propertyType = 'station'
    


class CardSpace(Space):
    def __init__(self, name, cardType):
        self.name = name
        self.cardType = cardType
        self.spaceType = "card_space"


class Special(Space):
    def __init__(self, name):
        self.name = name


class Group:
    def __init__(self, name, sites=[]):
        self.name = name
        self.sites = sites # List of Site objects

    def __iadd__(self, other):
        if issubclass(type(other), Property):
            self.sites.append(other)
            return self
        else:
            raise TypeError("Can't add non-property objects.")

    def __repr__(self):
        return f"<Group {len(self.sites)}>"



class Player:
    def __init__(self):
        self.position = 0
        self.inJail = False
        self.doubleCounter = 0
        self.balance = 1500
        self.properties = set()
        self.diceRoll = 0

    def checkForColourSet(self):
        pass
        
    def getCurrentSpace(self, board):
        return board.spaces[self.position]

    def addProperty(self, prop):
        # Make player the owner of given property.
        prop.owner = self
        self.properties.add(prop)
        return prop

    def removeProperty(self, prop):
        # Remove a property from player's ownership.
        prop.owner = None
        self.properties.discard(prop)
        return prop

    def buyProperty(self, prop):
        # Check if space is owned.
        if prop.owner:
            return False
        # Check that player has enough money.
        if self.balance < prop.price:
            return False
        # Make player the owner of property.
        return self.addProperty(prop)

    def passGo(self):
        self.balance += 200

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
        self.diceRoll = self.rollDice()
        self.move(board, self.diceRoll)
