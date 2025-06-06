# -*- coding: utf-8 -*-
"""Inverse Kinematics Solver for Robot Manipulator.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FSona_SciAUxXtruM8YdR6ffpS4B2Qt9
"""

!pip install numpy matplotlib > /dev/null  # Silent install
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Robot arm configuration
link_lengths = [1.0, 1.0, 1.0]  # 3 links of 1 unit each
num_joints = len(link_lengths)
target = np.array([0.5, 2.0])    # Reachable target

# Forward kinematics calculation
def forward_kinematics(theta):
    x, y = 0.0, 0.0
    angle = 0.0
    positions = [(x, y)]
    for i in range(num_joints):
        angle += theta[i]
        x += link_lengths[i] * np.cos(angle)
        y += link_lengths[i] * np.sin(angle)
        positions.append((x, y))
    return np.array([x, y]), positions

# Inverse Kinematics Solver with motion history
def gradient_descent_ik(target, max_iter=2000, lr=0.01, tolerance=1e-3):
    theta = np.zeros(num_joints)
    history = [theta.copy()]

    for _ in range(max_iter):
        error = np.linalg.norm(forward_kinematics(theta)[0] - target)
        if error < tolerance:
            break

        # Numerical gradient calculation
        grad = np.zeros(num_joints)
        for i in range(num_joints):
            theta_temp = theta.copy()
            theta_temp[i] += 1e-6
            error_temp = np.linalg.norm(forward_kinematics(theta_temp)[0] - target)
            grad[i] = (error_temp - error) / 1e-6

        theta -= lr * grad
        history.append(theta.copy())

    return theta, history

# Run IK solver and get motion history
theta_optimized, history = gradient_descent_ik(target)

# Create animation
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.grid(True)
ax.set_title("Robot Arm IK Animation")

line, = ax.plot([], [], 'bo-', lw=2)
target_marker = ax.plot(target[0], target[1], 'rx', markersize=12)[0]

def update(frame):
    _, positions = forward_kinematics(history[frame])
    line.set_data([p[0] for p in positions], [p[1] for p in positions])
    return line, target_marker

# Animate at 30fps (faster than real-time for demonstration)
ani = FuncAnimation(fig, update, frames=len(history), interval=30, blit=True)
plt.close()  # Prevent double display of static plot

# Display animation in notebook
from IPython.display import HTML
HTML(ani.to_html5_video())