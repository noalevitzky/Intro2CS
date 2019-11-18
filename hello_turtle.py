# the following code draws a flower bed using turtle functions

import turtle


def draw_petal():
    """these x lines draw a petal"""
    turtle.circle(100,90)
    turtle.left(90)
    turtle.circle(100,90)

def draw_flower():
    """these next lines draw a flower, using the draw_petal fn"""
    turtle.setheading(0)
    draw_petal()
    turtle.setheading(90)
    draw_petal()
    turtle.setheading(180)
    draw_petal()
    turtle.setheading(270)
    draw_petal()
    turtle.setheading(270)
    turtle.forward(250)

def draw_flower_advance():
    """these next lines draw a flower & move the turtle head in order to draw more flowers"""
    draw_flower()
    turtle.right(90)
    turtle.up()
    turtle.forward(250)
    turtle.right(90)
    turtle.forward(250)
    turtle.left(90)
    turtle.down()

def draw_flower_bed():
    """these next lines draw 3 flowers"""
    turtle.up()
    turtle.forward(200)
    turtle.left(180)
    turtle.down()
    draw_flower_advance()
    draw_flower_advance()
    draw_flower_advance()

if __name__ == "__main__" :
    draw_flower_bed()
    turtle.done
