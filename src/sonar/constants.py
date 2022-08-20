import math
import pygame

EXCLUSIVE_PING = False
DEBUG = False
FADEOUT = True

# 0,0 is upper left of screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

PI = math.pi
BOX = 768  # Size of bounding box
HBOX = BOX // 2
CENTER = (HBOX, HBOX)  # Center of box
ABOXL = int(HBOX * 1)  # Arc box limit so they leave screen
RWT = 2  # Reticle line weight
ARC_SPEED = 4
AWT = 8  # Arc line weight
RCNT = 20  # Center circle diameter
BG_BLUE = (24, 53, 76)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HRETL = pygame.Rect(RWT, HBOX - RWT / 2, BOX - (RWT * 2), RWT)
VRETL = pygame.Rect(HBOX - RWT / 2, RWT, RWT, BOX - (RWT * 2))
TOP_SPEED = 10
RANGE = HBOX + (75 / 2)  # Range outside of which to delete contact
SUB_ICON = pygame.image.load("../../images/big_sub.png")
SUB_LOCATION = (HBOX - 50, HBOX - 40)

ANIMALS = ('orca', 'beluga', 'whale', 'seal',)
MESSAGES = ('hi', 'love', 'food', 'danger',)
