import RPi.GPIO as GPIO

motor1_pwm_pin = 8
motor2_pwm_pin = 10
motor_in1 = 5
motor_in2 = 11
motor_in3 = 13
motor_in4 = 15

class MotorController:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(motor1_pwm_pin, GPIO.OUT)
        GPIO.setup(motor2_pwm_pin, GPIO.OUT)
        GPIO.setup(motor_in1, GPIO.OUT)
        GPIO.setup(motor_in2, GPIO.OUT)
        GPIO.setup(motor_in3, GPIO.OUT)
        GPIO.setup(motor_in4, GPIO.OUT)
        self.pwm1 = GPIO.PWM(motor1_pwm_pin, 200)
        self.pwm2 = GPIO.PWM(motor2_pwm_pin, 200)
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
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.HIGH)
        GPIO.output(motor_in3, GPIO.HIGH)
        GPIO.output(motor_in4, GPIO.LOW)

    def movebackward(self):
        GPIO.output(motor_in1, GPIO.HIGH)
        GPIO.output(motor_in2, GPIO.LOW)
        GPIO.output(motor_in3, GPIO.LOW)
        GPIO.output(motor_in4, GPIO.HIGH)

    def moveleft(self):
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.HIGH)
        GPIO.output(motor_in3, GPIO.LOW)
        GPIO.output(motor_in4, GPIO.LOW)

    def moveright(self):
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.LOW)
        GPIO.output(motor_in3, GPIO.HIGH)
        GPIO.output(motor_in4, GPIO.LOW)

    def movehardright(self):
        GPIO.output(motor_in1, GPIO.HIGH)
        GPIO.output(motor_in2, GPIO.LOW)
        GPIO.output(motor_in3, GPIO.HIGH)
        GPIO.output(motor_in4, GPIO.LOW)

    def movehardleft(self):
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.HIGH)
        GPIO.output(motor_in3, GPIO.LOW)
        GPIO.output(motor_in4, GPIO.HIGH)

    def stop(self):
        GPIO.output(motor_in1, GPIO.LOW)
        GPIO.output(motor_in2, GPIO.LOW)
        GPIO.output(motor_in3, GPIO.LOW)
        GPIO.output(motor_in4, GPIO.LOW)
