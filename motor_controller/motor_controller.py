import RPi.GPIO as GPIO
import numpy as np


class MotorController:

    motor1_pwm_pin: 8
    motor2_pwm_pin: 10
    motor_in1: 5
    motor_in2: 11
    motor_in3: 13
    motor_in4: 15
    motor_speed: 50

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.motor1_pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor2_pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)
        GPIO.setup(self.motor_in3, GPIO.OUT)
        GPIO.setup(self.motor_in4, GPIO.OUT)
        self.motor1_pwm = GPIO.PWM(self.motor1_pwm_pin, 200)
        self.motor2_pwm = GPIO.PWM(self.motor2_pwm_pin, 200)
        self.motor1_pwm.start(self.motor_speed)
        self.motor2_pwm.start(self.motor_speed)
        self.stop()

    def increase_motor_speed(self, speed_offset):
        self.__offset_motor_speed(speed_offset)

    def decrease_motor_speed(self, speed_offset):
        self.__offset_motor_speed(-speed_offset)
        
    def set_motor_speed(self, speed: int):
        self.motor_speed = np.clip(speed, 0, 100)
        self.motor1_pwm.ChangeDutyCycle(self.motor_speed)
        self.motor2_pwm.ChangeDutyCycle(self.motor_speed)

    def move_forward(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.HIGH)

    def move_backward(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.HIGH)
        GPIO.output(self.motor_in3, GPIO.HIGH)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def move_left(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.HIGH)

    def move_right(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def move_hard_left(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.HIGH)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.HIGH)

    def move_hard_right(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.HIGH)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def stop(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def __offset_motor_speed(self, speed_offset: int):
        self.motor_speed = np.clip(self.motor_speed + speed_offset, 0, 100)
        self.motor1_pwm.ChangeDutyCycle(self.motor_speed)
        self.motor2_pwm.ChangeDutyCycle(self.motor_speed)