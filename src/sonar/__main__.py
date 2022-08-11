"""Main program file for sonar interface."""
import math
import time
from enum import Enum
from enum import auto
from itertools import chain
from math import atan2
from math import degrees
from math import radians
from random import randint

import pygame
from loguru import logger
from pygame.locals import K_DOWN
from pygame.locals import K_ESCAPE
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_UP
from pygame.locals import KEYDOWN
from pygame.locals import QUIT
from pygame.locals import K_b
from pygame.locals import K_e
from pygame.locals import K_g
from pygame.locals import K_o
from pygame.locals import K_p
from pygame.locals import K_r
from pygame.locals import K_t
from pygame.locals import K_v
from pygame.locals import K_w
from rich.traceback import install


install(show_locals=True)


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

EXCLUSIVE_PING = False
DEBUG = False

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
RANGE = HBOX + (75/2) # Range outside of which to delete contact

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
    return angle_of_vector(x2 - x1, y2 - y1)


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
                    arc_mgr.arcs.extend(
                        arc_mgr.arc_to_center_from_xy(rand_x, rand_y, GREEN)
                    )
                if event.key == K_t:
                    angle = randint(0, 359)
                    # radius = randint(100, HBOX)
                    radius = HBOX - 40
                    x = radius * math.cos(angle) + HBOX
                    y = radius * math.sin(angle) + HBOX
                    logger.debug(f"Random contact at {x,y}")
                    arc_mgr.contacts.append(Contact(x, y))
                if event.key == K_v:
                    arc_mgr.contacts.append(Contact(150, 617))
                    # arc_mgr.arcs.extend(arc_mgr.arc_lower_right_bounced())
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

        time.sleep(0.01)

    # Running false, time to quit.
    pygame.quit()


