import sys
import helper
from board import Board
from car import Car

LENGTH_IDX = 0
LOCATION_IDX = 1
ORIENTATION_IDX = 2
NAME_IDX = 0
COMMA_IDX = 1
COMMA = ','
MOVEKEY_IDX = 2
CAR_NAMES = 'YBOWGR'
MIN_CAR_LEN = 2
MAX_CAR_LEN = 4
VERTICAL = 0
HORIZONTAL = 1


class Game:
    """
    rush-hour game
    """
    MSG = {
        'welcome': 'Welcome to the best game ever!',
        'illegal input': 'Your input is invalid.\n',
        'request move': 'Please enter a car name (= color) to move, and the requested direction (e.g Y,d): ',
        'illegal names': 'Only one car can be moved at once. Cars {} where not moved.\n',
        'illegal separator': 'Illegal separator.\n',
        'illegal car name': 'Illegal car name. car {} was not moved.\n',
        'illegal direction': 'Illegal direction. car {} was not moved.\n',
        'illegal move': 'Illegal move. Car {} was not moved.\n',
        'end': 'Car {} is out, game is over! :)'
    }

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board
        self.__end = False

    def __single_turn(self):
        """
        The function runs one round of the game:
        get user's input, check if the input is valid and try moving car according to user's input.
        """
        user_input = input(self.MSG['request move'])

        # check if input is valid
        if self.__is_input_valid(user_input):
            name = user_input[NAME_IDX]
            movekey = user_input[MOVEKEY_IDX]

            # checks if car can be moved, and moves it if possible
            if not self.board.move_car(name, movekey):
                print(self.MSG['illegal move'].format(name))

    def __is_game_over(self):
        """
        if game is over, prints message and updates 'end' param to be True
        """
        target = self.board.target_location()

        # checks if the exit cell had been reached
        if self.board.cell_content(target):
            car_name = self.board.cell_content(target)

            # a car reached the target cell, game is over
            print(self.MSG['end'].format(car_name))
            self.__end = True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while not self.__end:
            print(self.board)

            # runs one iteration, and checks if game is over
            self.__single_turn()
            self.__is_game_over()

    def __is_input_valid(self, user_input):
        """
        :return: True upon success, False otherwise
        """
        # checks if name and direction where entered
        if len(user_input) != 3:
            print(Game.MSG['illegal input'])
            return False

        name = user_input[NAME_IDX]
        comma = user_input[COMMA_IDX]
        movekey = user_input[MOVEKEY_IDX]

        # check if comma is indeed comma
        if comma != COMMA:
            print(self.MSG['illegal separator'])
            return False

        # check if more then one name was requested
        if len(name) != 1:
            print(self.MSG['illegal names'].format(name))
            return False

        # check if movekey is legal
        if len(movekey) != 1:
            print(self.MSG['illegal direction'].format(name))
            return False

        # input is legal
        return True


def is_car_valid(car_name, length, orientation):
    """
    :return: True upon success, False otherwise
    """

    if car_name in CAR_NAMES:
        # legal names: 'YBOWGR'

        if MIN_CAR_LEN <= length <= MAX_CAR_LEN:
            # legal length: 2-4

                if orientation == VERTICAL or orientation == HORIZONTAL:
                    # legal orientation
                    # all car params are met, car is valid
                    return True

    # car is invalid
    return False


if __name__ == "__main__":
    # initializing board game
    board = Board()
    car_config = helper.load_json(sys.argv[1])
    car_dict = {}

    # adding cars to game from json file, if valid
    for car_name, car_values in car_config.items():
        length = car_values[LENGTH_IDX]
        location = tuple(car_values[LOCATION_IDX])
        orientation = car_values[ORIENTATION_IDX]

        # check that params are valid, creates car and add to board
        if is_car_valid(car_name, length, orientation):
            car = Car(car_name, length, location, orientation)
            board.add_car(car)
            car_dict[car_name] = car

    game = Game(board)
    print(game.MSG['welcome'])
    game.play()
