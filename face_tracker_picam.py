# import required libraries
from motorcontroller import MotorController
import time
import cv2 as cv
import numpy as np

# if using the picamera, import those libraries as well
from picamera.array import PiRGBArray
from picamera import PiCamera

# point to the haar cascade file in the directory
cascPath = "haarcascade.xml"
faceCascade = cv.CascadeClassifier(cascPath)

# #start the camera and define settings
camera = PiCamera()
camera.resolution = (400, 300) #a smaller resolution means faster processing
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(400, 300))

side_borders_distance = 150
max_tracking_area = 2000
min_tracking_area = 1600

# give camera time to warm up
time.sleep(0.1)

# start video frame capture
# cap = cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 400)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 300)

motor_controller = MotorController()

# while True:
#     ret, image = cap.read()

for still in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # take the frame as an array, convert it to black and white, and look for facial features
    image = still.array
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv.CASCADE_SCALE_IMAGE
    )

    if len(faces) == 0:
    	motor_controller.stop()

    # for each face, draw a green rectangle around it and append to the image
    for(x, y, w, h) in faces:

        x_in_right = (x + w > image.shape[1] - side_borders_distance)
        x_in_left = (x < side_borders_distance)

        cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if x_in_left and not x_in_right:
            # within the left region
            left_motorspeed = ((x - side_borders_distance) * (-100) / (side_borders_distance))
            left_motorspeed = np.clip(left_motorspeed, 30, 80)
            print(left_motorspeed)
            motor_controller.setmotorspeed(left_motorspeed)
            motor_controller.movehardleft()
            print('left')

        elif x_in_right and not x_in_left:
            # within the right region
            right_motorspeed = (((x + w) - (image.shape[1] - side_borders_distance)) * 100) / side_borders_distance
            right_motorspeed = np.clip(right_motorspeed, 30, 80)
            print(right_motorspeed)
            motor_controller.setmotorspeed(right_motorspeed)
            motor_controller.movehardright()
            print('right')
			
        elif (x_in_left and x_in_right) or not (x_in_left and x_in_right):
            print('center')
            area = (w ** 2)
            print(area)
            if area > max_tracking_area:
            	motor_controller.setmotorspeed(50)
            	motor_controller.movebackward()
            elif area < min_tracking_area:
            	motor_controller.setmotorspeed(50)
            	motor_controller.moveforward()
            else:
            	motor_controller.stop()

		print('Motor speed:', motor_controller.motorspeed)


    # display the resulting image
    cv.line(image, (side_borders_distance, 0),
            (side_borders_distance, image.shape[0]), (0, 0, 255), 5)
    cv.line(image, (image.shape[1] - side_borders_distance, 0),
            (image.shape[1] - side_borders_distance, image.shape[0]), (0, 0, 255), 5)

    cv.imshow("Display", image)

    # clear the stream capture
    rawCapture.truncate(0)

    # set "q" as the key to exit the program when pressed
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        break
