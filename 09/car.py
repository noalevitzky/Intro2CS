ROW = 0
COL = 1
VERTICAL = 0
HORIZONTAL = 1
MOVES = 'udlr'
UP, DOWN, LEFT, RIGHT = MOVES
ERROR_MSG = {
    'illegal direction': 'Illegal direction. Car {} was not moved'
}


class Car:
    """
    one dimensional object that could be added and moved
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name.
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location.
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL).
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in.
        """
        lst = []

        # for vertical cars- rows change, column is constant.
        if self.__orientation == VERTICAL:
            for i in range(self.__length):
                lst.append((self.__location[ROW]+i, self.__location[COL]))

        # for horizontal cars- row is constant, columns change.
        if self.__orientation == HORIZONTAL:
            for i in range(self.__length):
                lst.append((self.__location[ROW], self.__location[COL]+i))

        return lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        moves_dict = {}

        # The keys for vertical cars are 'u' and 'd'.
        if self.__orientation == VERTICAL:
            moves_dict = {
                'u': "cause the car to go up",
                'd': "cause the car to go down"
            }

        # The keys for horizontal cars are 'l' and 'r'.
        if self.__orientation == HORIZONTAL:
            moves_dict = {
                'l': "cause the car to go left",
                'r': "cause the car to go right"
            }

        return moves_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        lst = []

        # appends the cells that should be empty to lst, based on required direction.
        if movekey == UP:
            lst = [(self.__location[ROW]-1, self.__location[COL])]
        if movekey == DOWN:
            last_cell = self.car_coordinates()[-1]
            lst = [(last_cell[ROW]+1, last_cell[COL])]
        if movekey == LEFT:
            lst = [(self.__location[ROW], self.__location[COL]-1)]
        if movekey == RIGHT:
            last_cell = self.car_coordinates()[-1]
            lst = [(last_cell[ROW], last_cell[COL]+1)]

        return lst

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # get current location of car.
        row, col = self.__location

        # if required move is possible, set new location.
        if movekey in self.possible_moves():
            if movekey == UP:
                self.__set_location((row-1, col))
            if movekey == DOWN:
                self.__set_location((row+1, col))
            if movekey == LEFT:
                self.__set_location((row, col-1))
            if movekey == RIGHT:
                self.__set_location((row, col+1))

            return True

        # required move is illegal
        else:
            print(ERROR_MSG['illegal direction'].format(self.__name))
            return False

    def __set_location(self, new_location):
        """
        Changes the car location
        """
        self.__location = new_location

    def get_name(self):
        """
        :return: The name of this car.
        """
        return str(self.__name)

