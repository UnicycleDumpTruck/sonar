"""Command-line interface."""

import math
from time import sleep

from loguru import logger

import pygame
from pygame.locals import (
    K_p,
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
BOX = 800  # Size of bounding box
HBOX = BOX // 2
CENT = (HBOX, HBOX)  # Center of box
ABOXL = int(HBOX * 1.5)  # Arc box limit so they leave screen
RWT = 2  # Reticle line weight
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
    def reset_empty_ping_arcs(self):
        self.arc_gen_i = (     # Upper right
            (RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 0+.2, PI/2-.2)
            for x in range(0, ABOXL, 4)
        )
        self.arc_gen_iv = (    # Upper left
            (RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), PI/2+.2, PI-.2)
            for x in range(0, ABOXL, 4)
        )
        self.arc_gen_iii = (   # Lower left
            (RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), PI+.2, 3*PI/2-.2)
            for x in range(0, ABOXL, 4)
        )
        self.arc_gen_ii = (    # Lower right
            (RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 3*PI/2+.2, 2*PI-.2)
            for x in range(0, ABOXL, 4)
        )

        self.arc_gen_right = (
            (BLACK, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 1.75*PI, PI/4,)
            for x in range(0, ABOXL, 2)
        )

        self.arc_gen_left = (
            (BLACK, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), 0.75*PI, 1.25*PI,)
            for x in range(0, ABOXL, 2)
        )

    def __init__(self, scrn):
        self.screen = scrn
        self.pinging = False
        self.biosound = False
        self.arcs = {}
        self.reset_empty_ping_arcs()

    def draw_single_arc(self, arc_gen):
        arc_details = next(arc_gen)
        points = [
            (arc_details[1][0], arc_details[1][1]),
            (arc_details[1][0], arc_details[1][1]+arc_details[1][3]),
            (arc_details[1][0]+arc_details[1][2],
             arc_details[1][1]+arc_details[1][3]),
            (arc_details[1][0]+arc_details[1][2], arc_details[1][1]),
        ]
        # pygame.draw.lines(self.screen, arc_details[0], True, points, 1)
        pygame.draw.arc(self.screen, *arc_details, AWT)

    def draw_arcs_out(self):
        try:
            self.draw_single_arc(self.arc_gen_iv)
            self.draw_single_arc(self.arc_gen_i)
            self.draw_single_arc(self.arc_gen_ii)
            self.draw_single_arc(self.arc_gen_iii)

            # self.draw_single_arc(self.arc_gen_right)
            # self.draw_single_arc(self.arc_gen_left)

        except StopIteration:
            self.pinging = False
            self.reset_empty_ping_arcs()
            logger.debug("Arc generators exhausted.")

    def draw(self):
        if self.pinging:
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


if __name__ == "__main__":
    main()
