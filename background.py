import turtle
import random
import time

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Random Geometric Shapes with Lines")
screen.setup(width=1.0, height=1.0)  # Use the whole screen

# Create a turtle object
pen = turtle.Turtle()
pen.speed(1)  # Slow down the animation

# Function to draw a random shape
def draw_random_shape(size):
    sides = random.randint(3, 8)  # Random number of sides (3-8)
    angle = 360 / sides

    for _ in range(sides):
        pen.forward(size)
        pen.right(angle)

# Function to draw a random line
def draw_random_line():
    pen.penup()
    pen.goto(random.randint(-400, 400), random.randint(-300, 300))
    pen.pendown()
    pen.goto(random.randint(-400, 400), random.randint(-300, 300))

# Draw shapes and lines
for _ in range(10):  # Adjust the number of shapes
    size = random.randint(20, 100)
    draw_random_shape(size)
    draw_random_line()
    time.sleep(0.5)  # Pause for half a second

turtle.done()