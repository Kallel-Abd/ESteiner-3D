import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

class YourClass:
    def __init__(self, terminals, s, dict_index_coordinates_terminals, dict_index_coordinates_steiner, connection_index):
        self.terminals = terminals
        self.s = s
        self.dict_index_coordinates_terminals = dict_index_coordinates_terminals
        self.dict_index_coordinates_steiner = dict_index_coordinates_steiner
        self.connection_index = connection_index

    def draw(self):
        t = self.terminals
        s = self.s

        # merge the terminals and the steiner dict
        all_coords = {**self.dict_index_coordinates_terminals, **self.dict_index_coordinates_steiner}

        x = t[:, 0]
        y = t[:, 1]
        z = t[:, 2]

        x2 = s[:, 0]
        y2 = s[:, 1]
        z2 = s[:, 2]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x, y, z, c='r', marker='o')
        scatter2 = ax.scatter(x2, y2, z2, c='b', marker='o')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # plot connections
        for connection in self.connection_index:
            x1, y1, z1 = all_coords[int(connection[0])]
            x2, y2, z2 = all_coords[int(connection[1])]
            ax.plot([x1, x2], [y1, y2], [z1, z2], 'k-')

        # Function to update the view on mouse drag
        def on_mouse_drag(event):
            if event.inaxes == ax:
                ax.view_init(elev=ax.elev + event.dy, azim=ax.azim + event.dx)
                fig.canvas.draw()

        # Connect the mouse drag event to the function
        fig.canvas.mpl_connect('motion_notify_event', on_mouse_drag)

        return fig, ax

    def update_animation(self, frame, ax):
        # You can update the plot for each animation frame if needed
        pass

    def create_animation(self):
        frames = 100
        interval = 50  # milliseconds

        fig, ax = self.draw()

        animation = FuncAnimation(fig, self.update_animation, frames=frames, fargs=(ax,), interval=interval, repeat=True)

        # Save the animation as a GIF
        animation.save('3d_animation.gif', writer='imagemagick')

        plt.show()

# Example usage:
terminals = np.random.rand(5, 3)  # Replace this with your actual data
s = np.random.rand(3, 3)  # Replace this with your actual data
dict_index_coordinates_terminals = {0: [0, 0, 0], 1: [1, 1, 1]}  # Replace this with your actual data
dict_index_coordinates_steiner = {2: [2, 2, 2], 3: [3, 3, 3]}  # Replace this with your actual data
connection_index = [(0, 1), (2, 3)]  # Replace this with your actual data

your_instance = YourClass(terminals, s, dict_index_coordinates_terminals, dict_index_coordinates_steiner, connection_index)
your_instance.create_animation()
