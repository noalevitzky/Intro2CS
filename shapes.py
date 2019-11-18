# this function calculates the area of the shape that the user chooses, based of the provided inputs

import math

PI = math.pi
TRI_AREA = (math.sqrt(3) / 4)

def circle_area():
    r = int(input())
    area = PI * (r ** 2)
    return int(area)

def rectangle_area():
    a = float(input())
    b = float(input())
    area = a * b
    return int(area)

def triangle_area():
    c = float(input())
    area = TRI_AREA * (c ** 2)
    return int(area)

def shape_area():
    """user chooses a shape"""
    shape = input('Choose shape (1=circle, 2=rectangle, 3=triangle): ')
    shape = int(shape)

    if shape == 1:
        area = circle_area()

    elif shape == 2:
        area = rectangle_area()

    elif shape == 3:
        area = triangle_area()

    else:
        return None

    return area
