import numpy as np


class Board:
    SIZE = [6, 7]
    EMPTY_CELL = 0
    PLAYER_SYMBOLS = [1, 2]
    STEP = 4

    def __init__(self):
        self._matrix = np.zeros(self.SIZE, dtype=int)
        self.discs_on_board = 0
        self._win_set = []
        self.original_placement = []
        self._first_row_seq_coor = []
        self._first_l_diagonal_coor = []
        self._first_r_diagonal_coor = []

    def __repr__(self):
        return repr(self._matrix)

    def find_closest_from_left(self, x, y, player):
        if y == 0 or self._matrix[x][y - 1] != player:
            self._first_row_seq_coor = x, y
            return x, y
        else:
            return self.find_closest_from_left(x, y - 1, player)

    def find_diagonal_from_top_right(self, x, y, player):
        if y == 6 or x == 0 or self._matrix[x - 1][y + 1] != player:
            self._first_l_diagonal_coor = x, y
            return x, y
        else:
            return self.find_diagonal_from_top_right(x - 1, y + 1, player)

    def find_diagonal_from_top_left(self, x, y, player):
        if y == 0 or x == 0 or self._matrix[x - 1][y - 1] != player:
            self._first_r_diagonal_coor = x, y
            return x, y
        else:
            return self.find_diagonal_from_top_left(x - 1, y - 1, player)

    def _foursetes_maker(self, coordinate, player):
        x, y = self.find_closest_from_left(coordinate[0],
                                           coordinate[1], player)
        right = ('right', list(self._matrix[x][y:y + self.STEP]))

        down = ('down', [row[y] for row in self._matrix[x:x +
                                                          self.STEP]])
        ############################
        x, y = self.find_diagonal_from_top_left(coordinate[0],
                                                coordinate[1], player)
        d_bottom_right = ('r_diagonal', list(self._matrix[x:].diagonal(y)))

        #############################
        x, y = self.find_diagonal_from_top_right(coordinate[0],

                                                 coordinate[1], player)
        d_bottom_left = ('l_diagonal', list(np.fliplr(self._matrix[x:])
                                            .diagonal
                                            (len(self._matrix[1]) - 1 - y)))

        return right, down, d_bottom_left, d_bottom_right

    def __update_win_set(self, direction):
        result = []
        for i in range(4):
            if direction == 'right':
                x, y = self._first_row_seq_coor
                result.append((x, y + i))
            if direction == 'down':
                x, y = self.original_placement
                result.append((x + i, y))
            if direction == 'r_diagonal':
                x, y = self._first_r_diagonal_coor
                result.append((x + i, y + i))
            if direction == 'l_diagonal':
                x, y = self._first_l_diagonal_coor
                result.append((x + i, y - i))
        self._win_set = result

    def find_winner(self, placing, goal):
        self.original_placement = placing
        if self.discs_on_board == (Board.SIZE[0] * Board.SIZE[1]):
            return 0
        else:
            player = self._matrix[placing[0], placing[1]]
            [*possible_foursets] = self._foursetes_maker(placing, player)
            for direction in possible_foursets:
                if len(direction[1]) == goal:
                    if list(direction[1]).count(player) == goal:
                        self.__update_win_set(direction[0])
                        return player
            else:
                return

    def is_legal_placement(self, column):
        requested_column = self._matrix.T[column]  # throws index error if
        # out of range
        if self.EMPTY_CELL not in requested_column:  # column is full
            raise IndexError

    def get_lowest_cell(self, column):
        column_from_bottom = self._matrix.T[column]
        for ridx, row in reversed(list(enumerate(column_from_bottom))):
            if row == self.EMPTY_CELL:
                return ridx, column

    def place_object(self, column, player_symbol):
        self.discs_on_board += 1
        ridx, row = self.get_lowest_cell(column)
        self._matrix[ridx][column] = player_symbol
        return ridx, column

    def get_unoccupied_cells_in_col(self, column):
        lst = []
        current_col = self._matrix.T[column]
        for ridx, row in enumerate(current_col):
            if row == self.EMPTY_CELL:
                lst.append((ridx, column))
        return lst

    def get_cell(self, row, col):
        return self._matrix[row][col]

    def get_win_set(self):
        return self._win_set
