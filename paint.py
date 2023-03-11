from sense_hat import SenseHat
from time import sleep
import random
import signal
import sys

sense = SenseHat()
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

B = BLACK
R = RED
G = GREEN
P = (230, 230, 250)
W = (255, 255, 255)
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
FROG = [
        B, G, G, G, B, G, G, G,
        B, G, P, G, B, G, P, G,
        G, G, G, G, G, G, G, G,
        G, P, P, P, P, P, P, P,
        G, G, G, G, G, G, G, G,
        G, G, G, G, G, G, G, G,
        G, G, G, G, G, G, G, G,
        G, G, B, G, G, G, B, G
        ]
CREEP = []

def sigint_handler(signal, frame):
    sense.clear()
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

sense.set_pixels(DRAW_SNAKE)
sleep(5)
sense.set_pixels(FROG)
sleep(5)
sense.clear()
