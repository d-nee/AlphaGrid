from nodegrid.GridGame import GridGame

game = GridGame(4)

b = game.getInitBoard()

player = 1

while game.getGameEnded(b, player) == 0:
    game.display(b)
    print(game.getValidMoves(b, player))
    s = input("move: ").split(" ")
    action = 4*(4*int(s[0]) + int(s[1])) + int(s[2])
    b, player = game.getNextState(b, player, action)

