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
        self.connection_matrix = None
        self.connection_index = None


    def solve_geosteiner(self):
        self.est1.solve()
        self.est2.solve()
        index_connection1 = self.est1.connection_index
        index_connection2 = self.est2.connection_index 
        lens1 = len(self.est1.terminals) - 2
        lens2 = len(self.est2.terminals) - 2
        lent1 = len(self.est1.terminals)
        lent2 = len(self.est2.terminals)
        lenindex1 = len(index_connection1)
        lenindex2 = len(index_connection2)


        index_connection_s1 = np.zeros((lens1 + 1,2))
        index_connection_s2 = np.zeros((lens2 + 1 ,2))



        cnt = 0
        i = 0
        while i < len(index_connection1):
            if index_connection1[i][0] > lent1 - 1 and index_connection1[i][1] > lent1 - 1:
                #remove the connection
                index_connection_s1[cnt] = index_connection1[i]
                index_connection1 = np.delete(index_connection1,i,0)
                i -= 1
                cnt += 1
            i += 1
        
        cnt = 0
        i = 0
        while i < len(index_connection2):
            if index_connection2[i][0] > lent2 - 1 and index_connection2[i][1] > lent2 - 1:
                #remove the connection
                index_connection_s2[cnt] = index_connection2[i]
                index_connection2 = np.delete(index_connection2,i,0)
                i -= 1
                cnt += 1
            i += 1
        
        

        new_connections1 = index_connection_s1[0]
        new_connections2 = index_connection_s2[0]

        index_connection_s1 = np.delete(index_connection_s1,0,0)
        index_connection_s2 = np.delete(index_connection_s2,0,0)

        index_connection_s1[-1] = [new_connections1[0], lent1 + lens1]
        index_connection_s1[-2] = [new_connections1[1], lent1 + lens1]

        index_connection_s2[-1] = [new_connections2[0], lent2 + lens2]
        index_connection_s2[-2] = [new_connections2[1], lent2 + lens2]



        for i in range(len(index_connection1)):
            for j in range(2):
                if index_connection1[i][j] > lent1 - 1:
                    index_connection1[i][j] += lent2
        
        index_connection2 = index_connection2 + lent1
        
        for i in range(len(index_connection2)):
            for j in range(2):
                if index_connection2[i][j] > lent1 + lent2 - 1:
                    index_connection2[i][j] += lens1


        index_connection_s1 = index_connection_s1 + lent2


        index_connection_s2 = index_connection_s2 + lent1 + lens1 + 1

        list_index = np.concatenate((index_connection1,index_connection2,index_connection_s1,index_connection_s2),axis=0)
        self.connection_index = list_index

        matrix_index = np.zeros((lent1 + lent2 + lens1 + lens2 + 2,lent1 + lent2 + lens1 + lens2 + 2))

        for i in range(len(list_index)):
            for j in range(2):
                matrix_index[i][j] = int(list_index[i][j])
        
        self.connection_matrix = matrix_index
        
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