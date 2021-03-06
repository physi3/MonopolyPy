import classes

board = classes.Board()
player = classes.Player()

for i in range(100):
    player.turn(board)
    space = player.getCurrentSpace(board)
    print(space.spaceType)
    print(space.name)
    if space.spaceType == "card_space":
        if space.cardType == "Chance":
            print("take a chance")
            card = board.drawChance(player)
            print(card.message)
        elif space.cardType == "Chest":
            print("take a chest")
            card = board.drawChest(player)
            print(card.message)

    input()
