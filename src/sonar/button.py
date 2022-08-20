# from cgi import print_arguments
# import RPi.GPIO as GPIO
from loguru import logger
import board
import busio
from digitalio import Direction
from digitalio import Pull
from digitalio import DigitalInOut
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_debouncer import Debouncer

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)


class ButtonMgr():
    def __init__(self):
        # Pins 0-7 on the right side of the MCP23017
        pin0 = mcp.get_pin(pin=0)
        pin0.switch_to_input()
        pin0.pull = Pull.UP
        but0 = Debouncer(pin0)

        pin1 = mcp.get_pin(pin=1)
        pin1.switch_to_input()
        pin1.pull = Pull.UP
        but1 = Debouncer(pin1)

        pin2 = mcp.get_pin(pin=2)
        pin2.switch_to_input()
        pin2.pull = Pull.UP
        but2 = Debouncer(pin2)

        pin3 = mcp.get_pin(pin=3)
        pin3.switch_to_input()
        pin3.pull = Pull.UP
        but3 = Debouncer(pin3)

        pin4 = mcp.get_pin(pin=4)
        pin4.switch_to_input()
        pin4.pull = Pull.UP
        but4 = Debouncer(pin4)

        pin5 = mcp.get_pin(pin=5)
        pin5.switch_to_input()
        pin5.pull = Pull.UP
        but5 = Debouncer(pin5)

        pin6 = mcp.get_pin(pin=6)
        pin6.switch_to_input()
        pin6.pull = Pull.UP
        but6 = Debouncer(pin6)

        pin7 = mcp.get_pin(pin=7)
        pin7.switch_to_input()
        pin7.pull = Pull.UP
        but7 = Debouncer(pin7)

        pinGrn = DigitalInOut(board.D23)
        butGrn = Debouncer(pinGrn)

        pinRed = DigitalInOut(board.D24)
        butRed = Debouncer(pinRed)

        GreenLed = DigitalInOut(board.D18)
        GreenLed.direction = Direction.OUTPUT

        RedLed = DigitalInOut(board.D25)
        RedLed.direction = Direction.OUTPUT

        # Pins 8-15 on the left side of the MCP23017
        pin8 = mcp.get_pin(pin=8)
        pin8.direction = Direction.OUTPUT
        pin9 = mcp.get_pin(pin=9)
        pin9.direction = Direction.OUTPUT
        pin10 = mcp.get_pin(pin=10)
        pin10.direction = Direction.OUTPUT
        pin11 = mcp.get_pin(pin=11)
        pin11.direction = Direction.OUTPUT
        pin12 = mcp.get_pin(pin=12)
        pin12.direction = Direction.OUTPUT
        pin13 = mcp.get_pin(pin=13)
        pin13.direction = Direction.OUTPUT
        pin14 = mcp.get_pin(pin=14)
        pin14.direction = Direction.OUTPUT
        pin15 = mcp.get_pin(pin=15)
        pin15.direction = Direction.OUTPUT

        self.inputs = [but0, but1, but2, but3, but4,
                       but5, but6, but7, butGrn, butRed, ]
        self.outputs = [pin8, pin9, pin10, pin11, pin12,
                        pin13, pin14, pin15, GreenLed, RedLed]

        self.ping_buttons = [(butGrn, GreenLed, 8), (butRed, RedLed, 9), ]
        self.animal_buttons = [
            (but0, pin8, 0), (but1, pin9, 1), (but2, pin10, 2), (but3, pin11, 3), ]
        self.message_buttons = [
            (but4, pin12, 4), (but5, pin13, 5), (but6, pin14, 6), (but7, pin15, 7), ]

    def update(self):
        changes = []
        for button, led, number in self.ping_buttons:
            button.update()
            if button.fell:
                logger.debug(f"Input {number} fell.")
                changes.append(number)
                led.value = False
            if button.rose:
                led.value = True
        return changes
