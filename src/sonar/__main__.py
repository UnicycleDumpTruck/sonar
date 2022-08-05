"""Command-line interface."""

from random import randint
from math import atan2, degrees, radians
import math
from time import sleep

from loguru import logger

import pygame
from pygame.locals import (
    K_p,
    K_o,
    K_r,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# 0,0 is upper left of screen

PI = math.pi
BOX = 600  # Size of bounding box
HBOX = BOX // 2
CENT = (HBOX, HBOX)  # Center of box
ABOXL = int(HBOX * 1.5)  # Arc box limit so they leave screen
RWT = 2  # Reticle line weight
ARC_SPEED = 4
AWT = 8  # Arc line weight
RCNT = 20  # Center circle diameter
BLUE = (24, 53, 76)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HRETL = pygame.Rect(RWT, HBOX - RWT/2, BOX-(RWT*2), RWT)
VRETL = pygame.Rect(HBOX - RWT/2, RWT, RWT, BOX-(RWT*2))

ping = pygame.mixer.Sound("high_ping.wav")


def angle_of_vector(x, y):
    # return math.degrees(math.atan2(-y, x))            # 1: with math.atan
    # 2: with pygame.math.Vector2.angle_to
    return pygame.math.Vector2(x, y).angle_to((1, 0))


def angle_of_line(x1, y1, x2, y2):
    # return math.degrees(math.atan2(-y1-y2, x2-x1))    # 1: math.atan
    # 2: pygame.math.Vector2.angle_to
    return angle_of_vector(x2-x1, y2-y1)


def get_angle(point_1, point_2):  # These can also be four parameters instead of two arrays
    angle = atan2(point_1[1] - point_2[1], point_1[0] - point_2[0])

    # # Optional
    # angle = degrees(angle)

    # OR
    angle = radians(angle)
    logger.debug(angle)
    return angle


def main() -> None:
    """Sonar."""

    # Set up the drawing window
    screen = pygame.display.set_mode([BOX, BOX])
    arc_mgr = ArcMgr(screen)

    # Run until quit
    running = True

    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    arc_mgr.start_ping()
                if event.key == K_o:
                    arc_mgr.arcs_from_xy(400, 400)
                if event.key == K_r:
                    rand_x = randint(0, BOX)
                    rand_y = randint(0, BOX)
                    arc_mgr.arc_to_center_from_xy(rand_x, rand_y)
                if event.key == K_ESCAPE:
                    running = False

        # Fill the background with blue
        screen.fill(BLUE)

        draw_reticle(screen)
        arc_mgr.draw()

        # Flip the display
        pygame.display.flip()

        sleep(0.01)

    # Running false, time to quit.
    pygame.quit()


def draw_reticle(scrn):
    # Outer White Circle
    pygame.draw.circle(scrn, WHITE, CENT, BOX//2-RWT)

    # Inner Blue Circle
    pygame.draw.circle(scrn, BLUE, CENT, BOX//2-(RWT*2))

    # Reticle crossing lines
    pygame.draw.rect(scrn, WHITE, HRETL)
    pygame.draw.rect(scrn, WHITE, VRETL)

    # Central Blanking circle
    pygame.draw.circle(scrn, BLUE, CENT, RCNT+RWT)

    # Central circle
    pygame.draw.circle(scrn, WHITE, CENT, RCNT)


class SoundArc:
    def __init__(self):
        pass


class ArcMgr:
    def arcs_from_xy(self, start_x, start_y):
        x_offset = start_x - HBOX
        y_offset = start_y - HBOX
        self.arcs.append(     # Upper right
            ((RED, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), 0+.2, PI/2-.2)
             for x in range(AWT, ABOXL, ARC_SPEED))
        )
        self.arcs.append(    # Upper left
            ((RED, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), PI/2+.2, PI-.2)
             for x in range(AWT, ABOXL, ARC_SPEED))
        )
        self.arcs.append(   # Lower left
            ((RED, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), PI+.2, 3*PI/2-.2)
             for x in range(AWT, ABOXL, ARC_SPEED))
        )
        self.arcs.append(    # Lower right
            ((RED, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), 3*PI/2+.2, 2*PI-.2)
             for x in range(AWT, ABOXL, ARC_SPEED))
        )

    def arc_to_center_from_xy(self, start_x, start_y):
        x_offset = start_x - HBOX
        y_offset = start_y - HBOX
        # angle = get_angle((HBOX, HBOX), (start_x, start_y))
        angle = angle_of_line(start_x, start_y, HBOX, HBOX)
        arc_start = radians(angle - (3*PI))
        arc_end = radians(angle + (3*PI))
        logger.debug(f"arc_start:{arc_start} arc_end:{arc_end}")
        self.arcs.append(     # Upper right
            ((RED, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), arc_start, arc_end)
             for x in range(AWT, ABOXL, ARC_SPEED))
        )

    def reset_empty_ping_arcs(self):
        self.arcs_from_xy(HBOX, HBOX)

    # def NOT_reset_empty_ping_arcs(self):
    #     self.arcs.append(     # Upper right
    #         ((RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 0+.2, PI/2-.2)
    #          for x in range(AWT, ABOXL, ARC_SPEED))
    #     )
    #     self.arcs.append(    # Upper left
    #         ((RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), PI/2+.2, PI-.2)
    #          for x in range(AWT, ABOXL, ARC_SPEED))
    #     )
    #     self.arcs.append(   # Lower left
    #         ((RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), PI+.2, 3*PI/2-.2)
    #          for x in range(AWT, ABOXL, ARC_SPEED))
    #     )

    #     self.arcs.append(    # Lower right
    #         ((RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 3*PI/2+.2, 2*PI-.2)
    #          for x in range(AWT, ABOXL, ARC_SPEED))
    #     )

        # self.arcs.append(
        #     ((BLACK, pygame.Rect(HBOX+x, HBOX-x, x, 2*x), 1.75*PI, PI/4,)
        #      for x in range(AWT, ABOXL, ARC_SPEED))
        # )

        # self.arcs.append(
        #     ((BLACK, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 0.75*PI, 1.25*PI,)
        #      for x in range(AWT, ABOXL, ARC_SPEED))
        # )

    def __init__(self, scrn):
        self.screen = scrn
        self.pinging = False
        self.biosound = False
        self.arcs = []

    def draw_single_arc(self, arc_gen):
        arc_details = next(arc_gen)
        points = [
            (arc_details[1][0], arc_details[1][1]),
            (arc_details[1][0], arc_details[1][1]+arc_details[1][3]),
            (arc_details[1][0]+arc_details[1][2],
             arc_details[1][1]+arc_details[1][3]),
            (arc_details[1][0]+arc_details[1][2], arc_details[1][1]),
        ]
        pygame.draw.lines(self.screen, arc_details[0], True, points, 1)
        pygame.draw.arc(self.screen, *arc_details, AWT)

    def draw_arcs_out(self):
        if self.arcs:
            for arc in self.arcs:
                try:
                    self.draw_single_arc(arc)
                except StopIteration:
                    self.arcs.remove(arc)
                    logger.debug("Arc generator exhausted.")
        else:
            self.pinging = False

    def draw(self):
        # if self.pinging:
        self.draw_arcs_out()

    def start_ping(self):
        # create generator, give main loop arc drawing object and sound player
        if self.pinging:
            logger.debug("Ping requested, but already pinging.")
            return
        else:
            logger.debug("Commencing ping.")
            self.pinging = True
            pygame.mixer.Sound.play(ping)
            self.arcs_from_xy(HBOX, HBOX)


if __name__ == "__main__":
    main()
