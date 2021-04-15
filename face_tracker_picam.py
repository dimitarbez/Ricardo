#import required libraries
from motorcontroller import MotorController
import time
import cv2 as cv
import numpy as np
from motorcontroller import MotorController

#if using the picamera, import those libraries as well
from picamera.array import PiRGBArray
from picamera import PiCamera

#point to the haar cascade file in the directory
cascPath = "haarcascade.xml"
faceCascade = cv.CascadeClassifier(cascPath)

#start the camera and define settings
camera = PiCamera()
camera.resolution = (320, 240) #a smaller resolution means faster processing
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

#give camera time to warm up
time.sleep(0.1)

# start video frame capture
#cap = cv.VideoCapture(0)
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

motor_controller = MotorController()

#while True:
	#ret, image = cap.read()

for still in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# take the frame as an array, convert it to black and white, and look for facial features
	image = still.array
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
		image,
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize=(30, 30),
		flags = cv.CASCADE_SCALE_IMAGE
	)

	#for each face, draw a green rectangle around it and append to the image
	for(x,y,w,h) in faces:
		cv.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
		if x < 50:
			# within the left region
			print('Motor speed:', (100 - x)/2)
			motor_controller.setmotorspeed((100 - x)/2)
			motor_controller.movehardleft()
			print('left')
		elif x + w > image.shape[1] - 50:
			# within the right region
			print('Motor speed:', ((x + w) + 100 - image.shape[1])/2)
			motor_controller.setmotorspeed(((x + w) + 100 - image.shape[1])/2)
			motor_controller.movehardright()
			print('right')
		else:
			print('center')
			area = (w ** 2)
			print(area)
			if area > 3000:
				motor_controller.setmotorspeed(50)
				motor_controller.movebackward()
			elif area < 2000:
				motor_controller.setmotorspeed(50)
				motor_controller.moveforward()
			else:
				motor_controller.stop()
						
		#time.sleep(0.2)
		#print((x + w) ** 2)
		# 50000
		# 30000

	#motor_controller.stop()

	#display the resulting image
	cv.imshow("Display", image)

	# clear the stream capture
	rawCapture.truncate(0)

	#set "q" as the key to exit the program when pressed
	key = cv.waitKey(1) & 0xFF
	if key == ord("q"):
		break
