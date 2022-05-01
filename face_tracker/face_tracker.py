import cv2 as cv


class FaceTracker:

    tracked_face_color = (0, 255, 0)
    side_border_color = (0, 0, 255)
    motor_speed_clipping = (35,80)

    def __init__(
            self,
            upper_facewidth_threshold=2000,
            lower_facewidth_threshold=1600,
            rotation_region_size = 150
        ) -> None:
        # set the distance between the edge of the screen
        # and the borders that trigger robot rotation
        self.rotation_region_size = rotation_region_size
        # face tracking area thresholds are used for forward/backward movement of the robot
        # max square area threshold for face tracking
        self.upper_facewidth_threshold = upper_facewidth_threshold
        # min square area threshold for face tracking
        self.lower_facewidth_threshold = lower_facewidth_threshold


    def get_face_from_image(self, image, face_cascade):
        faces = face_cascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv.CASCADE_SCALE_IMAGE
        )

        if len(faces) == 0:
            return []

        return faces[0]


    def is_face_in_left_region(self, face) -> bool:
        face_x = face[0]
        return (face_x < self.rotation_region_size)


    def is_face_in_right_region(self, face, image) -> bool:
        face_x = face[0]
        face_width = face[2]
        image_width = image.shape[1]
        return (face_x + face_width > image_width - self.rotation_region_size)



