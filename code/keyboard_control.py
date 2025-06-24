from picarx import Picarx
from robot_hat import Servo
from time import sleep
import readchar

manual = '''
Press keys on keyboard to control PiCar-X!
    w: Forward
    s: Backward
    a: Turn left Forward
    d: Turn right Forward
    q: Turn letf Backward
    e: Turn right Backward
    i: Camera Head up
    m: Camera Head down
    j: Camera Turn head left
    l: Camera Turn head right
    k: Camera head centre
    ctrl+c: Quit
'''

class KeyboardController:
    def __init__(self):
        self.px = Picarx()
        self.cam_pan = Servo(0)
        self.cam_tilt = Servo(1)
        self.pan_angle = 0
        self.tilt_angle = 0

    def show_info(self):
        print("\033[H\033[J", end='')  # Clear terminal
        print(manual)

    def run(self):
        self.show_info()
        try:
            while True:
                key = readchar.readkey().lower()

                if key in 'wsadqemijlk':
                    if key == 'w':
                        self.px.set_dir_servo_angle(0)
                        self.px.forward(80)
                    elif key == 's':
                        self.px.set_dir_servo_angle(0)
                        self.px.backward(80)
                    elif key == 'a':
                        self.px.set_dir_servo_angle(-35)
                        self.px.forward(80)
                    elif key == 'd':
                        self.px.set_dir_servo_angle(35)
                        self.px.forward(80)
                    elif key == 'q':
                        self.px.set_dir_servo_angle(35)
                        self.px.backward(80)
                    elif key == 'e':
                        self.px.set_dir_servo_angle(-35)
                        self.px.backward(80)

                  #Camera Control
                    elif key == 'i':
                        self.tilt_angle = min(-45, self.tilt_angle - 10)
                        self.cam_tilt.angle(self.tilt_angle)
                    elif key == 'm':
                        self.tilt_angle = max(38, self.tilt_angle + 10)
                        self.cam_tilt.angle(self.tilt_angle)
                    elif key == 'l':
                        self.pan_angle = min(45, self.pan_angle + 10)
                        self.cam_pan.angle(self.pan_angle)
                    elif key == 'j':
                        self.pan_angle = max(-45, self.pan_angle - 10)
                        self.cam_pan.angle(self.pan_angle)
                    elif key == 'k':
                        self.pan_angle = 0
                        self.tilt_angle = 0
                        self.cam_pan.angle (0)
                        self.cam_tilt.angle(0)

                    elif key == readchar.key.CTRL_C:
                        print("\n Back to Menu")
                        return

                    self.show_info()
                    sleep(0.5)
                    self.px.stop()
        finally:
            self.cam_pan.angle(0)
            self.cam_tilt.angle(0)
            self.px.set_dir_servo_angle(0)
            self.px.stop()
        print("Stopped and reset.")
