from enum import Enum, auto
import time
from random import uniform
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
    ConType.UNK: "../../images/question.png",
    ConType.SHIP: "../../images/ship.png",
    ConType.SUB: "../../images/sub.png",
    ConType.WHALE: "../../images/whale.png",
    ConType.DOLPHIN: "../../images/dolphin.png",
    ConType.SHARK: "../../images/shark.png",
    ConType.NARWHAL: "../../images/narwhal.png",
    ConType.ORCA: "../../images/whale.png"
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
            self.rect.center = self.rect.center + self.towards

    def heard(self, arc_gen):
        """Process sound and change heading and speed accordingly."""
        heard_type = arc_gen.originator.type
        if heard_type in Contact.foes[self.type]:
            con_vector = pygame.Vector2(self.rect.center)
            sound_vector = pygame.Vector2((arc_gen.originator.rect.centerx, arc_gen.originator.rect.centery,))
            direction = (con_vector - sound_vector)
            if direction.length() != 0:
                self.towards = direction.normalize() * self.speed
                logger.debug(f"{self.type} fleeing {arc_gen.originator.type} in direction: {self.towards}")
            else:
                logger.warning(f"Direction vector == 0. {self.type} on top of {arc_gen.originator.type}.")  


        if heard_type in Contact.friends[self.type]:
            con_vector = pygame.Vector2(self.rect.center)
            sound_vector = pygame.Vector2((arc_gen.originator.rect.centerx, arc_gen.originator.rect.centery,))
            direction = (sound_vector - con_vector)
            if direction.length() != 0:
                self.towards = direction.normalize() * self.speed
                logger.debug(f"{self.type} chasing {arc_gen.originator.type} in direction: {self.towards}")
            else:
                logger.warning(f"Direction vector == 0. {self.type} on top of {arc_gen.originator.type}.")  

        else:
            logger.debug(
                f"{self.type} heard {heard_type} but doesn't care.")

    def __repr__(self):
        return f"{self.type.name} centered at x:{self.rect.centerx} y:{self.rect.centery}, towards:{self.towards}"