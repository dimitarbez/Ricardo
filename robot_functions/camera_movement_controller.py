from time import sleep
import RPi.GPIO as GPIO
from camera_movement_interface import CameraMovementInterface

class CameraMovementController(CameraMovementInterface):

    __servo1_duty_cycle: 6.5
    __servo2_duty_cycle: 7
    __cameraMoveIncrement: 0.1
    __servoMoveDelay: 0.05
    __servo1_pin: 38
    __servo2_pin: 40

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__servo1_pin, GPIO.OUT)
        GPIO.setup(self.__servo2_pin, GPIO.OUT)
        self.__servo1 = GPIO.PWM(self.__servo1_pin, 50)
        self.__servo2 = GPIO.PWM(self.__servo2_pin, 50)
        self.__servo1.start(self.__servo1_duty_cycle)
        self.__servo2.start(self.__servo2_duty_cycle)
        self.__disable_servos()

    def move_camera_up(self):
        self.__move_camera(self.__cameraMoveIncrement, 0)

    def move_camera_down(self):
        self.__move_camera(-self.__cameraMoveIncrement, 0)    

    def move_camera_left(self):
        self.__move_camera(0, self.__cameraMoveIncrement)    

    def move_camera_right(self):
        self.__move_camera(0, -self.__cameraMoveIncrement)    

    def center_camera(self):
        self.__change_servos_duty_cycle(6.5, 7)

    def __move_camera(self, pitch_change:float, yaw_change:float):
        self.__offset_servo_cycle(pitch_change, yaw_change)
        sleep(self.__servoMoveDelay)
        self.__disable_servos()

    def __offset_servo_cycle(self, servo1_offset:float, servo2_offset:float):

        new_servo1_duty_cycle = servo1_offset + self.__servo1_duty_cycle
        new_servo2_duty_cycle = servo2_offset + self.__servo2_duty_cycle

        if (new_servo1_duty_cycle <= 9 and new_servo2_duty_cycle <= 9.7) and (new_servo1_duty_cycle >= 2 and new_servo2_duty_cycle >= 4):
            self.__servo1_duty_cycle = new_servo1_duty_cycle
            self.__servo2_duty_cycle = new_servo2_duty_cycle
            self.__servo1.ChangeDutyCycle(self.__servo1_duty_cycle)
            self.__servo2.ChangeDutyCycle(self.__servo2_duty_cycle)

    def __change_servos_duty_cycle(self, new_servo1_duty_cycle: int, new_servo2_duty_cycle: int):

        self.__servo1_duty_cycle = new_servo1_duty_cycle
        self.__servo2_duty_cycle = new_servo2_duty_cycle
        self.__servo1.ChangeDutyCycle(self.__servo1_duty_cycle)
        self.__servo2.ChangeDutyCycle(self.__servo2_duty_cycle)
        
    def __disable_servos(self):
        self.__servo1.ChangeDutyCycle(0)
        self.__servo2.ChangeDutyCycle(0)