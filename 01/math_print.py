# the following code enables to practice the math module

import math


def golden_ratio():
    """calculates the golden ration"""
    print((1+math.sqrt(5))/2)

def six_cubed():
    """calculates 6 squared"""
    print(6**3)

def hypotenuse():
    """calculates the hypotenuse of a triangle"""
    print(math.sqrt(5*5+3*3))

def pi():
    """"prints pi's value"""
    print(math.pi)

def e():
    """prints e's value"""
    print(math.e)

def triangular_area():
    """calculates the areas of several triangles"""
    print((1*1)/2, (2*2)/2, (3*3)/2, (4*4)/2, (5*5)/2, (6*6)/2, (7*7)/2, (8*8)/2, (9*9)/2, (10*10)/2)


if __name__ == "__main__" :
    golden_ratio()
    six_cubed()
    hypotenuse()
    pi()
    e()
    triangular_area()
