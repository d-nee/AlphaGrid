from Visualizer import SaveToFileVisualizer
import Arena
from MCTS import MCTS
from nodegrid.GridGame import GridGame
from nodegrid.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

p2_is_not_nn = True


g = GridGame(5)

# all players
# rp = RandomPlayer(g).play

def humanplay(b):
    print(g.getValidMoves(b, 1))
    s = input("move: ").split(" ")
    action = 5*(5*int(s[0]) + int(s[1])) + int(s[2])
    return action

def randomplay(b):
    a = np.random.randint(g.getActionSize())
    valids = g.getValidMoves(b, 1)
    while valids[a] != 1:
        a = np.random.randint(g.getActionSize())
    return a

# nnet players
n1 = NNet(g)
n1.load_checkpoint('models_2s_4d','best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

with open("pitlog.txt", "w") as r:
    print("cleared log")

if p2_is_not_nn:
    # player2 = humanplay
    player2 = randomplay
else:
    n2 = NNet(g)
    n2.load_checkpoint('models_2s_4d','best.pth.tar')
    args2 = dotdict({'numMCTSSims': 100, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=GridGame.display)

print(arena.playGames(40, verbose=False, visualizer=SaveToFileVisualizer, viz_args={'path': 'gameviz'}))
