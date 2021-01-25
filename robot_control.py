import RPi.GPIO as GPIO
import curses
from datetime import datetime
from picamera import PiCamera
from time import sleep

pwmOffset = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

GPIO.setup(37, GPIO.OUT)

pwm1 = GPIO.PWM(8, 200)
pwm2 = GPIO.PWM(10, 200)
ledLights = GPIO.PWM(36, 5000)
servo1 = GPIO.PWM(38, 50)
servo2 = GPIO.PWM(40, 50)

pwmHorn = GPIO.PWM(37, 1000)

servo1DutyCycle = 6.5
servo2DutyCycle = 7

cameraMoveIncrement = 0.1
servoMoveDelay = 0.05

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)    

motorSpeed = 100

def changeMotorSpeed(speedPerc):
    global motorSpeed
    motorSpeed = speedPerc
    pwm1.ChangeDutyCycle(motorSpeed+pwmOffset)
    pwm2.ChangeDutyCycle(motorSpeed)

def offsetServoCycle(motor1, motor2):
    global servo1DutyCycle
    global servo2DutyCycle
    motorOffset1 = motor1+servo1DutyCycle
    motorOffset2 = motor2+servo2DutyCycle

    if (motorOffset1 <= 9 and motorOffset2 <= 9.7) and (motorOffset1 >= 2 and motorOffset2 >= 4) :
        servo1DutyCycle = servo1DutyCycle + motor1
        servo2DutyCycle = servo2DutyCycle + motor2

        servo1.ChangeDutyCycle(servo1DutyCycle)
        servo2.ChangeDutyCycle(servo2DutyCycle)

def changeServoCycle(motor1, motor2):
    global servo1DutyCycle
    global servo2DutyCycle
    servo1DutyCycle = motor1
    servo2DutyCycle = motor2
    servo1.ChangeDutyCycle(servo1DutyCycle)
    servo2.ChangeDutyCycle(servo2DutyCycle)
    
def disableServos():
    servo1.ChangeDutyCycle(0)
    servo2.ChangeDutyCycle(0)

try:
    pwm1.start(motorSpeed)
    pwm2.start(motorSpeed)


    

    servo1.start(servo1DutyCycle)
    servo2.start(servo2DutyCycle)
    disableServos()
    
    camera = PiCamera()
    camera.rotation = 0

    camera.start_preview(fullscreen=False, window=(200,-100,600,800))

    
    while True:
        char = screen.getch()
        if char == ord('q'):
            GPIO.output(5, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
            break
        elif char == ord('w'):            
            GPIO.output(5, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(15, GPIO.LOW)
        elif char == ord('s'):            
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.HIGH)
        elif char == ord('a'):            
            GPIO.output(5, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
        elif char == ord('d'):            
            GPIO.output(5, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(15, GPIO.LOW)    
        elif char == ord('e'):            
            GPIO.output(5, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
        elif char == ord('z'):            
            GPIO.output(5, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.HIGH)
        elif char == ord('c'):            
            GPIO.output(5, GPIO.HIGH)
            GPIO.output(11, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(15, GPIO.LOW)    
        elif char == ord('1'):
            changeMotorSpeed(20)            
        elif char == ord('2'):
            changeMotorSpeed(40)
        elif char == ord('3'):
            changeMotorSpeed(60)
        elif char == ord('4'):
            changeMotorSpeed(80)
        elif char == ord('5'):
            changeMotorSpeed(100)
        elif char == ord(','):
            if motorSpeed > 0:
                motorSpeed = motorSpeed - 2
                changeMotorSpeed(motorSpeed)
        elif char == ord('.'):
            if motorSpeed < 100:
                motorSpeed = motorSpeed + 2
                changeMotorSpeed(motorSpeed)
        elif char == ord('h'):
            pwmHorn.start(50)
        elif char == ord('j'):
            pwmHorn.stop()
        elif char == ord('l'):
            ledLights.start(25)
        elif char == ord(';'):
            ledLights.stop()
        elif char == ord('0'):
            changeServoCycle(6.5, 7)
            sleep(0.2)            
            disableServos()
        elif char == curses.KEY_UP:
            offsetServoCycle(cameraMoveIncrement, 0)      
            sleep(servoMoveDelay)
            disableServos()
        elif char == curses.KEY_DOWN:
            offsetServoCycle(-cameraMoveIncrement, 0)      
            sleep(servoMoveDelay)
            disableServos()
        elif char == curses.KEY_RIGHT:
            offsetServoCycle(0, -cameraMoveIncrement)      
            sleep(servoMoveDelay)
            disableServos()
        elif char == curses.KEY_LEFT:
            offsetServoCycle(0, cameraMoveIncrement)      
            sleep(servoMoveDelay)
            disableServos()
        elif char == ord('+'):
            cameraMoveIncrement = 0.05
            camera.zoom = (0.25, 0.25, 0.5, 0.5)
        elif char == ord('-'):
            cameraMoveIncrement = 0.1
            camera.zoom = (0, 0, 1, 1)
        elif char == ord('i'):
            GPIO.output(32, GPIO.HIGH)
        elif char == ord('o'):        
            GPIO.output(32, GPIO.LOW)
        elif char == ord('t'):
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y-%H%M%S")
            camera.capture('/home/pi/Desktop/RobotImages/robot_%s.jpg' % dt_string)
    
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    camera.stop_preview()
    GPIO.cleanup()