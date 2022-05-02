import RPi.GPIO as GPIO
import curses
from motor_controller.motor_controller import MotorController
from robot_functions.camera_movement_controller import CameraMovementController
from robot_functions.buzzer_controller import BuzzerController
from robot_functions.headlights_controller import HeadlightsController
from robot_functions.laser_controller import LaserController
from robot_functions.camera_software_controller import CameraSoftwareController


if __name__ == '__main__':

    try:

        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)    

        motor_controller = MotorController()
        camera_movement_controller = CameraMovementController()
        buzzer_controller = BuzzerController()
        headlights_controller = HeadlightsController()
        laser_controller = LaserController()
        camera_software_controller = CameraSoftwareController()

        camera_software_controller.start_camera()

        while True:
            char = screen.getch()
            if char == ord('q'):
                motor_controller.stop()
                break
            elif char == ord('w'):            
                motor_controller.move_forward()
            elif char == ord('s'):            
                motor_controller.move_backward()
            elif char == ord('a'):            
                motor_controller.move_left()
            elif char == ord('d'):            
                motor_controller.move_right()
            elif char == ord('e'):            
                motor_controller.stop()
            elif char == ord('z'):            
                motor_controller.move_hard_left()
            elif char == ord('c'):            
                motor_controller.move_hard_right()
            elif char == ord('1'):
                motor_controller.set_motor_speed(20)
            elif char == ord('2'):
                motor_controller.set_motor_speed(40)
            elif char == ord('3'):
                motor_controller.set_motor_speed(60)
            elif char == ord('4'):
                motor_controller.set_motor_speed(80)
            elif char == ord('5'):
                motor_controller.set_motor_speed(100)
            elif char == ord(','):
                motor_controller.increase_motor_speed(5)
            elif char == ord('.'):
                motor_controller.decrease_motor_speed(5)
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
                camera_movement_controller.set_camera_move_speed(0.05)
                camera_software_controller.zoom_in()
            elif char == ord('-'):
                camera_movement_controller.set_camera_move_speed(0.1)
                camera_software_controller.zoom_out()
            elif char == ord('i'):
                laser_controller.turn_on()
            elif char == ord('o'):        
                laser_controller.turn_off()
            elif char == ord('t'):
                camera_software_controller.take_picture()

    except Exception as err:
        print(err)

    finally:
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        GPIO.cleanup()
