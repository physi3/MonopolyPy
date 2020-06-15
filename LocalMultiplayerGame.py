import classes

class Game:
    def __init__(self, playerCount,boardFilePath="./boards/UK.board"):
        self.players = [classes.Player() for _ in range(playerCount)]
        self.board = classes.Board(boardFilePath)
    def createOptions(self,player):
        space = player.getCurrentSpace(self.board)
        optionMessages = []
        options = []
        if space.spaceType == "property":
            if space.owner == None and player.balance >= space.price:
                optionMessages.append(f"Buy {space.name} for {space.price}M")
                options.append("Buy")

        optionMessages.append("Display balance")
        options.append("Disp_Balance")

        optionMessages.append("Display properties")
        options.append("Disp_properties")

        optionMessages.append("End turn")
        options.append("End")
        return [optionMessages,options]

    def turn(self,player):
        playerIndex = self.players.index(player)
        input(f"Player {playerIndex+1} ...\nPress enter to roll the dice.")
        player.turn(self.board)
        space = player.getCurrentSpace(self.board)
        print(f"You rolled a {player.diceRoll} and landed on {space.name}")

        if space.spaceType == "tax":
            player.balance -= space.tax
            print(f"Charged for {space.tax} in tax.")

        if space.spaceType == "property":
            if space.rentDue(player):
                rent = space.calcRent(player)
                space.owner.balance+=rent
                player.balance-=rent
                print(f"{rent}M payed to player {self.players.index(space.owner)+1}.")

        while True:
            options = self.createOptions(player)
            for i in options[0]:
                print(i+f" [{options[0].index(i)+1}]")
            chosenOpt = options[1][int(input("Please choose an option [>> "))-1]
            if chosenOpt == "Buy":
                reply = player.purchaseProperty(player.getCurrentSpace(self.board))
                print(reply)
            if chosenOpt == "End":
                break
            if chosenOpt == "Disp_Balance":
                print(f"Your balance is currently {player.balance}M")
            if chosenOpt == "Disp_properties":
                print("You currently own:")
                for i in player.properties:
                    print(i.name)

            # if on go to jail, go to jail
            # (give option to trade)
            # give option to mortgage
            # give option to quit

    def start(self):
        while True:
            for i in self.players:
                self.turn(i)
