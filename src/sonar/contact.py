from enum import Enum, auto
import time
from random import uniform
from loguru import logger
import pygame
from random import choice, randint
import constants

con_types = (
    'unknown',
    'sub',
    'ship',
    'whale',
    # 'dolphin',
    'shark',
    'narwhal',
    'orca',
)

con_weights = (
    0,  # UNK
    5,  # SUB
    5,  # SHIP
    12,  # WHALE
    # 15,  # DOLPHIN
    10,  # SHARK
    10,  # NARWHAL
    12,  # ORCA
)

con_image_filenames = {
    'unknown': "../../images/question.png",
    'ship': "../../images/ship.png",
    'sub': "../../images/sub.png",
    'whale': "../../images/whale.png",
    # 'dolphin': "../../images/dolphin.png",
    'shark': "../../images/shark.png",
    'narwhal': "../../images/narwhal.png",
    'orca': "../../images/whale.png"
}


class Contact(pygame.sprite.Sprite):
    """Sonar contact."""

    # Values are what the key will move toward:
    friends = {
        'unknown': [],
        'ship': [
            'dolphin',
            'whale',
            'shark',
            'sub',
            'narwhal',
            'orca',
        ],
        'sub': [
            'ship',
            'sub',
            'dolphin',
            'shark',
            'whale',
            'narwhal',
            'orca',
        ],
        'whale': [
            'whale',
            'orca',
            'dolphin',
            # 'sub',
        ],
        'dolphin': [
            'dolphin',
            'orca',
            'narwhal',
            'ship',
            # 'sub',
        ],
        'shark': [
            'ship',
            # 'sub',
        ],
        'narwhal': [
            'narwhal',
            # 'sub',
        ],
        'orca': [
            'orca',
            # 'sub',
        ]
    }

    # Values are what the key will flee:
    foes = {
        'unknown': [],
        'dolphin': [
            'shark',
        ],
        'ship': [],
        'whale': [
            'shark',
            'ship',
        ],
        'sub': [],
        'shark': [
            'orca',
            'dolphin'
        ],
        'narwhal': [
            'narwhal'
        ],
        'orca': [
            'orca'
        ],
    }

    def __init__(self, x, y, type='unknown'):
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
        self.last_sound = time.monotonic()
        self.time_to_next_sound = randint(8, 32)
        self.last_known_x = self.rect.x
        self.last_known_y = self.rect.y
        self.towards = pygame.Vector2(uniform(-2, 2), uniform(-2, 2))
        self.last_hailed = 0
        self.replies = 0

    def update(self):
        """Continue at set heading and speed. Return true if time to play sound."""

        if (time.monotonic() - self.last_move) > 0.5:
            self.last_move = time.monotonic()
            self.rect.center = self.rect.center + self.towards

        if self.last_hailed != 0 and ((time.monotonic() - self.last_hailed) > constants.HAIL_DELAY + self.replies):
            self.last_hailed = 0
            self.replies += randint(20, 30)
            logger.debug(f"{self.type} reply, reply counter: {self.replies}")
            return True

        if ((time.monotonic() - self.last_sound) > self.time_to_next_sound) and not self.last_hailed:
            self.last_sound = time.monotonic()
            self.time_to_next_sound = randint(30, 120)
            logger.debug(f"{self} randomly making a sound.")
            return True
        return False

    def heard(self, arc_gen):
        """Process sound and change heading and speed accordingly."""
        if arc_gen.originator == self:
            return None
        # heard_type = arc_gen.originator.type
        heard_type = arc_gen.arc_type.split('_')[0]
        # logger.debug(f"{self} heard {heard_type}")
        if heard_type in Contact.foes[self.type]:
            con_vector = pygame.Vector2(self.rect.center)
            sound_vector = pygame.Vector2(
                (arc_gen.originator.rect.centerx, arc_gen.originator.rect.centery,))
            direction = (con_vector - sound_vector)
            if direction.length() != 0:
                self.towards = direction.normalize() * self.speed
                # logger.debug(
                #     f"{self.type} fleeing {heard_type} noise from {arc_gen.originator.type} in direction: {self.towards}")
            # else:
            #     logger.warning(
            #         f"Direction vector == 0. {self.type} on top of {arc_gen.originator.type}.")

        if heard_type in Contact.friends[self.type]:
            con_vector = pygame.Vector2(self.rect.center)
            sound_vector = pygame.Vector2(
                (arc_gen.originator.rect.centerx, arc_gen.originator.rect.centery,))
            direction = (sound_vector - con_vector)
            if direction.length() != 0:
                self.towards = direction.normalize() * self.speed
            self.last_hailed = time.monotonic()
            #     logger.debug(
            #         f"{self.type} chasing {heard_type} noise from {arc_gen.originator.type} in direction: {self.towards}")
            # else:
            #     logger.warning(
            #         f"Direction vector == 0. {self.type} on top of {arc_gen.originator.type}.")

        # else:
        #     logger.debug(
        #         f"{self.type} heard {heard_type} from {arc_gen.originator.type} noise but doesn't care.")

    def __repr__(self):
        return f"{self.type} x{self.rect.centerx}y{self.rect.centery} t:{self.towards}"
