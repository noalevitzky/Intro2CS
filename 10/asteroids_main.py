from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random
import sys
import math

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    X = 0
    Y = 1
    MAX_TORPEDOS = 10
    TORPEDO_SHOT = 1
    TORPEDO_GONE = -1
    TORPEDO_MAX_LIFE = 200
    MIN_ASTEROID_SPEED = 1
    MAX_ASTEROID_SPEED = 4
    LOSE_LIFE_MSG = ('Ship lost 1 life!', 'Ship was hit by an asteroid.')
    ALL_AST_EXPLODED = ('All asteroids were exploded', 'Good job, you won!')
    NO_LIFE = ('Ship has no life left', 'Better luck next time!')
    Q_PRESSED = ('\'q\' was pressed', 'See you again soon!')
    BIG_SIZE, FEW_POINTS = (3, 20)
    MEDIUM_SIZE, MEDIUM_POINTS = (2, 50)
    SMALL_SIZE, MANY_POINTS = (1, 100)

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__torpedo_list = []
        self.__asteroids_amount = asteroids_amount
        self.__asteroids_list = []
        self.__ship = self.init_ship()
        self.create_asteroids(self.__asteroids_amount)
        self.__game_points = 0

    def init_ship(self):
        """
        create ship and draw it on screen
        """
        x, y = self._random_coor()
        ship = Ship(x, y)
        x, y, x_speed, y_speed, heading = self._obj_prams(ship)
        self.__screen.draw_ship(x, y, heading)
        return ship

    def create_asteroids(self, amount, asteroid=None, new_size=None, torpedo=None):
        """
        first, init asteroids and draw them on screen.
        if asteroid was sent, func splits it into 2 new asteroids and draw them on screen (orig asteroid is deleted).
        """
        if asteroid:
            # split given asteroid
            x_old, y_old, x_speed_old, y_speed_old, size_old = self._obj_prams(asteroid)
            x_speed_new1, y_speed_new1, x_speed_new2, y_speed_new2 = self.new_asteroid_speed(x_speed_old,
                                                                                             y_speed_old, torpedo)
            asteroid1 = Asteroid(x_old, y_old, x_speed_new1, y_speed_new1, new_size)
            asteroid2 = Asteroid(x_old, y_old, x_speed_new2, y_speed_new2, new_size)

            self.update_game_asteroids(asteroid, asteroid1, asteroid2)
            self.draw_asteroid(asteroid1, new_size, x_old, y_old)
            self.draw_asteroid(asteroid2, new_size, x_old, y_old)

        # init asteroids
        for i in range(amount):
            x, y = self._random_coor()
            x_speed, y_speed = self._random_speed()
            asteroid = Asteroid(x, y, x_speed, y_speed)
            size = asteroid.get_size()

            self.update_game_asteroids(asteroid)
            self.draw_asteroid(asteroid, size, x, y)

    def update_game_asteroids(self, asteroid, asteroid1=None, asteroid2=None):
        """
        append new asteroid/s to list and update asteroids count.
        if asteroid was split, remove orig one from screen as well.
        """
        if asteroid1 and asteroid2:
            # split asteroid
            self.remove_asteroid(asteroid)
            self.__asteroids_list.append(asteroid1)
            self.__asteroids_list.append(asteroid2)
        else:
            # new asteroid
            self.__asteroids_list.append(asteroid)
        asteroid.asteroids_count += 1

    def draw_asteroid(self, asteroid, size, x, y):
        """
        adds asteroid to screen
        """
        self.__screen.register_asteroid(asteroid, size)
        self.__screen.draw_asteroid(asteroid, x, y)

    def create_torpedo(self, ship, x, y, x_speed, y_speed, heading):
        """
        if user pressed space, a torpedo is added to the game (unless max torpedo was reached).
        """
        if ship.get_torpedo_count() == self.MAX_TORPEDOS:
            return
        torpedo = Torpedo(x, y, x_speed, y_speed, heading)
        self.__torpedo_list.append(torpedo)
        self.__screen.register_torpedo(torpedo)
        ship.change_torpedos(self.TORPEDO_SHOT)
        x1, y1, x_speed1, y_speed1, heading1 = self._obj_prams(torpedo)
        self.__screen.draw_torpedo(torpedo, x1, y1, heading1)

    def _random_coor(self, is_ship=None):
        """
        func sets a random coordinate.
        if there are other obj on board, checks if coordinate is empty.
        if coordinate is occupied, randomize again.
        :return: x, y
        """
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        if self.__asteroids_list:
            # there are asteroids on board
            while not self._is_empty(x, y, is_ship):
                x = random.randint(self.__screen_min_x, self.__screen_max_x)
                y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x, y

    def _random_speed(self):
        """
        randomize asteroid speed (between 1 and 4 for each axis)
        """
        x_speed = random.randint(self.MIN_ASTEROID_SPEED, self.MAX_ASTEROID_SPEED)
        y_speed = random.randint(self.MIN_ASTEROID_SPEED, self.MAX_ASTEROID_SPEED)
        return x_speed, y_speed

    def _is_empty(self, x, y, is_ship):
        """
        :return: True if coordinate is empty, False otherwise
        """
        for asteroid in self.__asteroids_list:
            asteroid_x, asteroid_y = asteroid.get_coor()
            if x == asteroid_x and y == asteroid_y:
                return False

        # for asteroids only, checks if ship in coordinate
        if not is_ship:
            ship_x, ship_y = self.__ship.get_coor()
            if x == ship_x and y == ship_y:
                return False

        # coordinate is empty
        return True

    def change_obj_location(self, obj):
        """
        change obj location
        """
        dx = self.__screen_max_x - self.__screen_min_x
        dy = self.__screen_max_y - self.__screen_min_y
        x, y = obj.get_coor()
        x_speed, y_speed = obj.get_speed()
        new_x = (x_speed + x - self.__screen_min_x) % dx + self.__screen_min_x
        new_y = (y_speed + y - self.__screen_min_y) % dy + self.__screen_min_y
        obj.move(new_x, new_y)

    def change_heading(self, obj):
        """
        change obj heading based on user's input
        """
        if self.__screen.is_left_pressed():
            obj.change_heading("l")
        elif self.__screen.is_right_pressed():
            obj.change_heading("r")

    def acceleration(self, obj):
        """
        speed up ship based on user's input
        """
        if self.__screen.is_up_pressed():
            obj.acceleration()

    def teleported(self):
        """
        moves ship to a new coordinate, based on user's request
        """
        if self.__screen.is_teleport_pressed():
            x, y = self._random_coor('is_ship')
            self.__ship.move(x, y)

    def new_asteroid_speed(self, x_speed_old, y_speed_old, torpedo):
        """
        when asteroid is split into 2 new asteroids, calc new asteroids' speed
        :return: asteroid1 speed(x&y) , asteroid2 speed(x&y)
        """
        x_torpedo, y_torpedo, x_speed_torpedo, y_speed_torpedo, heading_torpedo = self._obj_prams(torpedo)
        x_speed_new1 = x_speed_torpedo + x_speed_old / math.sqrt(x_speed_old**2 + y_speed_old**2)
        y_speed_new1 = y_speed_torpedo + y_speed_old / math.sqrt(x_speed_old**2 + y_speed_old**2)
        x_speed_new2 = x_speed_torpedo - x_speed_old / math.sqrt(x_speed_old**2 + y_speed_old**2)
        y_speed_new2 = y_speed_torpedo - y_speed_old / math.sqrt(x_speed_old**2 + y_speed_old**2)
        return x_speed_new1, y_speed_new1, x_speed_new2, y_speed_new2

    def _obj_prams(self, obj):
        """
        :return: object parameters (coordinates, speed and size/heading)
        """
        x, y = obj.get_coor()
        x_speed, y_speed = obj.get_speed()

        if isinstance(obj, Asteroid):
            size = obj.get_size()
            return x, y, x_speed, y_speed, size

        # obj type is Torpedo or ship
        heading = obj.get_heading()
        return x, y, x_speed, y_speed, heading

    def is_asteroid_hit(self, obj):
        """
        :return : the asteroid that was hit, False otherwise
        """
        for asteroid in self.__asteroids_list:
            if asteroid.has_intersection(obj):
                return asteroid
        return False

    def remove_asteroid(self, asteroid):
        """
        remove asteroid from list, from asteroid count and from screen
        """
        self.__asteroids_list.remove(asteroid)
        asteroid.asteroids_count -= 1
        self.__screen.unregister_asteroid(asteroid)

    def remove_torpedo(self, torpedo):
        """
        remove torpedo from list and from screen
        """
        self.__torpedo_list.remove(torpedo)
        self.__ship.change_torpedos(self.TORPEDO_GONE)
        self.__screen.unregister_torpedo(torpedo)

    def remove_life(self, asteroid):
        """
        sends msg to user, remove ship life and remove hitting asteroid
        """
        title, msg = self.LOSE_LIFE_MSG
        self.__screen.show_message(title, msg)
        self.__ship.remove_life()
        self.__screen.remove_life()
        self.remove_asteroid(asteroid)

    def torpedo_hit_asteroid(self, torpedo, asteroid):
        """
        set new score to user, split asteroid and remove torpedo from screen
        """
        asteroid_size = asteroid.get_size(asteroid)
        self._set_score(asteroid_size)
        self.split_asteroid(asteroid, asteroid_size, torpedo)
        self.remove_torpedo(torpedo)

    def _set_score(self, asteroid_size):
        """
        set score based on asteroid size
        """
        points = 0
        if asteroid_size == self.BIG_SIZE:
            points = self.FEW_POINTS
        if asteroid_size == self.MEDIUM_SIZE:
            points = self.MEDIUM_POINTS
        if asteroid_size == self.SMALL_SIZE:
            points = self.MANY_POINTS
        self.__game_points += points
        self.__screen.set_score(self.__game_points)

    def split_asteroid(self, asteroid, asteroid_size, torpedo):
        """
        split asteroid based on asteroid's size. if asteroid is small, just remove it from board
        """
        if asteroid_size == self.BIG_SIZE:
            new_size = self.MEDIUM_SIZE
            self.create_asteroids(2, asteroid, new_size, torpedo)
        if asteroid_size == self.MEDIUM_SIZE:
            new_size = self.SMALL_SIZE
            self.create_asteroids(2, asteroid, new_size, torpedo)
        if asteroid_size == self.SMALL_SIZE:
            self.remove_asteroid(asteroid)

    def is_game_over(self):
        """
        game is over if either:
        1. asteroids list is empty
        2. ship has no life
        3. user pressed 'q' (quit)
        """
        if not self.__asteroids_list:
            title, msg = self.ALL_AST_EXPLODED
            self.__screen.show_message(title, msg)
            return True
        if self.__ship.get_life() == 0:
            title, msg = self.NO_LIFE
            self.__screen.show_message(title, msg)
            return True
        if self.__screen.should_end():
            title, msg = self.Q_PRESSED
            self.__screen.show_message(title, msg)
            return True
        #######################################
        # need to edit this func, not final

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _move_objects(self):
        """
        one iteration of obj movement
        """
        # move ship
        ship = self.__ship
        x, y, x_speed, y_speed, heading = self._obj_prams(ship)
        self.__screen.draw_ship(x, y, heading)
        self.teleported()
        self.change_heading(ship)
        self.acceleration(ship)
        self.change_obj_location(ship)

        # move asteroids
        for asteroid in self.__asteroids_list:
            xa, ya, x_speeda, y_speeda, size = self._obj_prams(asteroid)
            self.__screen.draw_asteroid(asteroid, xa, ya)
            self.change_obj_location(asteroid)

        # creates and move torpedo
        if self.__screen.is_space_pressed():
            self.create_torpedo(ship, x, y, x_speed, y_speed, heading)
        if self.__torpedo_list:
            for torpedo in self.__torpedo_list:
                x1, y1, x_speed1, y_speed1, heading1 = self._obj_prams(torpedo)
                self.__screen.draw_torpedo(torpedo, x1, y1, heading1)
                self.change_obj_location(torpedo)
                torpedo.add_life_time()
                if torpedo.get_life_time() == self.TORPEDO_MAX_LIFE:
                    self.remove_torpedo(torpedo)

    def _game_loop(self):
        """
        move obj, checks if asteroid was hit by ship/ torpedo and acts accordingly
        """
        self._move_objects()

        # check if asteroid hit ship
        if self.is_asteroid_hit(self.__ship):
            asteroid = self.is_asteroid_hit(self.__ship)
            self.remove_life(asteroid)

        # check if asteroid was hit by a torpedo
        for torpedo in self.__torpedo_list:
            if self.is_asteroid_hit(torpedo):
                asteroid = self.is_asteroid_hit(torpedo)
                self.torpedo_hit_asteroid(torpedo, asteroid)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
