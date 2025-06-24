from sunfounder_controller import SunFounderController
from picarx import Picarx
from robot_hat import utils, Music
from vilib import Vilib
import os
import time

# === Setup user paths and music player ===
User = os.popen('echo ${SUDO_USER:-$LOGNAME}').readline().strip()
UserHome = os.popen('getent passwd %s | cut -d: -f 6' %User).readline().strip()
music = Music()

# === Horn Function ===
def horn():
    _status, _result = utils.run_command('sudo killall pulseaudio')
    music.sound_play_threading(f'{UserHome}/picar-x/sounds/car-double-horn.wav')

# === Obstacle Avoidance Logic ===
def avoid_obstacles(px):
    distance = px.get_distance()
    if distance >= 40:
        px.set_dir_servo_angle(0)
        px.forward(40)
    elif distance >= 20:
        px.set_dir_servo_angle(30)
        px.forward(40)
        time.sleep(0.1)
    else:
        px.set_dir_servo_angle(-30)
        px.backward(40)
        time.sleep(0.5)

# === Line Following Logic ===
def get_status(val_list, px):
    _state = px.get_line_status(val_list)
    if _state == [0, 0, 0]:
        return 'stop'
    elif _state[1] == 1:
        return 'forward'
    elif _state[0] == 1:
        return 'right'
    elif _state[2] == 1:
        return 'left'

def outHandle(px, last_line_state):
    if last_line_state == 'left':
        px.set_dir_servo_angle(-30)
        px.backward(10)
    elif last_line_state == 'right':
        px.set_dir_servo_angle(30)
        px.backward(10)
    while True:
        gm_val_list = px.get_grayscale_data()
        gm_state = get_status(gm_val_list, px)
        if gm_state != last_line_state:
            break
    time.sleep(0.001)

def line_track(px, last_line_state):
    gm_val_list = px.get_grayscale_data()
    gm_state = get_status(gm_val_list, px)

    if gm_state != "stop":
        last_line_state = gm_state

    if gm_state == 'forward':
        px.set_dir_servo_angle(0)
        px.forward(10)
    elif gm_state == 'left':
        px.set_dir_servo_angle(20)
        px.forward(10)
    elif gm_state == 'right':
        px.set_dir_servo_angle(-20)
        px.forward(10)
    else:
        outHandle(px, last_line_state)

    return last_line_state

# === Main App Control Function ===
def run_app_control():
    print("Starting custom SunFounder app control...")

    # Reset board and initialize
    utils.reset_mcu()
    time.sleep(0.2)

    sc = SunFounderController()
    sc.set_name('MyCustomApp')
    sc.set_type('Picarx')
    sc.start()

    px = Picarx()
    last_line_state = "stop"
    speed = 0

    ip = utils.get_ip()
    print(f'IP: {ip}')
    sc.set('video', f'http://{ip}:9000/mjpg')

    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)

    speak = None

    try:
        while True:
            # Send sensor data to app
            sc.set("A", speed)
            sc.set("D", px.get_grayscale_data())
            sc.set("F", px.get_distance())

            # Horn button
            if sc.get('M') == True:
                horn()

            # Voice command
            speak = sc.get('J')
            if speak in ["forward"]:
                px.forward(speed)
            elif speak in ["backward"]:
                px.backward(speed)
            elif speak in ["left"]:
                px.set_dir_servo_angle(-30)
                px.forward(60)
                time.sleep(1.2)
                px.set_dir_servo_angle(0)
                px.forward(speed)
            elif speak in ["right", "white", "rice"]:
                px.set_dir_servo_angle(30)
                px.forward(60)
                time.sleep(1.2)
                px.set_dir_servo_angle(0)
                px.forward(speed)
            elif speak in ["stop"]:
                px.stop()

            # Line tracking / obstacle avoidance switches
            if sc.get('I') == True:
                speed = 10
                last_line_state = line_track(px, last_line_state)
            elif sc.get('E') == True:
                speed = 40
                avoid_obstacles(px)
            else:
                # Manual joystick
                joystick = sc.get("K")
                if joystick:
                    angle = utils.mapping(joystick[0], -100, 100, -30, 30)
                    speed = joystick[1]

                    px.set_dir_servo_angle(angle)

                    if speed > 0:
                        px.forward(speed)
                    elif speed < 0:
                        px.backward(-speed)
                    else:
                        px.stop()

            # Camera pan/tilt
            cam = sc.get('Q')
            if cam:
                pan = min(90, max(-90, cam[0]))
                tilt = min(65, max(-35, cam[1]))
                px.set_cam_pan_angle(pan)
                px.set_cam_tilt_angle(tilt)

            # Image recognition toggles
            if sc.get('N') == True:
                Vilib.color_detect("red")
            else:
                Vilib.color_detect("close")

            Vilib.face_detect_switch(sc.get('O') == True)
            Vilib.object_detect_switch(sc.get('P') == True)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Exiting app control")
        px.stop()
        Vilib.camera_close()

if __name__ == "__main__":
    run_app_control()
