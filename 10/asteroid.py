import math


class Asteroid:
    """

    """
    DEFAULT_ASTEROID_SIZE = 3
    SIZE_COEFFICIENT = 10
    NORMAL_FACTOR = 5

    def __init__(self, x, y, x_speed, y_speed, size=DEFAULT_ASTEROID_SIZE):
        """
        :param size: int 1-3
        """
        self.__x = x
        self.__y = y
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        self.__size = size
        self.asteroids_count = 0

    def get_coor(self):
        return self.__x, self.__y

    def get_speed(self):
        return self.__x_speed, self.__y_speed

    def get_size(self):
        return self.__size

    def move(self, new_x, new_y):
        self.__x = new_x
        self.__y = new_y

    def _calc_distance(self, obj):
        """
        :return: distance of obj from asteroid
        """
        obj_x, obj_y = obj.get_coor()
        asteroid_x, asteroid_y = self.get_coor()
        distance = math.sqrt((obj_x - asteroid_x)**2 + (obj_y - asteroid_y)**2)
        return distance

    def get_radius(self):
        """
        :return: asteroid's radius
        """
        return self.__size*self.SIZE_COEFFICIENT - self.NORMAL_FACTOR

    def has_intersection(self, obj):
        """
        :return: True if obj has intersection with asteroid, False otherwise
        """
        if self._calc_distance(obj) <= (self.get_radius() + obj.get_radius()):
            return True
        return False

