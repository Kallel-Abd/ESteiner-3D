import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


points = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
])
x = points[:, 0]
y = points[:, 1]
z = points[:, 2]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z)

# Set axis labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Function to update the view on mouse drag
def on_mouse_drag(event):
    if event.inaxes == ax:
        ax.view_init(elev=ax.elev + event.dy, azim=ax.azim + event.dx)
        fig.canvas.draw()

# Connect the mouse drag event to the function
fig.canvas.mpl_connect('motion_notify_event', on_mouse_drag)

plt.show()
