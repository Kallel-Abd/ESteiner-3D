from EST2D import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



class EST3D:
    def __init__(self,est1,est2) -> None:
        self.est1= est1
        self.est2= est2
        self.dist= 0
        self.num_t = 0
        self.num_s = 0
        self.t = []
        self.s = []


    def solve_geosteiner(self):
        pass
    def solve_minimize(self):
        pass
    def draw (self):
        t = self.t
        s = self.s
        x = t[:, 0]
        y = t[:, 1]
        z = t[:, 2]

        x2 = s[:, 0]
        y2 = s[:, 1]
        z2 = s[:, 2]


        # Create a 3D scatter plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x, y, z, c='r', marker='o')
        scatter2 = ax.scatter(x2, y2, z2, c='b', marker='o')

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