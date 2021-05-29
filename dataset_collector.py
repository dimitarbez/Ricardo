import cv2
import os
import time

cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height
cam.set
face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
# For each person, enter one numeric face id
face_id = input('\nenter integer user id for specific person: ')
num_of_images = int(input('\n enter how many images to take: '))

if num_of_images > 5000:
    raise Exception('Number of images too large!')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray)
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=20,
        minSize=(30, 30),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Save the captured image into the datasets folder
        cv2.imwrite("./dataset/user." + str(face_id) + '.' +
                    str(count) + ".jpg", gray[y:y+h, x:x+w])
        count += 1
        print('Image #' + str(count))

    cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= num_of_images:  # Take 30 face sample and stop video
        break
# Do a bit of cleanup
print(str(count) + ' images taken')
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
