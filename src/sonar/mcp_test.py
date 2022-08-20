from time import sleep

import board
import busio
from digitalio import Direction
from digitalio import Pull
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)

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

pin0 = mcp.get_pin(pin=0)
pin0.switch_to_input()
pin0.pull = Pull.UP


while True:
    print(f"Pin0: {pin0.value}")
    pin14.value = pin0.value
    pin15.value = True
    pin15.value = False
