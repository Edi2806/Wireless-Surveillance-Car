from motion import MotionController
from keyboard_control import KeyboardController
from Automatic_car import run_automatic_car
from app_control import run_app_control
import os

def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_menu():
    clear_terminal()
    print("\n")
    print("\033[1;36m" + "+-----------------------------------------+" + "\033[0m")
    print("\033[1;32m" + "|        Wireless Surveillance Car        |" + "\033[0m")
    print("\033[1;32m" + "|                 Main Menu               |" + "\033[0m")
    print("\033[1;36m" + "+-----------------------------------------+" + "\033[0m")
    print("\033[1;34m" + "| 1. Motion Demo                          |" + "\033[0m")
    print("\033[1;34m" + "| 2. Keyboard Control                     |" + "\033[0m")
    print("\033[1;34m" + "| 3. Automatic Car (Line, Video, Obstacle)|" + "\033[0m")
    print("\033[1;34m" + "| 4. Control via Mobile App               |" + "\033[0m")
    print("\033[1;34m" + "| q. Quit                                 |" + "\033[0m")
    print("\033[1;36m" + "+-----------------------------------------+" + "\033[0m")
    print()

def run_motion_demo():
    motion = MotionController()
    try:
        motion.move_forward()
        motion.sweep_steering()
        motion.sweep_camera()
    finally:
        motion.stop()

def run_keyboard_control():
    controller = KeyboardController()
    try:
        controller.run()
    except KeyboardInterrupt:
        print("\n Returning to main menu..")

if __name__ == "__main__":
    try:
        while True:
            print_menu()
            mode = input("\033[1;33mSelect an option (1, 2, 3, 4 or q): \033[0m").strip()

            if mode == '1':
                run_motion_demo()
            elif mode == '2':
                run_keyboard_control()
            elif mode == '3':
                run_automatic_car()
            elif mode == '4':
                run_app_control()
            elif mode.lower() == 'q':
                print("\n\033[1;31mGoodbye!\033[0m\n")
                break
            else:
                print("\n\033[1;33mInvalid option. Please choose 1, 2, 3 or q.\033[0m\n")
                input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\n\033[1;31mInterrupted by user. Exiting...\033[0m")
