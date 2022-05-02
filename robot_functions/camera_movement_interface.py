from abc import ABC, abstractmethod

class CameraMovementInterface(ABC):

    @abstractmethod
    def move_camera_up(self):
        pass

    @abstractmethod
    def move_camera_down(self):
        pass

    @abstractmethod
    def move_camera_left(self):
        pass

    @abstractmethod
    def move_camera_right(self):
        pass

    @abstractmethod
    def center_camera(self):
        pass
