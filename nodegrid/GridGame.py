from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .GridLogic import Board
import numpy as np

class GridGame(Game):
    def __init__(self, n):
        assert(n >= 2)
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.squares)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n*4

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n*self.n*4:
            return (board, -player)
        b = Board(self.n)
        b.squares = np.copy(board)
        move = np.unravel_index(action, (self.n, self.n, 4))
        b.execute_move(move, player)
        return (b.squares, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.squares = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        for x in legalMoves:
            valids[x] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        if board[1][0][0] == player and board[1][-1][-1] == player:
            return 1
        if board[1][0][0] == -player and board[1][-1][-1] == -player:
            return -1
        return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        canonical = np.copy(board)
        canonical[1,:,:] *= player
        return canonical

    def getSymmetries(self, board, pi):
        # mirror, rotational?? really hard rotations
        # hard because the rotation of actions is tough
        assert(len(pi) == self.n*self.n*4)
        pi_board = np.reshape(pi, (self.n, self.n, 4))
        l = []
        
        for i in range(0, 4):
            for j in [True, False]:
                newB = np.rot90(board, i, (1, 2))
                newPi = np.roll(np.rot90(pi_board, i, (0, 1)), i, 2)
                if j:
                    newB = np.flip(newB, 2)
                    newPi = np.flip(newPi, 1)
                    temp = np.copy(newPi[:,:,1])
                    newPi[:,:,1] = newPi[:,:,3]
                    newPi[:,:,3] = temp
                l += [(newB, list(newPi.ravel()))]
        return l


    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        b = board
        board_s = "".join(str((b[0][r][c], b[1][r][c])) \
                        for r in range(self.n) for c in range(self.n))
        return board_s

    @staticmethod
    def display(board):
        n = board[0].shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end="       ")
        print("")
        print("---------------------------------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                print((board[0][y][x] , board[1][y][x]), end=" ")
            print("|")

        print("---------------------------------------------")
