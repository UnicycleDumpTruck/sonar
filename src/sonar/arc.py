import math
import time
from random import randint, choice, choices
from loguru import logger
import pygame

import contact
import constants
import snd


def angle_of_vector(x, y):
    return pygame.math.Vector2(x, y).angle_to((1, 0))


def angle_of_line(x1, y1, x2, y2):
    return angle_of_vector(x2 - x1, y2 - y1)


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


class ArcGen:
    def __init__(self, generator, arc_type, originator, silent=False, tags=[]):
        self.contacts = []
        self.generator = generator
        self.arc_type = arc_type
        self.silent = silent
        self.tags = tags
        self.originator = originator

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.generator)


class ArcMgr:
    def __init__(self, scrn):
        self.screen = scrn
        self.pinging = False
        self.biosound = False
        self.arcs = []
        self.contacts = []
        self.listener = contact.Contact(
            constants.HX - 12, constants.HY - 12, 'sub')  # was x - 50, y - 40
        self.listener.rect.width = 100
        self.listener.rect.height = 100
        self.listener.radius = 50
        self.num_contacts = randint(
            constants.MIN_NUM_CON, constants.MAX_NUM_CON)
        self.time_to_next_con = randint(
            constants.MIN_TIME_BTWN_CON, constants.MAX_TIME_BTWN_CON)
        self.time_of_last_con = time.monotonic()
        logger.debug(f"num_contacts = {self.num_contacts}")
        logger.debug(f"time_to_next_con = {self.time_to_next_con}")

    def rand_contact(self):
        angle = randint(0, 359)
        radius = randint(200, constants.HBOX)
        x = radius * math.cos(math.radians(angle)) + constants.HX
        y = radius * math.sin(math.radians(angle)) + constants.HY
        new_contact = contact.Contact(x, y, choices(
            contact.con_types, contact.con_weights, k=1)[0])
        self.contacts.append(new_contact)
        logger.debug(f"Random contact: {new_contact}")

    def arcs_from_xy(
        self, originator, start_x=constants.HX, start_y=constants.HY, color=constants.RED, arc_type='ping_a', tags=[]
    ):
        x_offset = start_x - constants.HX
        y_offset = start_y - constants.HY
        return [  # Upper right
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            constants.HX - x + x_offset, constants.HY - x + y_offset, 2 * x, 2 * x
                        ),
                        0 + 0.2,
                        constants.PI / 2 - 0.2,
                    )
                    for x in range(constants.AWT, constants.ABOXL, constants.ARC_SPEED)
                ),
                arc_type,
                originator,
                silent=True,  # Only one of these four should cause an audible echo
                tags=tags,
            ),
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            constants.HX - x + x_offset, constants.HY - x + y_offset, 2 * x, 2 * x
                        ),
                        constants.PI / 2 + 0.2,
                        constants.PI - 0.2,
                    )
                    for x in range(constants.AWT, constants.ABOXL, constants.ARC_SPEED)
                ),
                arc_type,
                originator,
                silent=True,
                tags=tags,
            ),
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            constants.HX - x + x_offset, constants.HY - x + y_offset, 2 * x, 2 * x
                        ),
                        constants.PI + 0.2,
                        3 * constants.PI / 2 - 0.2,
                    )
                    for x in range(constants.AWT, constants.ABOXL, constants.ARC_SPEED)
                ),
                arc_type,
                originator,
                silent=True,
                tags=tags,
            ),
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            constants.HX - x + x_offset, constants.HY - x + y_offset, 2 * x, 2 * x
                        ),
                        3 * constants.PI / 2 + 0.2,
                        2 * constants.PI - 0.2,
                    )
                    for x in range(constants.AWT, constants.ABOXL, constants.ARC_SPEED)
                ),
                arc_type,
                originator,
                silent=False,  # This one will cause an audible echo
                tags=tags,
            ),
        ]

    def arc_to_center_from_xy(self, originator, start_x, start_y, color, arc_type, tags=[]):
        x_offset = start_x - constants.HX
        y_offset = start_y - constants.HY
        angle = angle_of_line(start_x, start_y, constants.HX,
                              constants.HY)  # comes back degrees
        # logger.debug(f"Angle: {angle}")
        arc_start = math.radians(angle - 30)  # convert to rads for pygame arc
        arc_end = math.radians(angle + 30)  # confert to rads for pygame arc
        return [
            ArcGen(
                (
                    Arc(
                        color,
                        pygame.Rect(
                            constants.HX - x + x_offset, constants.HY - x + y_offset, 2 * x, 2 * x
                        ),
                        arc_start,
                        arc_end,
                    )
                    for x in range(constants.AWT, constants.ABOXL, constants.ARC_SPEED)
                ),
                arc_type=arc_type,
                originator=originator,
                silent=False,
                tags=tags,
            ),
        ]

    def draw_single_arc(self, arc_gen):
        arc_details = next(arc_gen)
        if isinstance(arc_details, contact.Contact):
            self.contacts.append(arc_details)
        else:
            points = [
                (arc_details.rect[0], arc_details.rect[1]),
                (arc_details.rect[0],
                 arc_details.rect[1] + arc_details.rect[3]),
                (
                    arc_details.rect[0] + arc_details.rect[2],
                    arc_details.rect[1] + arc_details.rect[3],
                ),
                (arc_details.rect[0] +
                 arc_details.rect[2], arc_details.rect[1]),
            ]
            if constants.DEBUG:
                pygame.draw.lines(
                    self.screen, arc_details.color, True, points, 1)

            pygame.draw.arc(
                self.screen, *arc_details.iterable(), constants.AWT)
        # logger.debug(f"arc_type:{arc_gen.arc_type}")
        # if arc_gen.arc_type in {'ping_a', 'ping_b'} and not arc_gen.silent:
        if 'echo' not in arc_gen.arc_type and not arc_gen.silent:
            collide = pygame.sprite.spritecollide(
                arc_details, self.contacts, False, pygame.sprite.collide_circle
            )
            for con in collide:
                if con not in arc_gen.contacts:
                    con.heard(arc_gen)
                    # logger.debug(
                    #     f"Arc of type {arc_gen.arc_type} collided contact w tags {arc_gen.tags}")
                    if arc_gen.arc_type in {'ping', 'ping_a', 'ping_b', } and not arc_gen.silent:
                        self.arcs.extend(
                            self.arc_to_center_from_xy(
                                con,
                                con.rect.centerx,
                                con.rect.centery,
                                arc_details.color,
                                arc_gen.arc_type + '_echo',
                            )
                        )
                        arc_gen.contacts.append(con)
                        con.detected = True
                        con.alpha = 255
                        con.last_known_x = con.rect.x
                        con.last_known_y = con.rect.y
                    # TODO combine these
        elif arc_gen.arc_type in {'ping_a_echo', 'ping_b_echo'} and not arc_gen.silent:
            if pygame.sprite.spritecollide(
                arc_details, [
                    self.listener], False, pygame.sprite.collide_circle
            ):
                # Echo has come back to submarine.
                # logger.debug(f"Playing sound: {arc_gen.arc_type.name}")
                pygame.mixer.Sound.play(snd.sounds[arc_gen.arc_type])
                arc_gen.silent = True
                self.listener.heard(arc_gen)

    def draw(self):
        if (len(self.contacts) < self.num_contacts) and ((time.monotonic() - self.time_of_last_con) > self.time_to_next_con):
            self.rand_contact()
            self.num_contacts = randint(
                constants.MIN_NUM_CON, constants.MAX_NUM_CON)
            self.time_to_next_con = randint(
                constants.MIN_TIME_BTWN_CON, constants.MAX_TIME_BTWN_CON)
            self.time_of_last_con = time.monotonic()
            logger.debug(f"num_contacts = {self.num_contacts}")
            logger.debug(f"time_to_next_con = {self.time_to_next_con}")

        if self.arcs:
            for arc in self.arcs:
                try:
                    self.draw_single_arc(arc)
                except StopIteration:
                    self.arcs.remove(arc)
        else:
            self.pinging = False
        for con in self.contacts:
            if con.update():
                # logger.debug(f"Time for {con.type} to make some noise")
                if rand_sound := snd.sounds[con.type +
                                            choice(['_hi', '_food', '_danger', '_love'])]:
                    pygame.mixer.Sound.play(rand_sound)
                    self.arcs.extend(self.arcs_from_xy(
                        con, con.rect.centerx, con.rect.centery, constants.BLUE, f"{con.type}_hi"))
                    con.alpha = 255
                    con.last_known_x = con.rect.x
                    con.last_known_y = con.rect.y
                    con.detected = True
                # TODO combine these
                # con.image.set_alpha(255)

            if con.detected:
                if constants.FADEOUT:
                    self.screen.blit(
                        con.image, (con.last_known_x, con.last_known_y))
                    con.alpha -= 0.6
                    con.alpha = max(con.alpha, 0)
                    con.image.set_alpha(con.alpha)
                else:
                    self.screen.blit(con.image, con.rect)
            if (
                pygame.math.Vector2(con.rect.centerx, con.rect.centery).distance_to(
                    constants.CENTER
                )
                > constants.RANGE
            ):
                self.contacts.remove(con)
                del con
                logger.debug("Contact out of range, deleted.")

            if constants.DEBUG:
                pygame.draw.rect(
                    self.screen,
                    constants.RED,
                    pygame.Rect(
                        con.rect.left, con.rect.top, con.rect.width, con.rect.height
                    ),
                    2,
                )
