from EST2D import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.optimize import minimize



class EST3D:
    def __init__(self,est1,est2) -> None:
        self.est1= est1
        self.est2= est2
        self.dist= 0
        self.num_t = 0
        self.num_s = 0
        self.t = []
        self.s = []
        self.connection_matrix = None
        self.connection_index = None
        self.z0 = 0
        self.z1 = 10
        self.terminals = []


    def solve_geosteiner(self):
        self.est1.solve()
        self.est2.solve()

    
        index_connection1 = self.est1.connection_index
        index_connection2 = self.est2.connection_index 
        # self.est1.plot_steiner_tree()
        # self.est2.plot_steiner_tree()


        lens1 = len(self.est1.terminals) - 2
        lens2 = len(self.est2.terminals) - 2
        lent1 = len(self.est1.terminals)
        lent2 = len(self.est2.terminals)

        self.num_t = lent1 + lent2
        self.num_s = lens1 + lens2 + 2

        #connections between steiner points
        index_connection_s1 = np.zeros((lens1 + 1,2))
        index_connection_s2 = np.zeros((lens2 + 1 ,2))



        cnt = 0
        i = 0
        #add connections between steiner points in the fist tree
        while i < len(index_connection1):
            if index_connection1[i][0] > lent1 - 1 and index_connection1[i][1] > lent1 - 1:
                #remove the connection between the steiner points and leave the one between terminals and steiner points
                index_connection_s1[cnt] = index_connection1[i]
                index_connection1 = np.delete(index_connection1,i,0)
                i -= 1
                cnt += 1
            i += 1
        
        cnt = 0
        i = 0
        #add connections between steiner points in the fist tree
        while i < len(index_connection2):
            if index_connection2[i][0] > lent2 - 1 and index_connection2[i][1] > lent2 - 1:
                index_connection_s2[cnt] = index_connection2[i]
                index_connection2 = np.delete(index_connection2,i,0)
                i -= 1
                cnt += 1
            i += 1


        new_connections1 = index_connection_s1[0]
        new_connections2 = index_connection_s2[0]

        #remove a steiner connection in order to create the new ones for the new steiner points in 3D

        index_connection_s1 = np.delete(index_connection_s1,0,0)
        index_connection_s2 = np.delete(index_connection_s2,0,0)


        index_connection_s1[-1] = [new_connections1[0], lent1 + lens1]
        index_connection_s1[-2] = [new_connections1[1], lent1 + lens1]

        index_connection_s2[-1] = [new_connections2[0], lent2 + lens2]
        index_connection_s2[-2] = [new_connections2[1], lent2 + lens2]

        #index_connection_s1 and index_connection_s2 are filled with all the connections between the steiner points and the 2 newly added
        #todo remove a random connection instead of the first one



        # add lent1 + lens1 + 1 (the added steiner point) to the indexes so they follow
        index_connection2 = index_connection2 + lent1 + lens1 + 1        
        index_connection_s2 = index_connection_s2 + lent1 + lens1 + 1

        #add a connection between the 2 newly added steiner points
        last_connection = np.array([[index_connection_s1[-1,1],index_connection_s2[-1,1]]])

        #concatenate all the connexions
        list_index = np.concatenate((index_connection1,index_connection2,index_connection_s1,index_connection_s2,last_connection),axis=0)
        self.connection_index = list_index

        #create the connection matrix
        matrix_index = np.zeros((lent1 + lent2 + lens1 + lens2 + 2,lent1 + lent2 + lens1 + lens2 + 2))
        for i in range(len(list_index)):
            matrix_index[int(list_index[i][0]) ,int( list_index[i][1])] = 1
        self.connection_matrix = matrix_index

        #the index that corresponds to the steiner points
        s_index = set()
        for i in range(len(index_connection_s1)):
            s_index.add(index_connection_s1[i][0])
            s_index.add(index_connection_s1[i][1])

        for i in range(len(index_connection_s2)):
            s_index.add(index_connection_s2[i][0])
            s_index.add(index_connection_s2[i][1])

        #the index that corresponds to the terminals
        t_index = set()
        for i in range(len(list_index)):
            t_index.add(list_index[i][0])
            t_index.add(list_index[i][1])

        t_index = t_index - s_index


        t_index = np.array(list(t_index))
        s_index = np.array(list(s_index))
        t_index = np.sort(t_index)
        s_index = np.sort(s_index)



        self.terminals = np.zeros((self.num_t,3))

        

        #make a dictionary that contains the index of the terminals and their coordinates

        for i in range(len(self.est1.terminals)):
            self.terminals[i] = np.array([self.est1.terminals[i][0],self.est1.terminals[i][1],self.z0])
        for i in range(len(self.est1.terminals),len(self.est1.terminals) + len(self.est2.terminals)):
            self.terminals[i] = np.array([self.est2.terminals[i - len(self.est1.terminals)][0],self.est2.terminals[i - len(self.est1.terminals)][1],self.z1])

        
        dict_index_coordinates_terminals = {t_index[i]:self.terminals[i] for i in range(self.num_t)}
        self.dict_index_coordinates_terminals = dict_index_coordinates_terminals


        dict_index_steiner = {value: index for index, value in enumerate(s_index)}
        self.dict_index_steiner = dict_index_steiner
        print(f'index steiner : {dict_index_steiner}')


        print(f'index connections : {self.connection_index}')
        print(f'dict index coordinates terminals : {dict_index_coordinates_terminals}')        


    def solve_minimize(self):
              


        initial_guess = np.repeat(0, 3 *  self.num_s)

        print(f'num s : {self.num_s}')


        # Define the objective function

        def objective_auto(vars):
            index_connections = self.connection_index
            dict_index_coordinates_terminals = self.dict_index_coordinates_terminals
            obj = 0
            for i in range(len(index_connections)):
                if index_connections[i][0] in dict_index_coordinates_terminals.keys():
                    a = dict_index_coordinates_terminals[index_connections[i][0]]
                else:
                    a = vars[3 * self.dict_index_steiner[index_connections[i][0]]:3 * self.dict_index_steiner[index_connections[i][0]] + 3]

                if index_connections[i][1] in dict_index_coordinates_terminals.keys():
                    b = dict_index_coordinates_terminals[index_connections[i][1]]
                else:
                    b = vars[3 * self.dict_index_steiner[index_connections[i][1]]:3 * self.dict_index_steiner[index_connections[i][1]] + 3]

                obj += np.linalg.norm(a - b)
            return obj


    
        # Perform the optimization
        result = minimize(objective_auto, initial_guess,method="Powell")


        print(result)

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