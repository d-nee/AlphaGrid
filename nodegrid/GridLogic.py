'''
Board class.
Board data:
  1=p1, -1 = p2, 0 = neutral
Squares are stored and manipulated as (z,x,y) tuples, with an extra channel z
for ownership.
z is owner, x is the column, y is the row.
'''
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

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.squares[index]

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = []
        for i in range(self.n):
            for j in range(self.n):
                if self[1][i][j] == color:
                    base = 4 * (self.n * i + j)
                    if i > 0:
                        moves.append(base)
                    if j > 0:
                        moves.append(base + 1)
                    if i < self.n - 1:
                        moves.append(base + 2)
                    if j < self.n - 1:
                        moves.append(base + 3)
        return moves

    def is_eliminated(self, color):
        if color == 1:
            return self[1][0][0] != color
        else:
            return self[1][self.n - 1][self.n - 1] != color

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=p1,-1=p2)
        """
        r, c, direction = move
        if direction == 0:
            r_tg = r - 1
            c_tg = c
        elif direction == 1:
            r_tg = r
            c_tg = c - 1
        elif direction == 2:
            r_tg = r + 1
            c_tg = c
        elif direction == 3:
            r_tg = r
            c_tg = c + 1
        
        if self[1][r_tg][c_tg] == color:
            total = self[0][r][c] + self[0][r_tg][c_tg] 
            if total <= self.MAX_UNITS:
                self[0][r_tg][c_tg] = total
                self[0][r][c] = 0
            else:
                overflow = total - self.MAX_UNITS
                self[0][r_tg][c_tg] = self.MAX_UNITS
                self[0][r][c] = overflow
        else:
            diff = self[0][r_tg][c_tg] - self[0][r][c]
            self[0][r][c] = 0
            if diff < 0:
                self[0][r_tg][c_tg] = -1 * diff
                self[1][r_tg][c_tg] = color
            else:
                self[0][r_tg][c_tg] = diff
        
        #Economy

        for i in range(self.n):
            for j in range(self.n):
                if self[1][i][j] != 0 and self[0][i][j] <= self.MAX_UNITS:
                    self[0][i][j] += 1
        

                
