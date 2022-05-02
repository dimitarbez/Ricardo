from picamera import PiCamera
from datetime import datetime


class CameraSoftwareController:

    __camera_window: tuple(200,-100,600,800)

    def __init__(self) -> None:
        self.camera = PiCamera()
        self.camera.rotation = 0

    def __del__(self):
        self.camera.stop_preview()

    def start_camera(self):
        self.camera.start_preview(fullscreen=False, window=self.__camera_window)

    def zoom_in(self):
        self.camera.zoom = (0.25, 0.25, 0.5, 0.5)

    def zoom_out(self):
        self.camera.zoom = (0, 0, 1, 1)

    def take_picture(self):
        now = datetime.now()
        timestamp = now.strftime("%d%m%Y-%H%M%S")
        self.camera.capture('/home/pi/Desktop/RobotImages/robot_%s.jpg' % timestamp)
    