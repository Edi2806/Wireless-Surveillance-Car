from picarx import Picarx
from robot_hat import Servo
import time

class MotionController:
    def __init__(self):
        self.px = Picarx()
        self.cam_servo_pan = Servo(1)
        self.cam_servo_tilt = Servo(2)

    def move_forward(self, speed=30, duration=0.5):
        self.px.forward(speed)
        time.sleep(duration)
        self.px.forward(0)

    def sweep_steering(self, delay=0.01):
        for angle in range(0, 35):
            self.px.set_dir_servo_angle(angle)
            time.sleep(delay)
        for angle in range(35, -35, -1):
            self.px.set_dir_servo_angle(angle)
            time.sleep(delay)
        for angle in range(-35, 0):
            self.px.set_dir_servo_angle(angle)
            time.sleep(delay)

    def sweep_camera(self, delay=0.01):
        for angle in range(0, 35):
            self.cam_servo_pan.angle(angle)
            time.sleep(delay)
        for angle in range(35, -35, -1):
            self.cam_servo_pan.angle(angle)
            time.sleep(delay)
        for angle in range(-35, 0):
            self.cam_servo_pan.angle(angle)
            time.sleep(delay)

        for angle in range(0, 35):
            self.cam_servo_tilt.angle(angle)
            time.sleep(delay)
        for angle in range(35, -35, -1):
            self.cam_servo_tilt.angle(angle)
            time.sleep(delay)
        for angle in range(-35, 0):
            self.cam_servo_tilt.angle(angle)
            time.sleep(delay)

    def stop(self):
        self.px.forward(0)
