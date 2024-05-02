import turtle
import random
import math
import numpy as np
import time

random.seed(3314)
matrix = [[random.uniform(0,2) for j in range(11)] for i in range(11)]
k = 1.0 - 1 * 0.01 - 4 * 0.005 - 0.15
multipliedMatrix = np.multiply(matrix, k)
matrix_for_dir = np.floor(multipliedMatrix)
print(matrix_for_dir)
print()
undir_matrix = np.maximum(matrix_for_dir, np.transpose(matrix_for_dir))
print(undir_matrix)

positions = []

def drawNumbers():
    global positions
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-300, 300)
    count = 1
    vertical_spacing = -120 * 1.2
    horizontal_spacing = 180 * 1.2
    for i in range(4):
        positions.append(turtle.position())
        turtle.color("white")
        turtle.write(count, align="center")
        turtle.color("black")
        count += 1
        turtle.goto(turtle.xcor(), turtle.ycor() + vertical_spacing)
    for i in range(3):
        positions.append(turtle.position())
        turtle.color("white")
        turtle.write(count, align="center")
        turtle.color("black")
        count += 1
        turtle.goto(turtle.xcor() + horizontal_spacing, turtle.ycor())
    for i in range(4):
        positions.append(turtle.position())
        turtle.color("white")
        turtle.write(count, align="center")
        turtle.color("black")
        count += 1
        turtle.goto(turtle.xcor() - horizontal_spacing / 1.5, turtle.ycor() - vertical_spacing)
    turtle.hideturtle()

rad = 16

def drawCircles():
    turtle.speed(0)
    def draw_circle(x, y):
        turtle.begin_fill()
        turtle.penup()
        turtle.goto(x, y - rad)
        turtle.pendown()
        turtle.circle(rad)
        turtle.end_fill()
    for pos in positions:
        draw_circle(pos[0], pos[1])

def calculateDistance(start, end):
    distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    return distance

def getOrto(x, y):
    orthogonal_vector = (-y, x)
    magnitude = math.sqrt(orthogonal_vector[0] ** 2 + orthogonal_vector[1] ** 2)
    unit_vector = (orthogonal_vector[0] / magnitude, orthogonal_vector[1] / magnitude)
    return np.array(unit_vector)

def getStartPosition(pos1, pos_top):
    vec = (pos_top - pos1)
    vec = vec / calculateDistance(pos1, pos_top)
    return pos1 + vec * rad

def drawArrow(pos1, pos2, directed, k):
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    arr_vec = pos2 - pos1
    middle = (pos2 + pos1) / 2
    orto = getOrto(*arr_vec)
    dist_coef = k / calculateDistance(pos1, pos2) * 110
    side = 1 if dist_coef > 40 else -1
    orto = orto * side
    pos_top = middle + orto * dist_coef + orto * 40
    turtle.penup()
    pos_start = getStartPosition(pos1, pos_top)
    turtle.goto(pos_start[0], pos_start[1])
    turtle.pendown()
    turtle.goto(pos_top[0], pos_top[1])
    pos_end = getStartPosition(pos2, pos_top)
    turtle.goto(pos_end[0], pos_end[1])
    turtle.penup()
    if directed:
        drawDirectedArrow(pos_end, pos_top, pos2)

def drawDirectedArrow(pos_end, pos_top, pos2):
    width = 14 / 2
    length = 14
    orto2 = getOrto(*(pos_top - pos2))
    vec_back = (pos_top - pos_end) / calculateDistance(pos_top, pos_end)
    a = pos_end + vec_back * length
    turtle.goto(a + orto2 * width)
    turtle.pendown()
    turtle.begin_fill()
    turtle.goto(pos_end)
    turtle.penup()
    turtle.goto(a - orto2 * width)
    turtle.pendown()
    turtle.goto(pos_end)
    turtle.penup()
    turtle.goto(a - orto2 * width)
    turtle.pendown()
    turtle.goto(a + orto2 * width)
    turtle.end_fill()
    turtle.penup()

def drawSelfLoop(position, loop_size, directed):

    turtle.penup()
    turtle.goto(position[0], position[1] + rad)
    turtle.pendown()
    turtle.circle(loop_size)
    if directed:

        arrow_start_angle = 120
        arrow_length = 15
        arrow_width = 10


        arrow_pos_x = position[0] + loop_size * math.cos(math.radians(arrow_start_angle))
        arrow_pos_y = position[1] + 0.25*rad + loop_size * math.sin(math.radians(arrow_start_angle))


        arrow_dir_x = arrow_length * math.cos(math.radians(arrow_start_angle + 190))
        arrow_dir_y = arrow_length * math.sin(math.radians(arrow_start_angle + 190))


        turtle.penup()
        turtle.goto(arrow_pos_x, arrow_pos_y)
        turtle.pendown()
        turtle.begin_fill()
        turtle.goto(arrow_pos_x + arrow_dir_x, arrow_pos_y + arrow_dir_y)
        turtle.goto(arrow_pos_x - arrow_width, arrow_pos_y - arrow_width)
        turtle.goto(arrow_pos_x, arrow_pos_y)
        turtle.end_fill()

drawNumbers()
drawCircles()
drawNumbers()


for i in range(11):
    for j in range(i + 1):
        if undir_matrix[i][j]:
            if i == j:
                drawSelfLoop(positions[i],30,True)
            else:
                if i == 7:
                    k = 350
                elif i == 8 and 200 <= calculateDistance(positions[i], positions[j]) <= 280:
                    k = 50
                elif i > 8:
                    k = 30
                else:
                    k = 120
                drawArrow(positions[i], positions[j], directed=True, k=k)

time.sleep(6)
turtle.hideturtle()


turtle.clear()

drawNumbers()
drawCircles()
drawNumbers()

for i in range(11):
    for j in range(i + 1):
        if undir_matrix[i][j]:
            if i == j:
                drawSelfLoop(positions[i],30,False)
            else:
                if i == 7:
                    k = 350
                elif i == 8 and 200 <= calculateDistance(positions[i], positions[j]) <= 280:
                    k = 50
                elif i > 8:
                    k = 30
                else:
                    k = 120
                drawArrow(positions[i], positions[j], directed=False, k=k)

time.sleep(6)