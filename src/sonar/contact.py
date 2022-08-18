from enum import Enum, auto
import time
from random import uniform
import math
from loguru import logger
import pygame

class ConType(Enum):
    UNK = auto()
    SUB = auto()
    SHIP = auto()
    WHALE = auto()
    DOLPHIN = auto()
    SHARK = auto()
    NARWHAL = auto()
    ORCA = auto()


con_types = (
    ConType.UNK,
    ConType.SUB,
    ConType.SHIP,
    ConType.WHALE,
    ConType.DOLPHIN,
    ConType.SHARK,
    ConType.NARWHAL,
    ConType.ORCA,
)

con_weights = (
    0,  # UNK
    5,  # SUB
    5,  # SHIP
    12,  # WHALE
    15,  # DOLPHIN
    10,  # SHARK
    10,  # NARWHAL
    12,  # ORCA
)

con_image_filenames = {
    ConType.UNK: "question.png",
    ConType.SHIP: "ship.png",
    ConType.SUB: "sub.png",
    ConType.WHALE: "whale.png",
    ConType.DOLPHIN: "dolphin.png",
    ConType.SHARK: "shark.png",
    ConType.NARWHAL: "narwhal.png",
    ConType.ORCA: "whale.png"
}


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
            ConType.NARWHAL,
            ConType.ORCA,
        ],
        ConType.SUB: [
            ConType.SHIP,
            ConType.SUB,
            ConType.DOLPHIN,
            ConType.SHARK,
            ConType.WHALE,
            ConType.NARWHAL,
            ConType.ORCA,
        ],
        ConType.WHALE: [
            ConType.WHALE,
            ConType.ORCA,
            ConType.DOLPHIN,
            # ConType.SUB,
        ],
        ConType.DOLPHIN: [
            ConType.DOLPHIN,
            ConType.ORCA,
            ConType.NARWHAL,
            ConType.SHIP,
            # ConType.SUB,
        ],
        ConType.SHARK: [
            ConType.SHIP,
            # ConType.SUB,
        ],
        ConType.NARWHAL: [
            ConType.NARWHAL,
            # ConType.SUB,
        ],
        ConType.ORCA: [
            ConType.ORCA,
            # ConType.SUB,
        ]
    }

    # Values are what the key will flee:
    foes = {
        ConType.UNK: [],
        ConType.DOLPHIN: [
            ConType.SHARK,
        ],
        ConType.SHIP: [],
        ConType.WHALE: [
            ConType.SHARK,
            ConType.SHIP,
        ],
        ConType.SUB: [],
        ConType.SHARK: [
            ConType.ORCA,
            ConType.DOLPHIN
        ],
        ConType.NARWHAL: [
            ConType.NARWHAL
        ],
        ConType.ORCA: [
            ConType.ORCA
        ],
    }

    # TODO: movement toward good sounds away from bad
    # TODO: Categorize sounds good, bad, indifferent
    # TODO: wander away after period
    def __init__(self, x, y, type=ConType.UNK):
        """Initialize."""
        super().__init__()
        self.surf = pygame.Surface((75, 75))
        # self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.radius = self.rect.width // 2
        self.detected = False
        self.identified = False
        self.image = pygame.image.load(con_image_filenames[type])
        self.type = type
        self.alpha = 255
        self.last_activity = time.monotonic()
        self.max_age = 60
        self.heading = 0  # randint(0, 359)
        self.speed = 3
        self.last_move = time.monotonic()
        self.last_known_x = self.rect.x
        self.last_known_y = self.rect.y
        self.towards = pygame.Vector2(uniform(-2, 2), uniform(-2, 2))

    def update(self):
        """Continue at set heading and speed."""
        if time.monotonic() - self.last_move > 0.5:
            self.last_move = time.monotonic()
            new_x = int(
                (self.speed * math.cos(math.radians(self.heading))) + self.rect.left)
            new_y = int(
                (self.speed * math.sin(math.radians(self.heading))) + self.rect.top)
            #self.rect.x = new_x
            #self.rect.y = new_y

            self.rect.center = self.rect.center + self.towards

            # self.rect.move_ip(new_x, new_y)
            # logger.debug(
            #     f"speed:{self.speed} heading:{self.heading} new_x:{new_x} new_y:{new_y}")

    def heard(self, arc_gen):
        """Process sound and change heading and speed accordingly."""
        # logger.debug(
        #     f"{self} heard {arc_gen.arc_type} w tags {arc_gen.tags} originating from {arc_gen.originator}")
        heard_type = arc_gen.originator.type
        if heard_type in Contact.foes[self.type]:
            # logger.debug(
            #     f"Foe: I, {self.type} am afraid of {arc_gen.originator.type}!")

            con_vector = pygame.Vector2(self.rect.center)
            sound_vector = pygame.Vector2((arc_gen.originator.rect.centerx, arc_gen.originator.rect.centery,))
            direction = (con_vector - sound_vector)
            if direction.length() != 0:
                self.towards = direction.normalize() * self.speed
                logger.debug(f"{self.type} fleeing {arc_gen.originator.type} in direction: {self.towards}")
            else:
                logger.warning(f"Direction vector == 0. {self.type} on top of {arc_gen.originator.type}.")
           


        if heard_type in Contact.friends[self.type]:
            # logger.debug(
            #     f"Friendly {heard_type}! I, {self.type}, will go closer.")
            # prev_heading = self.heading
            # new_heading = angle_of_line(
            #     self.rect.centerx,
            #     self.rect.centery,
            #     #HBOX,
            #     #HBOX
            #     arc_gen.originator.rect.centerx,
            #     arc_gen.originator.rect.centery,
            #     # self.rect.centerx,
            #     # self.rect.centery
            # )
            # self.heading = new_heading

            con_vector = pygame.Vector2(self.rect.center)
            sound_vector = pygame.Vector2((arc_gen.originator.rect.centerx, arc_gen.originator.rect.centery,))
            self.towards = (sound_vector - con_vector).normalize() * self.speed
            print(self.towards)

            # logger.debug(
            #     f"{self.type} hdg chg {prev_heading} to {self.heading}")
        else:
            logger.debug(
                f"A {heard_type}, whatever, I, {self.type} don't care.")

    def __repr__(self):
        # heading:{self.heading} at rate:{self.speed}"
        return f"{self.type.name} centered at x:{self.rect.centerx} y:{self.rect.centery}, towards:{self.towards}"