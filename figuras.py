"""Paint, for drawing shapes.

Exercises

1. Add a color.
2. Complete circle.
3. Complete rectangle.
4. Complete triangle.
5. Add width parameter.
"""
# Actividad 1 - Juego de pintura - Gael Antonio Espinoza - A01645982

from turtle import *  # Import all turtle functions
from freegames import vector  # Import vector for coordinate handling

def line(start, end):
    """Draw line from start to end."""
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)

def square(start, end):
    """Draw square from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for i in range(4):  # Loop for 4 sides of the square
        forward(end.x - start.x)
        left(90)

    end_fill()

def draw_circle(start, end):
    """Draw circle from start to end."""
    # Calcula el radio
    radio = ((end.x - start.x) ** 2 + (end.y - start.y) ** 2) ** 0.5
    up()
    goto(start.x, start.y - radio)  # Empieza en una posicion del circulo considerando el radio
    down()
    begin_fill()
    circle(radio)  # Traza el circulo
    end_fill()

def rectangle(start, end):
    """Draw rectangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for j in range(2):  # 2 iteraciones para los lados paralelos
        forward(end.x - start.x)
        left(90)
        forward(end.y - start.y)
        left(90)

    end_fill()

def triangle(start, end):
    """Draw triangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    # Dibuja un triangulo equilatero
    for k in range(3):  # Iteraciones para los 3 lados del triangulo
        forward(end.x - start.x)
        left(120)

    end_fill()

def tap(x, y):
    """Store starting point or draw shape."""
    start = state['start']

    if start is None:
        state['start'] = vector(x, y)  # Store the first click as the start point
    else:
        shape = state['shape']
        end = vector(x, y)  # Store the second click as the end point
        shape(start, end)  # Call the appropriate shape function with start and end points
        state['start'] = None  # Reset the start point

def store(key, value):
    """Store value in state at key."""
    state[key] = value

# Set up the drawing state and window
state = {'start': None, 'shape': line}
setup(420, 420, 370, 0)
onscreenclick(tap)
listen()

# Key bindings for undo and color changes
onkey(undo, 'u')
onkey(lambda: color('yellow'), 'Y')  # Color amarillo agregado
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')

# Key bindings for shape selection
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', draw_circle), 'c')  # Use draw_circle instead of circle
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')

done()
