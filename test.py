import numpy as np
import torch

# A = np.random.rand(2,2,2)
# print(A)
# A[1,:,:] *= -1
# print(A)
# exit(1)

# A = np.arange(3*3*4)

# A = np.reshape(A, (3, 3, 4))
# print(A)
# exit(1)

# A = np.arange(36)
# A = np.reshape(A, (3,3,4))
# print(A)
# print(np.ravel(np.roll(np.rot90(A, 2, (0,1)), 2, 2)))

# A = np.arange(18)
# A = np.reshape(A, (2, 3, 3))
# print(A)
# print(np.flip(A, 2))

# A = np.arange(16)
# A = np.reshape(A, (2,2,4))
# print(A)
# np.rot90(A, 0, (0, 1))
# print(A)


# exit(1)

class Board():

    def __init__(self, n):
        "Set up initial board configuration."
        INIT_PLAYER_UNITS = 15
        INIT_NEUTRAL = 10
        self.MAX_UNITS = 50

        self.n = n
        # Create the empty board array.
        self.squares = []
        self.squares.append([])
        self.squares.append([])
        for i in range(self.n):
            self.squares[0].append([])
            self.squares[1].append([])
            for j in range(self.n):
                self.squares[0][i].append(INIT_NEUTRAL)
                self.squares[1][i].append(0)

        # Set up the initial 2 pieces.
        self.squares[0][0][0] = INIT_PLAYER_UNITS
        self.squares[0][self.n - 1][self.n - 1] = INIT_PLAYER_UNITS
        self.squares[1][0][0] = 1
        self.squares[1][self.n - 1][self.n - 1] = -1


boards = []

for i in range(2):
    boards.append(Board(3).squares)

boards = torch.FloatTensor(np.array(boards).astype(np.float64))

print(boards)