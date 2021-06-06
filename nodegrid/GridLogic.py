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
        self.squares.append([])
        for i in range(self.n):
            self.squares[0].append([])
            self.squares[1].append([])
            self.squares[2].append([])
            for j in range(self.n):
                self.squares[0][i].append(INIT_NEUTRAL)
                self.squares[1][i].append(0)
                self.squares[2][i].append(1)

        # Set up the initial 2 pieces.
        self.squares[0][0][0] = INIT_PLAYER_UNITS
        self.squares[0][self.n - 1][self.n - 1] = INIT_PLAYER_UNITS
        self.squares[1][0][0] = 1
        self.squares[1][self.n - 1][self.n - 1] = -1

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.squares[index]

    @staticmethod
    def get_tg_move(r, c, direction):
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
        return r_tg, c_tg
    
    def move_is_useful(self, r, c, d):
        r_tg, c_tg = Board.get_tg_move(r, c, d)
        if self[1][r][c] != self[1][r_tg][c_tg]:
            return True
        return self[0][r_tg][c_tg] != 50

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        ul = self[1][-1][-1] == color
        dr = self[1][0][0] == color
        moves = []
        for i in range(self.n):
            for j in range(self.n):
                if self[1][i][j] == color:
                    base = 4 * (self.n * i + j)
                    if i > 0 and ul and self.move_is_useful(i, j, 0):
                        moves.append(base)
                    if j > 0 and ul and self.move_is_useful(i, j, 1):
                        moves.append(base + 1)
                    if i < self.n - 1 and dr and self.move_is_useful(i, j, 2):
                        moves.append(base + 2)
                    if j < self.n - 1 and dr and self.move_is_useful(i, j, 3):
                        moves.append(base + 3)
        return moves


    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=p1,-1=p2)
        """
        r, c, direction = move

        r_tg, c_tg = Board.get_tg_move(r, c, direction)
        
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
                if self[1][i][j] != 0 and self[0][i][j] < self.MAX_UNITS:
                    self[0][i][j] += 1
                self[2][i][j] += 1

    def timeout_winner(self, color):
        sum_p1, sum_p2 = 0, 0
        p1_s, p2_s = 0, 0
        for i in range(self.n):
            for j in range(self.n):
                if self[1][i][j] == color:
                    sum_p1 += self[0][i][j]
                    p1_s += 1
                elif self[1][i][j] == -color:
                    sum_p2 += self[0][i][j]
                    p2_s += 1
        return 1 if sum_p1 >= sum_p2 else -1
                


        

                
