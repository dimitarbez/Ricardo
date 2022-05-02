import RPi.GPIO as GPIO
from gpio_pin_controller import GPIOPinController

class HeadlightsController(GPIOPinController):
    __headlights_pwm_frequency: 10000
    __headlights_pwm_duty_cycle: 25

    def __init__(self, headlights_pin: int = 36) -> None:
        super().__init__(headlights_pin)
        self.__headlights_pwm = GPIO.PWM(headlights_pin, self.__headlights_pwm_frequency)

    def turn_on(self):
        self.__headlights_pwm.start(self.__headlights_pwm_duty_cycle)

    def turn_off(self):
        self.__headlights_pwm.stop()