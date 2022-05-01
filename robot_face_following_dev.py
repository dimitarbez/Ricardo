# this is the main file for development and
# testing features features for the robot
# that later will be transfered to the
# face_tracker_picam.py script

# import required libraries
import cv2 as cv
from face_tracker.face_tracker import FaceTracker
from motor_controller.motor_speed_calculator import MotorSpeedCalculator


if __name__ == '__main__':
    # point to the haar cascade file in the directory
    cascPath = "./haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv.CascadeClassifier(cascPath)

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
    #time.sleep(0.1)

    # start video frame capture
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 400)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 300)

    face_tracker = FaceTracker()

    while cap.isOpened():

        ret, image = cap.read()
        if ret:

            face = face_tracker.get_face_from_image(image, faceCascade)
            if len(face) == 0:
                continue

            face_x = face[0]
            face_y = face[1]
            face_width = face[2]
            face_height = face[3]

            object_in_right_area = face_tracker.is_face_in_right_region(face, image)
            object_in_left_area = face_tracker.is_face_in_left_region(face)

            cv.rectangle(image, (face_x, face_y), (face_x+face_width, face_y+face_height), tracked_face_color, 2)

            # within the left region
            if object_in_left_area and not object_in_right_area:
                # interpolate motor speed from left side border to left edge of screen
                left_motorspeed = MotorSpeedCalculator.calculate_left_motor_speed(face_x, face_tracker.rotation_region_size)
                print(left_motorspeed)
                print('left')

            # within the right region
            elif object_in_right_area and not object_in_left_area:
                # interpolate motor speed from right side border to right edge of screen
                right_motorspeed = MotorSpeedCalculator.calculate_right_motor_speed(face_x, face_width, image.shape[1], face_tracker.rotation_region_size)
                print(right_motorspeed)
                print('right')

            elif (object_in_left_area and object_in_right_area) or not (object_in_left_area and object_in_right_area):
                print('center')
                print(face_width)
                if face_width > max_face_tracking_width:
                    print('move backward')
                elif face_width < min_face_tracking_width:
                    print('move forward')
                else:
                    print('stop')

            # draw side borders
            cv.line(image, (side_borders_distance, 0), (side_borders_distance, image.shape[0]), side_border_color, 5)
            cv.line(image, (image.shape[1] - side_borders_distance, 0), (image.shape[1] - side_borders_distance, image.shape[0]), side_border_color, 5)

            # display the resulting image
            cv.imshow("Display", image)

            # set "q" as the key to exit the program when pressed
            key = cv.waitKey(1) & 0xFF
            if key == ord("q"):
                break
