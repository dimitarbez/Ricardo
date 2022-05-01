import numpy as np


class MotorSpeedCalculator:

    @classmethod
    def calculate_left_motor_speed(cls, face_x, rotation_region_size) -> int:
        # interpolate motor speed from left side border to left edge of screen
        left_motorspeed = ((face_x - rotation_region_size) * (-100) / (rotation_region_size))
        left_motorspeed = np.clip(left_motorspeed, 35, 80)
        return left_motorspeed

    @classmethod
    def calculate_right_motor_speed(cls, face_x, face_width, image_width, rotation_region_size) -> int:
        # interpolate motor speed from right side border to right edge of screen
        right_motorspeed = (((face_x + face_width) - (image_width - rotation_region_size)) * 100) / rotation_region_size
        right_motorspeed = np.clip(right_motorspeed, 35, 80)
        return right_motorspeed