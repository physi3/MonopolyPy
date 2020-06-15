import classes

class Game:
    def __init__(self, playerCount, boardFilePath="./boards/UK.board"):
        self.players = [classes.Player() for _ in range(playerCount)]
        self.board = classes.Board(boardFilePath)

    def createOptions(self, player):
        space = player.getCurrentSpace(self.board)
        optionMessages = []
        options = []
        if space.spaceType == "property":
            if space.owner == None and player.balance >= space.price:
                optionMessages.append(f"Buy {space.name} for {space.price}M")
                options.append("Buy")

        if len(player.getFullGroups()) > 0:
            optionMessages.append("Add houses or hotels to your properties")
            options.append("Add_Building")
        optionMessages.append("Display balance")
        options.append("Disp_Balance")

        optionMessages.append("Display properties")
        options.append("Disp_properties")

        optionMessages.append("End turn")
        options.append("End")
        return [optionMessages,options]

    def turn(self,player):
        playerIndex = self.players.index(player)
        input(f"\nPlayer {playerIndex+1} ...\nPress enter to roll the dice.")
        player.turn(self.board)
        space = player.getCurrentSpace(self.board)
        if space.spaceType == "property":
            print("You rolled a {} and landed on {}, {}\n".format(
                player.diceRoll,
                space.name,
                space.group.name
            ))
        else:
            print("You rolled a {} and landed on {}\n".format(
                player.diceRoll,
                space.name
            ))

        if space.spaceType == "tax":
            player.balance -= space.tax
            print(f"Charged for {space.tax} in tax.\n")

        if space.spaceType == "card_space":
            if space.cardType == "Chance":
                print()
                print(self.board.drawChance(player).message)
            if space.cardType == "Chest":
                print()
                print(self.board.drawChest(player).message)

        if space.spaceType == "property":
            if space.rentDue(player):
                rent = space.calcRent(player)
                space.owner.balance+=rent
                player.balance-=rent
                print("{}M payed to player {}.\n".format(
                    rent,
                    self.players.index(space.owner)+1
                ))

        while True:
            options = self.createOptions(player)
            for i in options[0]:
                print(i+f" [{options[0].index(i)+1}]")
            chosenOpt = options[1][int(input("Please choose an option [>> "))-1]
            if chosenOpt == "Buy":
                reply = player.purchaseProperty(
                    player.getCurrentSpace(self.board)
                )
                print()
                print(reply)
            if chosenOpt == "End":
                break
            if chosenOpt == "Disp_Balance":
                print(f"\nYour balance is currently {player.balance}M")
            if chosenOpt == "Disp_properties":
                print("\nYou currently own:")
                for i in player.props:
                    print(i.name)
                print()

            # if on go to jail, go to jail
            # (give option to trade)
            # give option to mortgage
            # give option to quit

    def start(self):
        while True:
            for i in self.players:
                self.turn(i)

g = Game(2)
g.start()
