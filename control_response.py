# control_response.py
import matplotlib.pyplot as plt
import numpy as np

# Simulated throttle response vs. time (s)
time = np.linspace(0, 10, 100)
input_throttle = np.piecewise(time, [time < 3, (time >= 3) & (time < 7), time >= 7], [0.2, 0.6, 0.3])
actual_speed = np.convolve(input_throttle, np.ones(10)/10, mode='same')

plt.figure(figsize=(10, 5))
plt.plot(time, input_throttle, label='Throttle Input', linestyle='--')
plt.plot(time, actual_speed, label='Speed Response', linewidth=2)
plt.title('Throttle vs Speed Response')
plt.xlabel('Time (s)')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
