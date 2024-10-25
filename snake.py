from turtle import *
from random import randrange, random
from freegames import square, vector

# Colores para víbora y comida (sin incluir rojo)
colores_disponibles = ['blue', 'yellow', 'purple', 'orange', 'cyan']

# Asignación de colores distintos usando random
indice_vibora = randrange(len(colores_disponibles))
indice_comida = randrange(len(colores_disponibles))

# Asegura que los colores sean distintos
while indice_comida == indice_vibora:
    indice_comida = randrange(len(colores_disponibles))

color_vibora = colores_disponibles[indice_vibora]
color_comida = colores_disponibles[indice_comida]

def mover_comida():
    """Mueve la comida un paso aleatorio sin salirse de la ventana."""
    movimiento = vector(randrange(-1, 2) * 10, randrange(-1, 2) * 10)
    nueva_posicion = food + movimiento

    if -200 < nueva_posicion.x < 190 and -200 < nueva_posicion.y < 190:
        food.move(movimiento)

    ontimer(mover_comida, 500)  # Programar siguiente movimiento en 500ms

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190

def move():
    "Move snake forward one segment."
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    # Dibujar la víbora con el color asignado
    for body in snake:
        square(body.x, body.y, 9, color_vibora)

    # Dibujar la comida con el color asignado
    square(food.x, food.y, 9, color_comida)
    update()
    ontimer(move, 100)

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

move()
mover_comida()  # Iniciar movimiento aleatorio de la comida
done()
