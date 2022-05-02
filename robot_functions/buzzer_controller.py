import RPi.GPIO as GPIO
from gpio_pin_controller import GPIOPinController


class BuzzerController(GPIOPinController):
    __buzzer_pwm_frequency: int = 1000
    __buzzer_pwm_duty_cycle: int = 50

    def __init__(self, buzzer_pin: int = 37) -> None:
        super().__init__(buzzer_pin)
        self.__buzzer_pwm = GPIO.PWM(buzzer_pin, self.__buzzer_pwm_frequency)

    def turn_on(self):
        self.__buzzer_pwm.start(self.__buzzer_pwm_duty_cycle)

    def turn_off(self):
        self.__buzzer_pwm.stop()