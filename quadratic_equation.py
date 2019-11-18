# this function solves the quadratic equation

import math


def quadratic_equation(a, b, c):
    delta = (b**2 - 4*a*c)
    if delta > 0:
        sqr_delta = (math.sqrt(delta))
        x1 = int((-b + sqr_delta)/(2*a))
        x2 = int((-b - sqr_delta)/(2*a))
    elif delta == 0:
        x1 = None
        x2 = int(-b/(2*a))
    else:
        x1 = None
        x2 = None
    return x2, x1

# the next function solving the previous one, based on user input

def quadratic_equation_user_input():
    numbers = input("Insert coefficients a, b, and c: ")
    x, y, z = numbers.split( )
    x1, x2 = quadratic_equation(x,y,z)
    if x1 != None and x2 != None:
        print("The equation has 2 solutions: " + str(x1) + " and " + str(x2))
    elif x1 == None and x2 != None:
        print("The equation has 1 solution: " + str(x2))
    else:
        print("The equation has no solutions")

