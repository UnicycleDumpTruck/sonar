from cgi import print_arguments
# import RPi.GPIO as GPIO
import board
import busio
from digitalio import Direction
from digitalio import Pull
from digitalio import DigitalInOut
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)


class ButtonMgr():
    def __init__(self):

        pin0 = mcp.get_pin(pin=0)
        pin0.switch_to_input()
        pin0.pull = Pull.UP
        pin1 = mcp.get_pin(pin=1)
        pin1.switch_to_input()
        pin1.pull = Pull.UP
        pin2 = mcp.get_pin(pin=2)
        pin2.switch_to_input()
        pin2.pull = Pull.UP
        pin3 = mcp.get_pin(pin=3)
        pin3.switch_to_input()
        pin3.pull = Pull.UP
        pin4 = mcp.get_pin(pin=4)
        pin4.switch_to_input()
        pin4.pull = Pull.UP
        pin5 = mcp.get_pin(pin=5)
        pin5.switch_to_input()
        pin5.pull = Pull.UP
        pin6 = mcp.get_pin(pin=6)
        pin6.switch_to_input()
        pin6.pull = Pull.UP
        pin7 = mcp.get_pin(pin=7)
        pin7.switch_to_input()
        pin7.pull = Pull.UP

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

        pinGrn = DigitalInOut(board.D23)
        pinRed = DigitalInOut(board.D24)

        self.inputs = [pin0, pin1, pin2, pin3, pin4,
                       pin5, pin6, pin7, pinGrn, pinRed, ]
        self.outputs = [pin8, pin9, pin10, pin11, pin12, pin13, pin14, pin15, ]

    def update(self):
        for i, button in enumerate(self.inputs):
            if i < 8:
                self.outputs[i].value = button.value
