import math


class Torpedo:
    """

    """
    RADIUS = 4
    ACC_FACTOR = 2

    def __init__(self, x, y, x_speed, y_speed, heading):
        self.__x = x
        self.__y = y
        self.__heading = heading
        rad = math.radians(self.__heading)
        self.__x_speed = x_speed + self.ACC_FACTOR * math.cos(rad)
        self.__y_speed = y_speed + self.ACC_FACTOR * math.sin(rad)
        self.__radius = self.RADIUS
        self.__life_time = 0

    def get_coor(self):
        return self.__x, self.__y

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_heading(self):
        return self.__heading

    def get_radius(self):
        return self.__radius

    def get_life_time(self):
        return self.__life_time

    def move(self, new_x, new_y):
        self.__x = new_x
        self.__y = new_y

    def add_life_time(self):
        self.__life_time += 1



