from random import choice

NUM_ROWS = 6
NUM_COLS = 7


class AI:

    def __init__(self, game, player):
        self.game = game
        self.avatar = player

    def find_legal_move(self):
        self.__is_it_my_turn()

        possible_moves = []
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if not self.game.get_player_at(row, col):
                    possible_moves.append(col)

        if len(possible_moves) == 0:
            raise TypeError("No possible AI moves.")
        else:
            return choice(possible_moves)

    def __repr__(self):
        return "AI"

    def __is_it_my_turn(self):
        if self.game.get_current_player() != self.avatar:
            raise NameError("Wrong player.")

    def get_last_found_move(self):
        pass
