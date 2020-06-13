class Board:
    def __init__(self):
        self.size = 0
        self.spaces = []
        self.players = []


class Space:
    name = ''
    position = 0


class Property(Space):
    def __init__(self):
        self.colour = ''


class Special(Space):
    pass


class Player:
    def __init__(self):
        self.name = ''
        self.position = 0
        self.inJail = False

    def move(self, board, displacement):
        self.position += displacement
        if self.position < 0:
            self.position += board.size
        if self.position >= board.size:
            self.position -= board.size
    
    def moveDirectly(self, position):
        self.position = position