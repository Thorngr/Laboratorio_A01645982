# -*- coding: utf-8 -*-
tap_count = 0  # Inicializa el contador de taps


"""Memory, puzzle game of number pairs.

Exercises:

1. Count and print how many taps occur.
2. Decrease the number of tiles to a 4x4 grid.
3. Detect when all tiles are revealed.
4. Center single-digit tile.
5. Use letters instead of tiles.
"""
#Gael Antonio Espinoza A01645982 Actividad 5 Juego de Memoria

from random import *
from turtle import *

from freegames import path

car = path('car.gif')
tiles = list(range(32)) * 2
state = {'mark': None}
hide = [True] * 64


def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    global tap_count
    tap_count += 1  # Conteo de taps realizados

    spot = index(x, y)  # Cuadro seleccionado
    mark = state['mark']  # Cuadro marcado previamente

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        # Si no hay marca previa o se seleccionó el mismo cuadro, marca este cuadro
        state['mark'] = spot
    else:
        # Si los cuadros coinciden, destapa ambos
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None  # Reinicia la marca



def todos_descubiertos(hide):
    """Revisa si todos los cuadros estan descubiertos."""
    conteo_cubiertos = 0  # Inicializa el contador de cuadros cubiertos

    for h in hide:
        if h:  #Si el cuadro esta cubierto, lo cuenta
            conteo_cubiertos += 1

    if conteo_cubiertos == 0: 
        print("Todos los cuadros estan descubiertos.")


def draw():
    """Draw image and tiles."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    # Mostrar el conteo de taps en la esquina superior izquierda
    goto(-180, 180)  # Posición para mostrar el conteo
    color('black')
    write(f"Taps: {tap_count}", font=('Arial', 16, 'normal'))

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 25, y - 15)  # Ajuste para centrar mejor el texto
        color('black')
        write(tiles[mark], align='center', font=('Arial', 30, 'normal'))

    # Verificar si todos los cuadros han sido descubiertos
    if todos_descubiertos(hide):
        goto(0, 0)
        write("Ganaste!", align='center', font=('Arial', 30, 'bold'))
        return  # Detener la función para no seguir dibujando

    update()
    ontimer(draw, 100)



shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
