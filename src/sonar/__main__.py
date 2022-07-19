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
ABOXL = int(HBOX * 1.25)  # Arc box limit so they leave screen
RWT = 2  # Reticle line weight
AWT = 4  # Arc line weight
RCNT = 20  # Center circle diameter
BLUE = (24, 53, 76)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HRETL = pygame.Rect(RWT, HBOX - RWT/2, BOX-(RWT*2), RWT)
VRETL = pygame.Rect(HBOX - RWT/2, RWT, RWT, BOX-(RWT*2))


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

        pygame.draw.arc(screen, GREEN, [HBOX,0,HBOX,BOX], 1.75*PI, PI/4, AWT)
        pygame.draw.arc(screen, GREEN, [HBOX,0,HBOX/2,BOX], 1.75*PI, PI/4, AWT)
        pygame.draw.arc(screen, GREEN, [HBOX,0,HBOX/4,BOX], 1.75*PI, PI/4, AWT)


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
    def reset_arc_gen(self):
        self.arc_gen_i = (     # Upper right
            pygame.Rect(HBOX, HBOX-x, x, x)
            for x in range(ABOXL)
        )
        self.arc_gen_iv = (    # Upper left
            pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x)
            for x in range(ABOXL)
        )
        self.arc_gen_iii = (   # Lower left
            pygame.Rect(HBOX-x, HBOX, x, x)
            for x in range(ABOXL)
        )
        self.arc_gen_ii = (    # Lower right
            pygame.Rect(HBOX, HBOX, x, x)
            for x in range(ABOXL)
        )

        self.arc_gen_right = (
            pygame.Rect(HBOX+x, HBOX-x, x, 2*x)
            for x in range(ABOXL)
        )

        self.arc_gen_left = (
            pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x)
            for x in range(ABOXL)
        )


        self.box_gen_i = (     # Upper right, green
            pygame.Rect(x, BOX, x, BOX)
            for x in range(ABOXL)
        )

        self.rad_gen_i = (
            (PI/4-PI/2*r/800, PI/4+PI/2*r/800)
            for r in range(800)
        )

    def __init__(self, scrn):
        self.screen = scrn
        self.pinging = False
        self.biosound = False
        self.reset_arc_gen()

    def draw_arcs_out(self):
        # t_rect =
        # pygame.draw.rect(self.screen, (0, 0, 255), t_rect)

        try:
            pygame.draw.arc(self.screen, RED,
                            next(self.arc_gen_iv), PI/2, PI, AWT)

            pygame.draw.arc(self.screen, GREEN, next(self.arc_gen_i), 0, PI/2, AWT)

            pygame.draw.arc(self.screen, RED, next(
                self.arc_gen_ii), 3*PI/2, 2*PI, AWT)

            pygame.draw.arc(self.screen, GREEN, next(
                self.arc_gen_iii), PI, 3*PI/2, AWT)

            pygame.draw.arc(self.screen, GREEN, next(
                self.arc_gen_right), 1.75*PI, PI/4, AWT)
            pygame.draw.arc(self.screen, GREEN, next(
                self.arc_gen_left), 0.75*PI, 1.25*PI, AWT)



            pygame.draw.arc(self.screen, RED, next(
                self.box_gen_i), *next(self.rad_gen_i), AWT)

        except StopIteration:
            self.pinging = False
            self.reset_arc_gen()
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


if __name__ == "__main__":
    main()
