import RPi.GPIO as GPIO

class MotorController:

    pwmfreq = 200

    def __init__(self):
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)
        self.pwm1 = GPIO.PWM(8, pwmfreq)
        self.pwm2 = GPIO.PWM(10, pwmfreq)
        self.motorSpeed = 50
        pwm1.start(motorSpeed)
        pwm2.start(motorSpeed)

    def offsetmotorspeed(self, speed):
        if self.motorSpeed < 100 and self.motorSpeed > 0:
            self.motorSpeed = self.motorSpeed + speed

    def setmotorspeed(self, speed):
        self.motorSpeed = speed
        self.pwm1.ChangeDutyCycle(motorSpeed)
        self.pwm2.ChangeDutyCycle(motorSpeed)

    def moveforward(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    def movebackward(self):
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    def moveleft(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)

    def moveright(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    def movehardleft(self):
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    def movehardright(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    def stop(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
