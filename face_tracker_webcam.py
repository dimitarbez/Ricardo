# this is the main file for development and
# testing features features for the robot
# that later will be transfered to the
# face_tracker_picam.py script

# import required libraries
import time
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from numpy.lib.type_check import imag

# point to the haar cascade file in the directory
cascPath = "./haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascPath)

# set the distance between the edge of the screen
# and the borders that trigger robot rotation
side_borders_distance = 150

# face tracking area thresholds are used for forward/backward movement of the robot
# max square area threshold for face tracking
max_face_tracking_area = 2000
# min square area threshold for face tracking
min_face_tracking_area = 1600

tracked_face_color = (0, 255, 0)
side_border_color = (0, 0, 255)

# give camera time to warm up
time.sleep(0.1)

# start video frame capture
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 300)

plt.ion()

while True:
    ret, image = cap.read()
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv.CASCADE_SCALE_IMAGE
    )

    if len(faces) == 0:
        print('no faces found')

    # for each face, draw a green rectangle around it and append to the image
    # x-pos, y-pos, width, height
    for(x, y, w, h) in faces:

        # formula for object position
        object_in_right_area = (x + w > image.shape[1] - side_borders_distance)
        object_in_left_area = (x < side_borders_distance)

        cv.rectangle(image, (x, y), (x+w, y+h), tracked_face_color, 2)

        # within the left region
        if object_in_left_area and not object_in_right_area:
            # interpolate motor speed from left side border to left edge of screen
            left_motorspeed = ((x - side_borders_distance) * (-100) / (side_borders_distance))
            left_motorspeed = np.clip(left_motorspeed, 35, 80)
            print(left_motorspeed)
            print('left')

        # within the right region
        elif object_in_right_area and not object_in_left_area:
            # interpolate motor speed from right side border to right edge of screen
            right_motorspeed = (((x + w) - (image.shape[1] - side_borders_distance)) * 100) / side_borders_distance
            right_motorspeed = np.clip(right_motorspeed, 35, 80)
            print(right_motorspeed)
            print('right')

        elif (object_in_left_area and object_in_right_area) or not (object_in_left_area and object_in_right_area):
            print('center')
            area = (w ** 2)
            print(area)
            if area > max_face_tracking_area:
                print('move backward')
            elif area < min_face_tracking_area:
                print('move forward')
            else:
                print('stop')

    # draw side borders
    cv.line(image, (side_borders_distance, 0), (side_borders_distance, image.shape[0]), side_border_color, 5)
    cv.line(image, (image.shape[1] - side_borders_distance, 0), (image.shape[1] - side_borders_distance, image.shape[0]), side_border_color, 5)

    # display the resulting image
    #cv.imshow("Display", image)


    plt.imshow(gray, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
    plt.pause(0.05)

    # set "q" as the key to exit the program when pressed
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        plt.ioff()
        break
