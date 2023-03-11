from sense_hat import SenseHat
from time import sleep
import random
import signal
import sys

sense = SenseHat()
sense.low_light = True

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
START_DELAY = 3
MATRIX_MIN_VALUE = 0
MATRIX_MAX_VALUE = 7
MATRIX_SIZE = 8

B = BLACK
R = RED
G = GREEN
P = (230, 230, 250)
DRAW_SNAKE = [
        B, B, B, B, B, B, B, G,
        B, G, G, G, G, G, G, G,
        B, G, B, B, B, B, B, B,
        B, G, G, G, G, G, B, B,
        B, B, B, B, B, G, B, B,
        P, G, P, G, G, G, B, B,
        G, G, G, B, B, B, B, B,
        R, B, B, B, B, B, B, B
        ]

def sigint_handler(signal, frame):
    sense.clear()
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

sense.set_pixels(DRAW_SNAKE)
sleep(5)
sense.clear()

while True:
    gameOverFlag = False
    growSnakeFlag = False
    generateRandomFoodFlag = False
    snakeMovementDelay = 0.5
    snakeMovementDelayDecrease = -0.01
    score = 0
    
    sense.clear()
    sense.show_message("SNAKE GAME")
    #set default start pos
    snakePosX = [3]
    snakePosY = [6]
    #gen food position
    while True:
        foodposX = random.randint(0, 7)
        foodposY = random.randint(0, 7)
        if foodposX != snakePosX[0] or foodposY != snakePosY[0]:
            break
    #default direction
    movementX = 0
    movementY = -1
    while not gameOverFlag:
        #check if snake ate food
        if foodposX == snakePosX[0] and foodposY == snakePosY[0]:
            growSnakeFlag = True
            generateRandomFoodFlag = True
            snakeMovementDelay += snakeMovementDelayDecrease
            score += 1
        #check for snakebite
        for i in range(1, len(snakePosX)):
            if snakePosX[i] == snakePosX[0] and snakePosY[i] == snakePosY[0]:
                gameOverFlag = True
        #check for gg
        if gameOverFlag:
            break
        #check for joystick input
        for event in sense.stick.get_events():
            if event.direction == "left" and movementX != 1:
                movementX = -1
                movementY = 0
                print("moved left")
            elif event.direction == "right" and movementX != -1:
                movementX = 1
                movementY = 0
                print("moved right")
            elif event.direction == "up" and movementY != 1:
                movementY = -1
                movementX = 0
                print("moved up")
            elif event.direction == "down" and movementY != -1:
                movementY = 1
                movementX = 0
                print("moved down")
            #grow snake
        if growSnakeFlag:
            growSnakeFlag = False
            snakePosX.append(0)
            snakePosY.append(0)
            #move snake
        for i in range((len(snakePosX) - 1), 0, -1):
            snakePosX[i] = snakePosX[i - 1]
            snakePosY[i] = snakePosY[i - 1]
        snakePosX[0] += movementX
        snakePosY[0] += movementY
            #check borders
        if snakePosX[0] > MATRIX_MAX_VALUE:
            snakePosX -= MATRIX_SIZE
        elif snakePosX[0] < MATRIX_MIN_VALUE:
            snakePosX += MATRIX_SIZE
        if snakePosY[0] > MATRIX_MAX_VALUE:
            snakePosY[0] -= MATRIX_SIZE
        elif snakePosY[0] < MATRIX_MIN_VALUE:
            snakePosY[0] += MATRIX_SIZE
            #spawn random food
        if generateRandomFoodFlag:
            generateRandomFoodFlag = False
            retryFlag = True
            while retryFlag:
                foodposX = random.randint(0,7)
                foodposY = random.randint(0,7)
                retryFlag = False
                for x, y in zip(snakePosX, snakePosY):
                    if x == foodposX and y == foodposY:
                        retryFlag = True
                        break
        #update matrix
        sense.clear()
        sense.set_pixel(foodposX, foodposY, RED)
        for x, y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, GREEN)
        sleep(snakeMovementDelay)
    #blink dead snake
    for loop in range(5):
        sense.clear()
        sense.set_pixel(foodposX, foodposY, RED)
        for x, y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, RED)
        sleep(0.5)
        sense.clear()
        sense.set_pixel(foodposX, foodposY, RED)
        for x, y in zip(snakePosX, snakePosY):
            sense.set_pixel(x, y, RED)
        sleep(0.5)
    sense.clear()
    while score:
        sense.show_message("Score: {}".format(score), text_colour=YELLOW)
        for event in sense.stick.get_events():
            if event.direction == "middle":
                score = 0
