import RPi.GPIO as GPIO
import curses
from datetime import datetime
from picamera import PiCamera
from motor_controller.motor_controller import MotorController
from robot_functions.camera_movement_controller import CameraMovementController
from robot_functions.buzzer_controller import BuzzerController
from robot_functions.headlights_controller import HeadlightsController
from robot_functions.laser_controller import LaserController

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)    

try:

    motor_controller = MotorController()
    camera_movement_controller = CameraMovementController()
    buzzer_controller = BuzzerController()
    headlights_controller = HeadlightsController()
    laser_controller = LaserController()

    camera = PiCamera()
    camera.rotation = 0
    camera.start_preview(fullscreen=False, window=(200,-100,600,800))
    
    while True:
        char = screen.getch()
        if char == ord('q'):
            motor_controller.stop()
            break
        elif char == ord('w'):            
            motor_controller.moveforward()
        elif char == ord('s'):            
            motor_controller.movebackward()
        elif char == ord('a'):            
            motor_controller.moveleft()
        elif char == ord('d'):            
            motor_controller.moveright()
        elif char == ord('e'):            
            motor_controller.stop()
        elif char == ord('z'):            
            motor_controller.movehardleft()
        elif char == ord('c'):            
            motor_controller.movehardright()
        elif char == ord('1'):
            motor_controller.setmotorspeed(20)
        elif char == ord('2'):
            motor_controller.setmotorspeed(40)
        elif char == ord('3'):
            motor_controller.setmotorspeed(60)
        elif char == ord('4'):
            motor_controller.setmotorspeed(80)
        elif char == ord('5'):
            motor_controller.setmotorspeed(100)
        elif char == ord(','):
            motor_controller.offsetmotorspeed(-5)
        elif char == ord('.'):
            motor_controller.offsetmotorspeed(+5)
        elif char == ord('h'):
            buzzer_controller.turn_on()
        elif char == ord('j'):
            buzzer_controller.turn_off()
        elif char == ord('l'):
            headlights_controller.turn_on()
        elif char == ord(';'):
            headlights_controller.turn_off()
        elif char == ord('0'):
            camera_movement_controller.center_camera()
        elif char == curses.KEY_UP:
            camera_movement_controller.move_camera_up()
        elif char == curses.KEY_DOWN:
            camera_movement_controller.move_camera_down()
        elif char == curses.KEY_RIGHT:
            camera_movement_controller.move_camera_right()
        elif char == curses.KEY_LEFT:
            camera_movement_controller.move_camera_left()
        elif char == ord('+'):
            cameraMoveIncrement = 0.05
            camera.zoom = (0.25, 0.25, 0.5, 0.5)
        elif char == ord('-'):
            cameraMoveIncrement = 0.1
            camera.zoom = (0, 0, 1, 1)
        elif char == ord('i'):
            laser_controller.turn_on()
        elif char == ord('o'):        
            laser_controller.turn_off()
        elif char == ord('t'):
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y-%H%M%S")
            camera.capture('/home/pi/Desktop/RobotImages/robot_%s.jpg' % dt_string)
    
finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    camera.stop_preview()
    GPIO.cleanup()
