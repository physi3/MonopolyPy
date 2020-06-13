import classes

board = classes.Board()
player = classes.Player()

for i in range(100):
    player.turn(board)
    print(board.spaces[player.position])
    input()
