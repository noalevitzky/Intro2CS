class Board:
    """
    represented by list of lists. each cell is either empty '_', occupied by a car or the target cell 'E'.
    board size is permanent 7X7, starting at index (0,0) at the top left cell. Target cell is at index (3,7).
    """
    EMPTY_CELL = '_'
    TARGET_CELL = 'E'

    def __init__(self, height=7, width=7):
        """
        initialize the game board, based on width and height.
        """
        self.__height = height
        self.__width = width
        self.__board_cur_lst = self.__init_board()
        self.__list_of_cells = self.cell_list()
        self.__num_cars = 0
        # list of car names on board, considering there's only one car with that name/color
        self.__cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_str = ''
        for row in self.__board_cur_lst:
            row = ' '.join(row)
            board_str += row
            board_str += '\n'
        return board_str

    def __init_board(self):
        """
        :return: list of lists that represent an empty board
        """
        board_list = []

        # initiate empty board
        for row in range(self.__height):
            if row == int((self.__height - 1) / 2):
                board_list.append(['_'] * self.__width + ['E'])
            else:
                board_list.append(['_'] * self.__width)
        return board_list

    def __update_board(self, car):
        """
        :param car:
        :return: fill in car's locations in board (represented by car name)
        """
        for cell in self.__list_of_cells:
            i, j = cell

            # remove old car coordinates from board
            if self.__board_cur_lst[i][j] == car.get_name():
                self.__board_cur_lst[i][j] = self.EMPTY_CELL

            # adds new car coordinates to board
            if cell in car.car_coordinates():
                self.__board_cur_lst[i][j] = car.get_name()

    def cell_list(self):
        """
        This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        lst = []

        # adds all 7X7 cells to list
        for i, row in enumerate(range(self.__height)):
            for j, col in enumerate(range(self.__width)):
                cell = (i,j)
                lst.append(cell)

        # adds target location to list (3,7)
        lst.append(self.target_location())

        self.__list_of_cells = lst
        return lst

    def possible_moves(self):
        """
        This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) representing legal moves
        """
        lst = []
        for car_name, car in self.__cars.items():

            for move in self.__single_car_possible_moves(car):
                # move is of form (name,movekey,description)
                lst.append(move)
        return lst

    def __single_car_possible_moves(self, car):
        """
        :return: list of lists.
        each inner list represent a possible car move, and is of form (name,movekey,description)
        """
        lst = []

        # get possible car moves, based on car's orientation.
        for movekey in car.possible_moves():

            # get movement requirements.
            for target_cell in car.movement_requirements(movekey):
                target_row, target_col = target_cell

                # check if movement requirements could be fulfilled-
                # validate that new location of car is in board cells, and is not occupied.
                if self.__board_cur_lst[target_row][target_col] in self.__list_of_cells and \
                        self.__board_cur_lst[target_row][target_col] == Board.EMPTY_CELL:
                    lst.append((car.get_name(),movekey,car.possible_moves()[movekey]))
        return lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        target_row = int((self.__height - 1) / 2)     # middle row of board
        target_col = self.__width             # first col that is out of board range
        target = (target_row,target_col)
        return target

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate
        board_coordinate = self.__board_cur_lst[row][col]

        # target coordinate is occupied, returns winning car's name
        if coordinate == self.target_location() and board_coordinate != self.TARGET_CELL:
            return board_coordinate

        # regular coordinate is not occupied, returns car's name
        if coordinate != self.target_location() and board_coordinate != self.EMPTY_CELL:
                return board_coordinate

        # coordinate is empty
        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        for cell in car.car_coordinates():
            if cell not in self.__list_of_cells:
                # car's location is not in board range
                return False

            if self.cell_content(cell):
                # car's location in board is occupied
                return False

        # car is valid, add car to cars (dict)
        self.__cars[car.get_name()] = car
        self.__num_cars += 1
        self.__update_board(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.__cars.keys():
            return False

        car = self.__cars[name]
        moves_dict = car.possible_moves()

        if movekey not in moves_dict:
            return False

        if not self.__is_car_requirements_are_met(name, movekey):
            return False

        if not car.move(movekey):
            return False

        self.__update_board(car)
        return True

    def __is_car_requirements_are_met(self, car_name, movekey):
        """
        :return: True if new car coordinates in board, False otherwise
        """
        lst = self.__cars[car_name].movement_requirements(movekey)
        for cell in lst:
            if cell not in self.__list_of_cells:
                return False
            if self.cell_content(cell):
                # car's location in board is occupied
                return False
        return True
