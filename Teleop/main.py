import pygame
from time import sleep
import serial
import json

''' Ardunio Pins
const int throttlePin = 6;  // Throttle (analog pin)
const int brakePin = 8;      // Brake (digital pin)
const int steeringPin = 9;   // Steering (servo pin)
'''

# Initialize constants
## Throttle
T_JOY_MIN = 0
T_JOY_MAX = 1
ARD_REF_V = 5
MOTOR_MIN_V = 0.9
MOTOR_MAX_V = 1.5
b = 1  # Use 1 for HIGH

## Steering
S_JOY_MIN = -1
S_JOY_MAX = 1
S_MIN = 0
S_MAX = 60  # Steering center is 30°, left is 0°, right is 60°

# Serial Setup
SERIAL_PORT = '/dev/ttyACM0' #nvidia
#SERIAL_PORT = 'com7' #windows
BAUD_RATE = 9600
SerialObj = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, bytesize=8, parity='N', stopbits=1)

sleep(3)  # Waiit for the serial connection to stabilize

# Data Range Conversion
def convert_range(value, input_min, input_max, output_min, output_max):
    scaled_value = ((value - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min
    return scaled_value

class JoystickReader:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print("Joystick Detected")
        except pygame.error:
            print("Joystick Not Found")
            self.joystick = None

    def get_joystick_values(self):
        if self.joystick is None:
            return 0, 0  # Return zero values if no joystick is detected

        pygame.event.pump()  # Process event queue
        x_axis = round(self.joystick.get_axis(1), 1)  # Left joystick X
        y_axis = round(-self.joystick.get_axis(3), 2)  # Right joystick Y
        return x_axis, y_axis

if __name__ == '__main__':
    try:
        joystick_reader = JoystickReader()
        while True:
            raw_throttle, raw_steer = joystick_reader.get_joystick_values()

            # Data Conversion
            throttle = -1 * raw_throttle
            steer = -1 * raw_steer

            # Throttle Control
            if throttle <= -0.7:
                t = 0
                b = 0  # Use 0 for LOW
            else:
                con_t = convert_range(throttle, T_JOY_MIN, T_JOY_MAX, MOTOR_MIN_V, MOTOR_MAX_V)
                t = int(con_t / ARD_REF_V * 255)
                b = 1  # Use 1 for HIGH

            # Steering Control
            con_s = convert_range(steer, S_JOY_MIN, S_JOY_MAX, S_MIN, S_MAX)
            s = int(con_s)

            data = {"t": t, "b": b, "s": s}
            json_data = json.dumps(data) + "\n"
            SerialObj.write(json_data.encode('utf-8'))  # Send data
            print(data)  # Print to console
            sleep(0.1)  # Adjust for desired frequency

    except KeyboardInterrupt:
        print("CTRL+C detected. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        SerialObj.close()  # Close the port
