from vilib import Vilib
from picarx import Picarx
from time import sleep
import time


def run_automatic_car():
    px = Picarx()
    px_power = 20
    offset = 20
    SAFE_DISTANCE = 3 #cm
    last_state = "stop"

    # Start the Camera
    try:
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=True, web=False)  # Set web=True to see it via browser too
    except Exception as e:
        print(f"Camera error: {e}")
    sleep(1)

    def outHandle():
        nonlocal last_state
        if last_state == 'left':
            px.set_dir_servo_angle(-30)
            px.backward(10)
        elif last_state == 'right':
            px.set_dir_servo_angle(30)
            px.backward(10)
        while True:
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("outHandle gm_val_list: %s, %s"%(gm_val_list, gm_state))
            if gm_state != last_state:
                break
        sleep(0.001)
    def get_status(val_list):
        _state = px.get_line_status(val_list)
        if _state == [0, 0, 0]:
            return 'stop'
        elif _state[1] == 1:
            return 'forward'
        elif _state[0] == 1:
            return 'right'
        elif _state[2] == 1:
            return 'left'
        return 'stop'

    # === Main Loop ===
    try:
        print("Starting Automatic car")
        while True:
            # Check distance
            distance = px.ultrasonic.read()
            print(f"Ultrasonic distance: {distance:.2f} cm")
            if distance < SAFE_DISTANCE:
                print("Obstacle detected - stopping")
                px.stop()
                time.sleep(1)
                continue

            #Line Following
            gm_val_list = px.get_grayscale_data()
            gm_state = get_status(gm_val_list)
            print("gm_val_list:", gm_val_list, gm_state)

            if gm_state != "stop":
                last_state = gm_state

            if gm_state == 'forward':
                px.set_dir_servo_angle(0)
                px.forward(px_power)
            elif gm_state == 'left':
                px.set_dir_servo_angle(offset)
                px.forward(px_power)
            elif gm_state == 'right':
                px.set_dir_servo_angle(-offset)
                px.forward(px_power)
            else:
                print("Line lost - stopping")
                px.stop()
                outHandle()

            sleep(0.05)

    except KeyboardInterrupt:
        print("\n Ctrl+C detected - stopping")
    finally:
        px.stop()
        Vilib.camera_close()
        print("stop and exit")

