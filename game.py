from . import board as bd


class Game:
    GOAL = 4
    ILLEGAL_MSG = "Illegal Move"
    ILLEGAL_LOCATION = 'Illegal location'
    GAME_OVER_MSG = "GAME OVER"
    NUM_PLAYERS = 2

    def __init__(self):
        self.__board = bd.Board()
        self.__current_placement = []
        self.__current_player = 1
        self.__winner = None

    def make_move(self, column):
        """
        if move is legal, place player's disk in requested cell
        (based on lowest unoccupied cell in given column)
        otherwise, raise index error exception
        """
        try:
            cur_player = self.get_current_player()
            self.__board.is_legal_placement(column)
            self.__current_placement = self.__board.place_object(column,
                                                                 cur_player)
            self.is_game_over()
        except ValueError:
            raise ValueError("Illegal move")  # game over
        except IndexError:
            raise IndexError("Illegal move")


    def __update_winner_status(self):
        self.__winner = self.__board.find_winner(self.__current_placement,
                                                 self.GOAL)

    def is_game_over(self):
        self.__update_winner_status()
        if self.__winner or self.__winner == 0:
            raise ValueError("we have a winner")

    def get_win_set(self):
        return self.__board.get_win_set()

    def get_winner(self):
        """
        return int (1 or 2) that represent the winner player.
        if tie, return 0. if game isn't over, return None
        """
        return self.__winner

    def get_player_at(self, row, col):
        """
        return int (1 or 2), based on who's disk is in given coordinates.
        if cell is empty, return None
        """
        try:
            return None if self.__board.get_cell(row,
                                             col) == self.__board.EMPTY_CELL \
                else self.__board.get_cell(row, col)
        except IndexError:
            raise IndexError(self.ILLEGAL_LOCATION, (row, col))

    def set_player(self):
        self.__current_player += 1

    def get_current_player(self):
        """
        returns int that represent current player (1 or 2)
        """
        player = self.__current_player % self.NUM_PLAYERS
        return player if player != 0 else self.NUM_PLAYERS

    def get_cur_placement(self):
        return self.__current_placement

    def get_unoccupied_cells(self, column):
        return self.__board.get_unoccupied_cells_in_col(column)
