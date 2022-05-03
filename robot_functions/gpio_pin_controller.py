import RPi.GPIO as GPIO
from abc import ABC, abstractmethod


class GPIOPinController(ABC):

    _gpio_pin: int

    def __init__(self, gpio_pin) -> None:
        super().__init__()
        self._gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._gpio_pin, GPIO.OUT)
        
    def __del__(self):
        GPIO.cleanup()

    @abstractmethod
    def turn_on():
        pass

    @abstractmethod
    def turn_off():
        pass