def draw_reticle(scrn):
    # Outer White Circle
    pygame.draw.circle(scrn, WHITE, CENTER, BOX // 2 - RWT)

    # Inner Blue Circle
    pygame.draw.circle(scrn, BG_BLUE, CENTER, BOX // 2 - (RWT * 2))

    # Reticle crossing lines
    pygame.draw.rect(scrn, WHITE, HRETL)
    pygame.draw.rect(scrn, WHITE, VRETL)

    # Central Blanking circle
    pygame.draw.circle(scrn, BG_BLUE, CENTER, RCNT + RWT)

    # Central circle
    pygame.draw.circle(scrn, WHITE, CENTER, RCNT)


class Arc:
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


class ArcType(Enum):
    PING = auto()
    PING_ECHO = auto()
    BIO = auto()
    BIO_ECHO = auto()


class ArcGen:
    def __init__(self, generator, arc_type):
        self.contacts = []
        self.generator = generator
        self.arc_type = arc_type

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.generator)


class ConType(Enum):
    UNK = auto()
    SUB = auto()
    SHIP = auto()
    WHALE = auto()
    DOLPHIN = auto()
    SHARK = auto()


class Contact(pygame.sprite.Sprite):
    """Sonar contact."""

    # Values are what the key will move toward:
    friends = {
        ConType.UNK: [],
        ConType.SHIP: [
            ConType.DOLPHIN,
            ConType.WHALE,
            ConType.SHARK,
            ConType.SUB,
        ],
        ConType.SUB: [
            ConType.SHIP,
            ConType.DOLPHIN,
            ConType.SHARK,
            ConType.WHALE,
        ],
        ConType.WHALE: [
            ConType.WHALE,
        ],
        ConType.DOLPHIN: [
            ConType.DOLPHIN,
            ConType.SHIP,
            ConType.SUB,
        ],
        ConType.SHARK: [
            ConType.SHIP,
            ConType.SUB,
        ]
    }

    # Values are what the key will flee:
    foes = {
        ConType: [],
        ConType.DOLPHIN: [
            ConType.SHARK,
        ],
        ConType.SHIP: [],
        ConType.WHALE: [
            ConType.SHARK,
            ConType.SHIP,
        ],
        ConType.SUB: [],
        ConType.SHARK: [],
    }

    # TODO: movement toward good sounds away from bad
    # TODO: Categorize sounds good, bad, indifferent
    # TODO: wander away after period
    def __init__(self, x, y):
        """Initialize."""
        super().__init__()
        self.surf = pygame.Surface((75, 75))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = self.rect.width // 2
        self.detected = False
        self.identified = False
        self.image = pygame.image.load("question.png")
        self.type = ConType.UNK
        self.alpha = 255
        self.last_activity = time.monotonic()
        self.max_age = 60
        self.heading = randint(0, 359)
        self.speed = 3
        self.last_move = time.monotonic()
        self.last_known_x = self.rect.x
        self.last_known_y = self.rect.y

    def update(self):
        """Continue at set heading and speed."""
        if time.monotonic() - self.last_move > 0.5:
            self.last_move = time.monotonic()
            new_x = int((self.speed * math.cos(self.heading)) + self.rect.left)
            new_y = int((self.speed * math.sin(self.heading)) + self.rect.top)
            self.rect.x = new_x
            self.rect.y = new_y
            # self.rect.move_ip(new_x, new_y)
            logger.debug(f"speed:{self.speed} heading:{self.heading} new_x:{new_x} new_y:{new_y}")

    def heard(self):
        """Process sound and change heading and speed accordingly."""
        pass

class ArcMgr:
    def __init__(self, scrn):
        self.screen = scrn
        self.pinging = False
        self.biosound = False
        self.arcs = []
        self.contacts = []

    def arcs_from_xy(
        self, start_x=HBOX, start_y=HBOX, color=RED, arc_type=ArcType.PING
    ):
        x_offset = start_x - HBOX
        y_offset = start_y - HBOX
        return [  # Upper right
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            HBOX - x + x_offset, HBOX - x + y_offset, 2 * x, 2 * x
                        ),
                        0 + 0.2,
                        PI / 2 - 0.2,
                    )
                    for x in range(AWT, ABOXL, ARC_SPEED)
                ),
                arc_type,
            ),
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            HBOX - x + x_offset, HBOX - x + y_offset, 2 * x, 2 * x
                        ),
                        PI / 2 + 0.2,
                        PI - 0.2,
                    )
                    for x in range(AWT, ABOXL, ARC_SPEED)
                ),
                arc_type,
            ),
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            HBOX - x + x_offset, HBOX - x + y_offset, 2 * x, 2 * x
                        ),
                        PI + 0.2,
                        3 * PI / 2 - 0.2,
                    )
                    for x in range(AWT, ABOXL, ARC_SPEED)
                ),
                arc_type,
            ),
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            HBOX - x + x_offset, HBOX - x + y_offset, 2 * x, 2 * x
                        ),
                        3 * PI / 2 + 0.2,
                        2 * PI - 0.2,
                    )
                    for x in range(AWT, ABOXL, ARC_SPEED)
                ),
                arc_type,
            ),
        ]

    def arc_to_center_from_xy(self, start_x, start_y, color, arc_type):
        x_offset = start_x - HBOX
        y_offset = start_y - HBOX
        angle = angle_of_line(start_x, start_y, HBOX, HBOX)  # comes back in degrees
        # logger.debug(f"Angle: {angle}")
        arc_start = radians(angle - 30)  # convert to rads for pygame arc
        arc_end = radians(angle + 30)  # confert to rads for pygame arc
        return [
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            HBOX - x + x_offset, HBOX - x + y_offset, 2 * x, 2 * x
                        ),
                        arc_start,
                        arc_end,
                    )
                    for x in range(AWT, ABOXL, ARC_SPEED)
                ),
                arc_type=arc_type,
            ),
        ]

    def draw_single_arc(self, arc_gen):
        arc_details = next(arc_gen)
        if isinstance(arc_details, Contact):
            self.contacts.append(arc_details)
        else:
            points = [
                (arc_details.rect[0], arc_details.rect[1]),
                (arc_details.rect[0], arc_details.rect[1] + arc_details.rect[3]),
                (
                    arc_details.rect[0] + arc_details.rect[2],
                    arc_details.rect[1] + arc_details.rect[3],
                ),
                (arc_details.rect[0] + arc_details.rect[2], arc_details.rect[1]),
            ]
            if DEBUG:
                pygame.draw.lines(self.screen, arc_details.color, True, points, 1)

            pygame.draw.arc(self.screen, *arc_details.iterable(), AWT)

        if arc_gen.arc_type in {ArcType.PING}:
            collide = pygame.sprite.spritecollide(
                arc_details, self.contacts, False, pygame.sprite.collide_circle
            )
            for con in collide:
                # print(arc_gen.contacts)
                if con not in arc_gen.contacts:
                    self.arcs.extend(
                        self.arc_to_center_from_xy(
                            con.rect.centerx,
                            con.rect.centery,
                            arc_details.color,
                            ArcType.PING_ECHO,
                        )
                    )
                    arc_gen.contacts.append(con)
                    con.detected = True
                    con.alpha = 255
                    con.last_known_x = con.rect.x
                    con.last_known_y = con.rect.y

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
            con.update()
            if con.detected:
                self.screen.blit(con.image, (con.last_known_x, con.last_known_y))
                con.alpha -= 0.6
                con.alpha = max(con.alpha, 0)
                con.image.set_alpha(con.alpha)
                # if con.alpha < 5:
                    # con.update()
            if pygame.math.Vector2(con.rect.centerx, con.rect.centery).distance_to(CENTER) > RANGE:
            # if time.monotonic() - con.last_activity > con.max_age:
                self.contacts.remove(con)
                del(con)
                logger.debug("Contact out of range, deleted.")


            if DEBUG:
                pygame.draw.rect(
                    self.screen,
                    RED,
                    pygame.Rect(
                        con.rect.left, con.rect.top, con.rect.width, con.rect.height
                    ),
                    2,
                )

    def start_ping(self, color=RED, sound=ping):
        if self.pinging and EXCLUSIVE_PING:
            logger.debug("Ping requested, but already pinging.")
            return
        else:
            logger.debug("Commencing ping.")
            self.pinging = True
            pygame.mixer.Sound.play(sound)
            self.arcs.extend(self.arcs_from_xy(HBOX, HBOX, color, ArcType.PING))


if __name__ == "__main__":
    main()
