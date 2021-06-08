import matplotlib.pyplot as plt
import numpy as np
import colorsys
import imageio
import os


class GridVisualizer:

    def addBoard(self, board):
        raise NotImplementedError("Not implemented: addBoard")

    def save(self):
        raise NotImplementedError("Not implemented: save")

# store hue, value pairs of desired max. colors 
P1_COLOR = (0., 0.75, 1.)
P2_COLOR = (0.6, 0.75, 1.)
NEUTRAL_COLOR = (0., 0., 1.)

MAX_TROOP = 50

class SaveToFileVisualizer(GridVisualizer):

    def __init__(self, path):
        self.path = path
        existing_games = os.listdir(self.path)

        if len(existing_games) > 0:
            number = len(existing_games)
            self.savedir = f"{self.path}/game_{number}"
        else:
            self.savedir = f"{self.path}/game_0"

        os.mkdir(self.savedir)

        

    def addBoard(self, board):
        plt.cla()
        plt.clf()
        ax = plt.gca()

        newBoard = np.ones((board.shape[1], board.shape[2], 3))
        for i in range(board.shape[1]):
            for j in range(board.shape[2]):
                if board[1][i][j] == 1:
                    newBoard[i][j] = np.array(colorsys.hsv_to_rgb(P1_COLOR[0], np.sqrt(P1_COLOR[1] * board[0][i][j] / MAX_TROOP), P1_COLOR[2]))
                elif board[1][i][j] == -1:
                    newBoard[i][j] = np.array(colorsys.hsv_to_rgb(P2_COLOR[0], np.sqrt(P2_COLOR[1] * board[0][i][j] / MAX_TROOP), P2_COLOR[2]))
                elif board[1][i][j] == 0:
                    # for grayscale, vary value instead of saturation
                    newBoard[i][j] = np.array(colorsys.hsv_to_rgb(NEUTRAL_COLOR[0], NEUTRAL_COLOR[1], 1-NEUTRAL_COLOR[2]* board[0][i][j] / MAX_TROOP))

        # print(board)

        ax.imshow(newBoard)

        for i in range(board.shape[1]):
            for j in range(board.shape[2]):
                ax.text(j,i,str(board[0][i][j]),ha='center',va='center')

        plt.savefig(f"{self.savedir}/{board[2][0][0]}.png")

    def save(self):
        filenames = os.listdir(self.savedir)
        filenames.sort(key=lambda t: int(t.split('.')[0]))
        with imageio.get_writer(f"{self.savedir}/game.gif", mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(os.getcwd() + '/' + self.savedir + '/' + filename)
                writer.append_data(image)
        


