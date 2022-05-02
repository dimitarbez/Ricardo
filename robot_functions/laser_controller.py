import RPi.GPIO as GPIO
from gpio_pin_controller import GPIOPinController


class LaserController(GPIOPinController):
    
    def __init__(self, laser_pin: int = 32) -> None:
        super().__init__(laser_pin)

    def turn_on(self):
        GPIO.output(self._gpio_pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self._gpio_pin, GPIO.LOW)