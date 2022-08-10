"""Command-line interface."""

from random import randint
from math import atan2, degrees, radians
import math
from time import sleep
from itertools import chain

from loguru import logger

from rich.traceback import install
install(show_locals=True)

import pygame
from pygame.locals import (
    K_p,
    K_o,
    K_r,
    K_g,
    K_b,
    K_e,
    K_v,
    K_w,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

EXCLUSIVE_PING = False

# 0,0 is upper left of screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
PI = math.pi
BOX = 768  # Size of bounding box
HBOX = BOX // 2
CENT = (HBOX, HBOX)  # Center of box
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
HRETL = pygame.Rect(RWT, HBOX - RWT/2, BOX-(RWT*2), RWT)
VRETL = pygame.Rect(HBOX - RWT/2, RWT, RWT, BOX-(RWT*2))

ping = pygame.mixer.Sound("high_ping.wav")
r_ping = pygame.mixer.Sound("high_ping.wav")
g_ping = pygame.mixer.Sound("high_ping.wav")
b_ping = pygame.mixer.Sound("high_ping.wav")


def angle_of_vector(x, y):
    # return math.degrees(math.atan2(-y, x))            # 1: with math.atan
    # 2: with pygame.math.Vector2.angle_to
    return pygame.math.Vector2(x, y).angle_to((1, 0))


def angle_of_line(x1, y1, x2, y2):
    # return math.degrees(math.atan2(-y1-y2, x2-x1))    # 1: math.atan
    # 2: pygame.math.Vector2.angle_to
    return angle_of_vector(x2-x1, y2-y1)


def main() -> None:
    """Sonar."""

    # Set up the drawing window
    # screen = pygame.display.set_mode([BOX, BOX])
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    arc_mgr = ArcMgr(screen)
    pygame.mouse.set_visible(False)
    # Run until quit
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    arc_mgr.start_ping(RED)
                if event.key == K_g:
                    arc_mgr.start_ping(GREEN)
                if event.key == K_b:
                    arc_mgr.start_ping(BLACK)
                if event.key == K_o:
                    arc_mgr.arcs_from_xy(400, 400, GREEN)
                if event.key == K_e:
                    rand_x = randint(0, BOX)
                    rand_y = randint(0, BOX)
                    arc_mgr.arcs.extend(arc_mgr.arc_to_center_from_xy(rand_x, rand_y, GREEN))
                if event.key == K_v:
                    arc_mgr.arcs.extend(arc_mgr.arc_lower_right_bounced())
                if event.key == K_w:
                    arc_mgr.contacts.append(Contact(112, 655))


                if event.key == K_ESCAPE:
                    running = False

        # Fill the background with blue
        screen.fill(BG_BLUE)

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
    pygame.draw.circle(scrn, BG_BLUE, CENT, BOX//2-(RWT*2))

    # Reticle crossing lines
    pygame.draw.rect(scrn, WHITE, HRETL)
    pygame.draw.rect(scrn, WHITE, VRETL)

    # Central Blanking circle
    pygame.draw.circle(scrn, BG_BLUE, CENT, RCNT+RWT)

    # Central circle
    pygame.draw.circle(scrn, WHITE, CENT, RCNT)


class Arc():
    """Information to draw a single arc."""
    def __init__(self, color, rect, start, end):
        """Initialize."""
        self.color = color
        self.rect = rect
        self.start = start
        self.end = end
        self.radius = self.rect.width // 2

    def iterable(self):
        return (self.color, self.rect, self.start, self.end)


class ArcGen():
    def __init__(self, generator, echo=False):
        self.contacts = []
        self.generator = generator
        self.echo = echo 
    def __iter__(self):
        return self
    def __next__(self):
        return next(self.generator)

class Contact(pygame.sprite.Sprite):
    """Sonar contact."""
    def __init__(self, x, y):
        """Initialize."""
        super().__init__()
        self.surf = pygame.Surface((75,75))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = self.rect.width // 2
        self.detected = False
        self.image = pygame.image.load('question.png')
class ArcMgr:
    def arc_to_and_back_xy(self, start_x=HBOX, start_y=HBOX, end_x=ABOXL, end_y=ABOXL, color=GREEN):
        return chain(self.arcs_from_xy(color=RED), 
            *self.arc_to_center_from_xy(112, 655, color=RED))

    def arc_lower_right_bounced(self):
        return [ArcGen(
                chain(
                    ArcGen(Arc(RED, pygame.Rect(HBOX-x, HBOX-x, 2*x, 2*x), PI+.2, 3*PI/2-.2)
                        for x in range(AWT, 150, ARC_SPEED)),
                (Contact(150, 617) for _ in range(1)),
                *self.arc_to_center_from_xy(150,617,RED),
                )
            )]

    def arcs_from_xy(self, start_x=HBOX, start_y=HBOX, color=RED):
        x_offset = start_x - HBOX
        y_offset = start_y - HBOX
        return [     # Upper right
            ArcGen(Arc(color, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), 0+.2, PI/2-.2)
                for x in range(AWT, ABOXL, ARC_SPEED)),
            ArcGen(Arc(color, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), PI/2+.2, PI-.2)
                for x in range(AWT, ABOXL, ARC_SPEED)),
            ArcGen(Arc(color, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), PI+.2, 3*PI/2-.2)
                for x in range(AWT, ABOXL, ARC_SPEED)),
            ArcGen(Arc(color, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), 3*PI/2+.2, 2*PI-.2)
                for x in range(AWT, ABOXL, ARC_SPEED)),
        ]

    def arc_to_center_from_xy(self, start_x, start_y, color):
        x_offset = start_x - HBOX
        y_offset = start_y - HBOX
        angle = angle_of_line(start_x, start_y, HBOX, HBOX) # comes back in degrees
        # logger.debug(f"Angle: {angle}")
        arc_start =  radians(angle - 45) # convert to rads for pygame arc
        arc_end = radians(angle + 45)    # confert to rads for pygame arc
        return [
            ArcGen((Arc(color, pygame.Rect(HBOX-x+x_offset, HBOX-x+y_offset, 2*x, 2*x), arc_start, arc_end)
                for x in range(AWT, ABOXL, ARC_SPEED)), echo=True),
        ]

    def __init__(self, scrn):
        self.screen = scrn
        self.pinging = False
        self.biosound = False
        self.arcs = []
        self.contacts = []

    def draw_single_arc(self, arc_gen):
        arc_details = next(arc_gen)
        if isinstance(arc_details, Contact):
            self.contacts.append(arc_details)
        else:
            points = [
                (arc_details.rect[0], arc_details.rect[1]),
                (arc_details.rect[0], arc_details.rect[1]+arc_details.rect[3]),
                (arc_details.rect[0]+arc_details.rect[2],
                arc_details.rect[1]+arc_details.rect[3]),
                (arc_details.rect[0]+arc_details.rect[2], arc_details.rect[1]),
            ]
            ## Outline arcs with boxes:
            pygame.draw.lines(self.screen, arc_details.color, True, points, 1)
            pygame.draw.arc(self.screen, *arc_details.iterable(), AWT)

        if not arc_gen.echo:
            # if con := pygame.sprite.spritecollideany(arc_details, self.contacts):
            collide = pygame.sprite.spritecollide(arc_details, self.contacts, False, pygame.sprite.collide_circle)
            for con in collide:
                print(arc_gen.contacts)
                if con not in arc_gen.contacts:
                    self.arcs.extend(self.arc_to_center_from_xy(con.rect.centerx, con.rect.centery, GREEN))
                    arc_gen.contacts.append(con)
                    print(arc_gen, arc_gen.contacts)
                

    def draw(self):
        if self.arcs:
            for arc in self.arcs:
                try:
                    self.draw_single_arc(arc)
                except StopIteration:
                    self.arcs.remove(arc)
        else:
            self.pinging = False
        for con in self.contacts:
            #con.rect.center = con.rect.topleft
            self.screen.blit(con.image, con.rect.topleft)


    def start_ping(self, color=RED, sound=ping):
        if self.pinging and EXCLUSIVE_PING:
            logger.debug("Ping requested, but already pinging.")
            return
        else:
            logger.debug("Commencing ping.")
            self.pinging = True
            pygame.mixer.Sound.play(sound)
            self.arcs.extend(self.arcs_from_xy(HBOX, HBOX, color))


if __name__ == "__main__":
    main()
