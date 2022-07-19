"""Command-line interface."""

import pygame
import math
from time import sleep

pygame.init()

# 0,0 is upper left of screen

PI = math.pi
BOX = 800  # Size of bounding box
HBOX = BOX // 2
CENT = (HBOX, HBOX)  # Center of box
RWT = 16  # Reticle line weight
AWT = 8  # Arc line weight
RCNT = 20  # Center circle diameter
BLUE = (24, 53, 76)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HRETL = pygame.Rect(RWT, HBOX - RWT/2, BOX-(RWT*2), RWT)
VRETL = pygame.Rect(HBOX - RWT/2, RWT, RWT, BOX-40)


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

        # Fill the background with blue
        screen.fill(BLUE)

        draw_reticle(screen)
        arc_mgr.draw_arcs_out()

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


class ArcMgr:
    arc_gen_i = arc_gen = (     # Upper right, green
        pygame.Rect(HBOX, HBOX-x, x, x)
        for x in range(HBOX)
    )
    arc_gen_iv = arc_gen = (    # Upper left, Blue
        pygame.Rect(HBOX-x, HBOX-x, x, x)
        for x in range(HBOX)
    )
    arc_gen_iii = arc_gen = (   # Lower left, black
        pygame.Rect(HBOX-x, HBOX, x, x)
        for x in range(HBOX)
    )
    arc_gen_ii = arc_gen = (    # Lower right, Red
        pygame.Rect(HBOX, HBOX, x, x)
        for x in range(HBOX)
    )

    def __init__(self, scrn):
        self.screen = scrn

    def reset_arc_gen(self):
        arc_gen = (
            (x, x)
            for x in range(BOX)
        )

    def draw_arcs_out(self):
        # establish a generator of positions with angles, each call uses one until gone
        # return iter_left # number of iterations left in generator

        # t_rect =
        # pygame.draw.rect(self.screen, (0, 0, 255), t_rect)

        pygame.draw.arc(self.screen, RED,
                        next(self.arc_gen_iv), PI/2, PI, AWT)

        pygame.draw.arc(self.screen, GREEN, next(self.arc_gen_i), 0, PI/2, AWT)

        pygame.draw.arc(self.screen, RED, next(
            self.arc_gen_ii), 3*PI/2, 2*PI, AWT)

        pygame.draw.arc(self.screen, GREEN, next(
            self.arc_gen_iii), PI, 3*PI/2, AWT)


def start_ping():
    # create generator, give main loop arc drawing object and sound player
    pass


if __name__ == "__main__":
    main()
