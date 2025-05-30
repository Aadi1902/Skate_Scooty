import pygame
from time import sleep
import serial
import json

# Constants
SERIAL_PORT = 'COM11'
BAUD_RATE = 9600
SerialObj = serial.Serial(SERIAL_PORT, BAUD_RATE)
sleep(3)


def convert_range(value, in_min, in_max, out_min, out_max):
    return ((value - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min


class JoystickReader:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def get_values(self):
        pygame.event.pump()
        return (-round(self.joystick.get_axis(3), 2),  # Throttle (inverted)
                round(self.joystick.get_axis(0), 2),  # Steering
                self.joystick.get_button(5))  # Brake button


if __name__ == '__main__':
    try:
        joy = JoystickReader()
        while True:
            throttle, steer, brake_btn = joy.get_values()

            t = r = 0
            if not brake_btn:
                if throttle < -0.2:  # Forward
                    t = int(convert_range(-throttle, 0.2, 1, 0.3, 1.5) / 5 * 255)
                elif throttle > 0.2:  # Reverse
                    t = int(convert_range(throttle, 0.2, 1, 0.3, 1.5) / 5 * 255)
                    r = 1

            data = {
                "t": t,
                "r": r,
                "brake": int(brake_btn),
                "s": int(convert_range(steer, -1, 1, 0, 60))
            }
            SerialObj.write((json.dumps(data) + "\n").encode('utf-8'))
            sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        SerialObj.close()
