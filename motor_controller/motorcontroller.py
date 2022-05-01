import RPi.GPIO as GPIO

class MotorController:

    motor1_pwm_pin = 8
    motor2_pwm_pin = 10
    motor_in1 = 5
    motor_in2 = 11
    motor_in3 = 13
    motor_in4 = 15

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.motor1_pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor2_pwm_pin, GPIO.OUT)
        GPIO.setup(self.MotorController.motor_in1, GPIO.OUT)
        GPIO.setup(self.motor_in2, GPIO.OUT)
        GPIO.setup(self.motor_in3, GPIO.OUT)
        GPIO.setup(self.motor_in4, GPIO.OUT)
        self.pwm1 = GPIO.PWM(self.motor1_pwm_pin, 200)
        self.pwm2 = GPIO.PWM(self.motor2_pwm_pin, 200)
        self.motorspeed = 50
        self.pwm1.start(self.motorspeed)
        self.pwm2.start(self.motorspeed)
        self.stop()

    def offsetmotorspeed(self, speedoffset):
        if speedoffset > 0:
            if self.motorspeed < 100:
                self.motorspeed = self.motorspeed + speedoffset
        elif speedoffset < 0:
            if self.motorspeed > 0:
                self.motorspeed = self.motorspeed + speedoffset
        self.pwm1.ChangeDutyCycle(self.motorspeed)
        self.pwm2.ChangeDutyCycle(self.motorspeed)
        
    def setmotorspeed(self, speed):
        self.motorspeed = speed
        self.pwm1.ChangeDutyCycle(self.motorspeed)
        self.pwm2.ChangeDutyCycle(self.motorspeed)

    def moveforward(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.HIGH)

    def movebackward(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.HIGH)
        GPIO.output(self.motor_in3, GPIO.HIGH)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def moveleft(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.HIGH)

    def moveright(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def movehardleft(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.HIGH)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.HIGH)

    def movehardright(self):
        GPIO.output(self.motor_in1, GPIO.HIGH)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.HIGH)
        GPIO.output(self.motor_in4, GPIO.LOW)

    def stop(self):
        GPIO.output(self.motor_in1, GPIO.LOW)
        GPIO.output(self.motor_in2, GPIO.LOW)
        GPIO.output(self.motor_in3, GPIO.LOW)
        GPIO.output(self.motor_in4, GPIO.LOW)
