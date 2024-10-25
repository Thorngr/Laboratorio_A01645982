"""Snake, classic arcade game with moving food and random colors.

1. The food moves randomly one step at a time within the window.
2. Snake and food have different colors selected randomly from a list (excluding red).
"""

from random import randrange, choice
from turtle import *
from freegames import square, vector

# List of possible colors (excluding red)
colors = ['blue', 'green', 'yellow', 'purple', 'orange']

# Assign random colors for snake and food, ensuring they are different
snake_color = choice(colors)
food_color = choice([c for c in colors if c != snake_color])

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y

def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

def move_food():
    """Move food one step randomly within the window boundaries."""
    options = [vector(10, 0), vector(-10, 0), vector(0, 10), vector(0, -10)]  # Possible movements
    move = choice(options)
    new_position = food + move

    # Ensure the food stays inside the window
    if -190 < new_position.x < 190 and -190 < new_position.y < 190:
        food.move(move)

    # Schedule the next move of the food
    ontimer(move_food, 500)

def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')  # Game over, show red head
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

    for body in snake:
        square(body.x, body.y, 9, snake_color)  # Draw snake with random color

    square(food.x, food.y, 9, food_color)  # Draw food with random color
    update()
    ontimer(move, 100)

# Setup the game window
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()

# Bind arrow keys to change direction
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

# Start the game
move()
move_food()  # Start moving the food
done()
