import RPi.GPIO as GPIO

class MotorController:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)
        self.pwm1 = GPIO.PWM(8, 200)
        self.pwm2 = GPIO.PWM(10, 200)
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

    def movehardright(self):
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    def movehardleft(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    def stop(self):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
