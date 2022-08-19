import board
import digitalio
import adafruit_aw9523

i2c = board.I2C()


class ButtonMgr():
    def __init__(self):
        self.aw = adafruit_aw9523.AW9523(i2c)
        self.led_pin = self.aw.get_pin(0)
        self.button_pin = self.aw.get_pin(1)
        self.led_pin.switch_to_output(value=True)
        self.button_pin.direction = digitalio.Direction.INPUT


    def update(self):
        self.led_pin.value = self.button_pin.value
