from EST2D import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.optimize import minimize
import networkx as nx


class EST3D:
    def __init__(self, est1, est2, z) -> None:
        self.est1 = est1
        self.est2 = est2
        self.dist = float('inf')
        self.num_t = 0
        self.num_s = 0
        self.t = []
        self.s = []
        self.connection_matrix = None
        self.connection_index = None
        self.z0 = 0
        self.z1 = z
        self.terminals = []

    def solve_geosteiner(self):
        self.est1.solve()
        self.est2.solve()

        index_connection1 = self.est1.connection_index
        index_connection2 = self.est2.connection_index

        lens1 = len(self.est1.terminals) - 2
        lens2 = len(self.est2.terminals) - 2
        lent1 = len(self.est1.terminals)
        lent2 = len(self.est2.terminals)

        self.num_t = lent1 + lent2
        self.num_s = lens1 + lens2 + 2

        # create graph object of the 2 graphs in order to get the center
        G1 = nx.Graph()
        for i in range(len(index_connection1)):
            G1.add_edge(index_connection1[i][0], index_connection1[i][1])
        center1 = nx.center(G1)

        G2 = nx.Graph()
        for i in range(len(index_connection2)):
            G2.add_edge(index_connection2[i][0], index_connection2[i][1])
        center2 = nx.center(G2)

        # if their is 2 center the edge we get rid of is the one between the 2 centers
        # if their is 1 center we get rid of the edge between the center and one of its neighbours

        if len(center1) == 2:
            possibility1 = 1
        elif len(center1) == 1:
            neighbourscenter1 = list(G1.neighbors(center1[0]))
            possibility1 = len(neighbourscenter1)
        if len(center2) == 2:
            possibility2 = 1

        elif len(center2) == 1:
            neighbourscenter2 = list(G2.neighbors(center2[0]))
            possibility2 = len(neighbourscenter2)

        # create a list of all possible edges for each graph depending on the edge we get rid of

        possible_arrangement = [None] * possibility1 * possibility2
        possible_arrangement1 = [None] * possibility1
        possible_arrangement2 = [None] * possibility2
        self.number_of_possible_arrangement = possibility1 * possibility2
        # remove the edge between the 2 centers and add an edge connecting to the new steiner point
        if len(center1) == 2:

            possible_arrangement1[0] = G1.copy()
            possible_arrangement1[0].remove_edge(center1[0], center1[1])
            possible_arrangement1[0].add_edge(lent1 + lens1, center1[0])
            possible_arrangement1[0].add_edge(lent1 + lens1, center1[1])
        # do every possibility of removing an edge between the center and one of its neighbours
        elif len(center1) == 1:
            neighbourscenter1 = list(G1.neighbors(center1[0]))

            for i in range(possibility1):
                possible_arrangement1[i] = G1.copy()
                possible_arrangement1[i].remove_edge(
                    center1[0], neighbourscenter1[i])
                possible_arrangement1[i].add_edge(lent1 + lens1, center1[0])
                possible_arrangement1[i].add_edge(
                    lent1 + lens1, neighbourscenter1[i])
        if len(center2) == 2:
            possible_arrangement2[0] = G2.copy()
            possible_arrangement2[0].remove_edge(center2[0], center2[1])
            possible_arrangement2[0].add_edge(
                lent2 + lens2, center2[0])
            possible_arrangement2[0].add_edge(
                lent2 + lens2, center2[1])

        elif len(center2) == 1:
            neighbourscenter2 = list(G2.neighbors(center2[0]))
            for i in range(possibility2):
                possible_arrangement2[i] = G2.copy()
                possible_arrangement2[i].remove_edge(
                    center2[0], neighbourscenter2[i])
                possible_arrangement2[i].add_edge(lent2 + lens2, center2[0])
                possible_arrangement2[i].add_edge(
                    lent2 + lens2, neighbourscenter2[i])

        # the edges are converted to a list of lists

        for i in range(possibility1):
            possible_arrangement1[i] = list(possible_arrangement1[i].edges)
            possible_arrangement1[i] = [list(x)
                                        for x in possible_arrangement1[i]]
        for i in range(possibility2):
            possible_arrangement2[i] = list(possible_arrangement2[i].edges)
            possible_arrangement2[i] = [list(x)
                                        for x in possible_arrangement2[i]]

            possible_arrangement2[i] = [
                [element + lent1 + lens1 + 1 for element in sublist] for sublist in possible_arrangement2[i]]

        # # add a connection between the 2 newly added steiner points
        last_connection = [[lent1 + lens1, lent1 + lens1 + lent2 + lens2 + 1]]

        # Comnining the possibilities of edges for the 2 graphs
        for i in range(possibility1):
            for j in range(possibility2):
                possible_arrangement[i * possibility2 + j] = possible_arrangement1[i] + \
                    possible_arrangement2[j] + last_connection

        self.possible_arrangement = possible_arrangement

        # the index that corresponds to the terminal points
        t_index = set()
        for i in range(lent1):
            t_index.add(i)

        for i in range(lent1+lens1+1, lent1+lens1+1+lent2):
            t_index.add(i)

        # the index that corresponds to the steiner points
        s_index = set()
        for i in range(lent1, lent1+lens1+1):
            s_index.add(i)
        for i in range(lent1+lens1+1+lent2, lent1+lens1+lent2+lent2):
            s_index.add(i)

        t_index = np.array(list(t_index))
        s_index = np.array(list(s_index))
        t_index = np.sort(t_index)
        s_index = np.sort(s_index)

        self.s_index = s_index

        self.terminals = np.zeros((self.num_t, 3))

        # make a dictionary that contains the index of the terminals and their coordinates

        for i in range(len(self.est1.terminals)):
            self.terminals[i] = np.array(
                [self.est1.terminals[i][0], self.est1.terminals[i][1], self.z0])
        for i in range(len(self.est1.terminals), len(self.est1.terminals) + len(self.est2.terminals)):
            self.terminals[i] = np.array([self.est2.terminals[i - len(self.est1.terminals)]
                                         [0], self.est2.terminals[i - len(self.est1.terminals)][1], self.z1])

        dict_index_coordinates_terminals = {
            t_index[i]: self.terminals[i] for i in range(self.num_t)}
        self.dict_index_coordinates_terminals = dict_index_coordinates_terminals

        dict_index_steiner = {value: index for index,
                              value in enumerate(s_index)}
        self.dict_index_steiner = dict_index_steiner

    def solve_minimize(self):

        # solve the optimization problem for each possible arrangement
        for i in range(self.number_of_possible_arrangement):
            initial_guess = np.repeat(0, 3 * self.num_s)

            # Define the objective function

            def objective_auto(vars):
                index_connections = connection_index
                dict_index_coordinates_terminals = self.dict_index_coordinates_terminals
                obj = 0
                for i in range(len(index_connections)):
                    if index_connections[i][0] in dict_index_coordinates_terminals.keys():
                        a = dict_index_coordinates_terminals[index_connections[i][0]]
                    else:
                        a = vars[3 * self.dict_index_steiner[index_connections[i][0]]                                 :3 * self.dict_index_steiner[index_connections[i][0]] + 3]

                    if index_connections[i][1] in dict_index_coordinates_terminals.keys():
                        b = dict_index_coordinates_terminals[index_connections[i][1]]
                    else:
                        b = vars[3 * self.dict_index_steiner[index_connections[i][1]]                                 :3 * self.dict_index_steiner[index_connections[i][1]] + 3]

                    obj += np.linalg.norm(a - b)
                return obj

            # Perform the optimization
            connection_index = self.possible_arrangement[i]
            result = minimize(objective_auto, initial_guess, method="Powell")

            # Update the optimal solution if the new solution is better
            if result.fun < self.dist:
                s = result.x
                s = s.reshape((self.num_s, 3))
                self.s = s
                # distance
                self.dist = result.fun

                dict_index_coordinates_steiner = {
                    self.s_index[i]: s[i] for i in range(self.num_s)}
                self.dict_index_coordinates_steiner = dict_index_coordinates_steiner
                self.connection_index = connection_index

    def draw(self):
        t = self.terminals
        s = self.s

        # merge the terminals and the steiner dict
        all = {**self.dict_index_coordinates_terminals,
               **self.dict_index_coordinates_steiner}

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

        # plot connections
        for connection in self.connection_index:
            x1, y1, z1 = all[int(connection[0])]
            x2, y2, z2 = all[int(connection[1])]
            ax.plot([x1, x2], [y1, y2], [z1, z2], 'k-')

        # Function to update the view on mouse drag
        def on_mouse_drag(event):
            if event.inaxes == ax:
                ax.view_init(elev=ax.elev + event.dy, azim=ax.azim + event.dx)
                fig.canvas.draw()

        # Connect the mouse drag event to the function
        fig.canvas.mpl_connect('motion_notify_event', on_mouse_drag)

        plt.show()
