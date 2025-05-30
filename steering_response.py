# steering_accuracy.py
import matplotlib.pyplot as plt
import numpy as np

# Planned vs actual servo positions (degrees)
planned_steering = np.array([90, 95, 100, 105, 110, 100, 90])
actual_steering = np.array([89, 96, 98, 107, 112, 99, 88])
error = actual_steering - planned_steering

plt.figure(figsize=(10, 5))
plt.plot(planned_steering, label='Planned Steering')
plt.plot(actual_steering, label='Actual Steering', linestyle='--')
plt.title('Steering Accuracy')
plt.xlabel('Time Step')
plt.ylabel('Steering Angle (degrees)')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 4))
plt.bar(range(len(error)), error)
plt.title('Steering Error')
plt.xlabel('Time Step')
plt.ylabel('Error (degrees)')
plt.grid(True)
plt.show()
