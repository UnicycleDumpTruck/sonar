"""Main program file for sonar interface."""
import time
from os import uname

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

# import contact
import arc
import constants
import snd

install(show_locals=True)

architecture = uname()[4][:3]
print(f"Running on architecture: {architecture}")
if architecture.lower() == "arm":
    import board
    import digitalio
    import adafruit_aw9523
    ON_RPI = True
else:
    ON_RPI = False

if ON_RPI:
    i2c = board.I2C()
    aw = adafruit_aw9523.AW9523(i2c)
    led_pin = aw.get_pin(0)
    button_pin = aw.get_pin(1)
    led_pin.switch_to_output(value=True)
    button_pin.direction = digitalio.Direction.INPUT

pygame.init()


# pinging = False


def main() -> None:
    """Sonar."""

    # Set up the drawing window
    # screen = pygame.display.set_mode([BOX, BOX])
    screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
    arc_mgr = arc.ArcMgr(screen)
    pygame.mouse.set_visible(False)
    # Run until quit
    running = True

    while running:
        if ON_RPI:
            led_pin.value = button_pin.value
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    start_ping(arc_mgr, constants.RED)
                if event.key == K_g:
                    start_ping(arc_mgr, constants.GREEN)
                if event.key == K_b:
                    start_ping(arc_mgr, constants.BLACK)
                if event.key == K_t:
                    arc_mgr.rand_contact()
                    # angle = randint(0, 359)
                    # # radius = randint(100, HBOX)
                    # radius = HBOX - 40
                    # x = radius * math.cos(angle) + HBOX
                    # y = radius * math.sin(angle) + HBOX
                    # logger.debug(f"Random contact at {x,y}")
                    # arc_mgr.contacts.append(Contact(x, y))

                if event.key == K_ESCAPE:
                    running = False

        # Fill the background with blue
        screen.fill(constants.BG_BLUE)

        draw_reticle(screen)
        arc_mgr.draw()

        # Flip the display
        pygame.display.flip()

        time.sleep(0.01)

    # Running false, time to quit.
    pygame.quit()


def draw_reticle(scrn):
    # Outer White Circle
    pygame.draw.circle(scrn, constants.WHITE, constants.CENTER, constants.BOX // 2 - constants.RWT)

    # Inner Blue Circle
    pygame.draw.circle(scrn, constants.BG_BLUE, constants.CENTER, constants.BOX // 2 - (constants.RWT * 2))

    # Reticle crossing lines
    pygame.draw.rect(scrn, constants.WHITE, constants.HRETL)
    pygame.draw.rect(scrn, constants.WHITE, constants.VRETL)

    # Central Blanking circle
    pygame.draw.circle(scrn, constants.BG_BLUE, constants.CENTER, 60)  # RCNT + RWT)

    # Central circle
    # pygame.draw.circle(scrn, WHITE, CENTER, RCNT)

    scrn.blit(constants.SUB_ICON, constants.SUB_LOCATION)


def start_ping(arc_mgr, color=constants.RED, sound=snd.ping):
    # if pinging and constants.EXCLUSIVE_PING:
    #     logger.debug("Ping requested, but already pinging.")
    #     return
    # else:
    # logger.debug("Commencing ping.")
    # pinging = True
    pygame.mixer.Sound.play(sound)
    # logger.debug(f"Number of channels: {sound.get_num_channels()}")
    arc_mgr.arcs.extend(arc_mgr.arcs_from_xy(
        arc_mgr.listener, constants.HBOX, constants.HBOX, color, 'ping_a'))

if __name__ == "__main__":
    main()
