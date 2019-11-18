import math


class Ship:
    RADIUS = 1
    START_LIFE = 3
    """

    """
    def __init__(self, x, y, x_speed=0, y_speed=0, heading=0):
        """

        :param x:
        :param y:
        :param x_speed:
        :param y_speed:
        :param heading:
        """
        self.__x = x
        self.__y = y
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        self.__heading = heading
        self.__radius = self.RADIUS
        self.__life = self.START_LIFE
        self.torpedo_count = 0

    def get_coor(self):
        return self.__x, self.__y

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_heading(self):
        return self.__heading

    def get_radius(self):
        return self.__radius

    def get_life(self):
        return self.__life

    def get_torpedo_count(self):
        return self.torpedo_count

    def move(self, new_x, new_y):
        self.__x = new_x
        self.__y = new_y

    def change_heading(self, direction):
        if direction == "r":
            self.__heading -= 7
        elif direction == "l":  # direction == "l"
            self.__heading += 7

    def acceleration(self):
        rad = math.radians(self.__heading)
        self.__x_speed = self.__x_speed + math.cos(rad)
        self.__y_speed = self.__y_speed + math.sin(rad)

    def change_torpedos(self, amount):
        self.torpedo_count += amount

    def remove_life(self):
        self.__life -= 1
