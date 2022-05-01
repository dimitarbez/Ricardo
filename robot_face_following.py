# import required libraries
from motor_controller.motorcontroller import MotorController
import time
import cv2 as cv
from face_tracker.face_tracker import FaceTracker
from motor_controller.motor_speed_calculator import MotorSpeedCalculator

# if using the picamera, import those libraries as well
from picamera.array import PiRGBArray
from picamera import PiCamera

# point to the haar cascade file in the directory
cascPath = "./haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascPath)

# #start the camera and define settings
camera = PiCamera()
camera.resolution = (400, 300)  # a smaller resolution means faster processing
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(400, 300))

# set the distance between the edge of the screen
# and the borders that trigger robot rotation
side_borders_distance = 150

# face tracking area thresholds are used for forward/backward movement of the robot
# max square area threshold for face tracking
max_face_tracking_width = 150
# min square area threshold for face tracking
min_face_tracking_width = 120

tracked_face_color = (0, 255, 0)
side_border_color = (0, 0, 255)

# give camera time to warm up
time.sleep(0.1)

motor_controller = MotorController()
face_tracker = FaceTracker()

for still in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # take the frame as an array, convert it to black and white, and look for facial features
    image = still.array
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    face = face_tracker.get_face_from_image(gray, faceCascade)
    if len(face) == 0:
        continue

    face_x = face[0]
    face_y = face[1]
    face_width = face[2]
    face_height = face[3]

    # formula for object position
    object_in_right_area = face_tracker.is_face_in_right_region(face, image)
    object_in_left_area = face_tracker.is_face_in_left_region(face)

    cv.rectangle(image, (face_x, face_y), (face_x+face_width, face_y+face_height), tracked_face_color, 2)

    # within the left region
    if object_in_left_area and not object_in_right_area:
        # interpolate motor speed from left side border to left edge of screen
        left_motorspeed = MotorSpeedCalculator.calculate_left_motor_speed(face_x, face_tracker.rotation_region_size)
        motor_controller.setmotorspeed(left_motorspeed)
        motor_controller.movehardleft()
        print('left')

    # within the right region
    elif object_in_right_area and not object_in_left_area:
        # interpolate motor speed from right side border to right edge of screen
        right_motorspeed = MotorSpeedCalculator.calculate_right_motor_speed(face_x, face_width, image.shape[1])
        motor_controller.setmotorspeed(right_motorspeed)
        motor_controller.movehardright()
        print('right')

    elif (object_in_left_area and object_in_right_area) or not (object_in_left_area and object_in_right_area):
        print('center')
        if face_width > max_face_tracking_width:
            print('move backward')
            motor_controller.setmotorspeed(50)
            motor_controller.movebackward()
        elif face_width < min_face_tracking_width:
            print('move forward')
            motor_controller.setmotorspeed(50)
            motor_controller.moveforward()
        else:
            motor_controller.stop()
            print('stop')

    # draw side borders
    cv.line(image, (side_borders_distance, 0),
            (side_borders_distance, image.shape[0]), side_border_color, 5)
    cv.line(image, (image.shape[1] - side_borders_distance, 0),
            (image.shape[1] - side_borders_distance, image.shape[0]), side_border_color, 5)

    # display the resulting image
    cv.imshow("Display", image)

    # clear the stream capture
    rawCapture.truncate(0)

    # set "q" as the key to exit the program when pressed
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break
