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
        self.est1.plot_steiner_tree()
        self.est2.plot_steiner_tree()


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
        print(f'index_connection1 : {index_connection1}')
        print(f'index_connection_s1 : {index_connection_s1}')
        print(f'index_connection2 : {index_connection2}')
        print(f'index_connection_s2 : {index_connection_s2}')
        print(f'last_connection : {last_connection}')
        list_index = np.concatenate((index_connection1,index_connection2,index_connection_s1,index_connection_s2,last_connection),axis=0)
        print(f'list_index : {list_index}')
        self.connection_index = list_index

        matrix_index = np.zeros((lent1 + lent2 + lens1 + lens2 + 2,lent1 + lent2 + lens1 + lens2 + 2))

        for i in range(len(list_index)):
            matrix_index[int(list_index[i][0]) ,int( list_index[i][1])] = 1
        
        self.connection_matrix = matrix_index
        print(f'connection_matrix : \n {self.connection_matrix}')

        self.terminals = np.zeros((self.num_t,3))

        for i in range(len(self.est1.terminals)):
            self.terminals[i] = np.array([self.est1.terminals[i][0],self.est1.terminals[i][1],self.z0])
        for i in range(len(self.est1.terminals),len(self.est1.terminals) + len(self.est2.terminals)):
            print(f'i : {i}')
            self.terminals[i] = np.array([self.est2.terminals[i - len(self.est1.terminals)][0],self.est2.terminals[i - len(self.est1.terminals)][1],self.z1])
        print(f'terminals : {self.terminals}')
        
    def solve_minimize(self):


        # def objective(vars):
        #     self.s = np.zeros(3*self.num_s)
        #     # print(f'vars : {vars}')
        #     for i in range(self.num_s):
        #         self.s[3*i:3*i+3] = vars[3*i:3*i+3]
            
        #     # print(f's : {self.s}')
            
        #     objt = 0
        #     # print(f'terminals : {self.est1.terminals}')
        #     for i in range(len(self.connection_index)):
        #         # print(f'connection_index : {self.connection_index[i]}')
                
        #         if self.connection_index[i][0] > (self.num_t - 1):
        #             a = self.s[int(self.connection_index[i][0])]
        #             # print(f'aa : {a}')
        #         elif self.connection_index[i][0] < len(self.est1.terminals):
        #             a = np.array([self.est1.terminals[int(self.connection_index[i][0])][0],self.est1.terminals[int(self.connection_index[i][0])][1],self.z0])
        #             # print(f'ab : {a}')   
        #         else:
        #             a = np.array([self.est1.terminals[int(self.connection_index[i][0] - len(self.est1.terminals))][0],self.est2.terminals[int(self.connection_index[i][0] - len(self.est1.terminals))][1],self.z1]) 
        #             # print(f'ac : {a}')  

        #         if self.connection_index[i][1] > (self.num_t - 1):
        #             b = self.s[int(self.connection_index[i][1])]
        #             # print(f'ba : {b}')
        #         elif self.connection_index[i][1] < len(self.est1.terminals):
        #             b = np.array([self.est1.terminals[int(self.connection_index[i][1])][0],self.est1.terminals[int(self.connection_index[i][1])][1],self.z0])
        #             # print(f'bb : {b}')
        #         else:
        #             b = np.array([self.est1.terminals[int(self.connection_index[i][1] - len(self.est1.terminals))][0],self.est2.terminals[int(self.connection_index[i][1] - len(self.est1.terminals))][1],self.z1])
        #             # print(f'bc : {b}')
        #         objt += np.linalg.norm(a - b)
        #         # print(f'objt : {objt}')
        #     # print(objt)
        #     return objt


                        


        # initial_guess = np.repeat(0, 3 *  self.num_s)

        # print(f'initial_guess : {initial_guess}')

        # result = minimize(objective, initial_guess,method="Powell")
        # print(result)
        # # for i in range(self.num_s):
        # #     print(f's{i} : {result.x[3*i:3*i+3]}')
        # return result.x
        # Define the points a, b, and c
        # t1 = self.terminals[0]
        # t2 = self.terminals[1]
        # t3 = self.terminals[2]
        # t4 = self.terminals[3]
        # t5 = self.terminals[4]
        # t6 = self.terminals[5]
        # t7 = self.terminals[6]
        # t8 = self.terminals[7]

        t1 = np.array([0, 0, 0])
        t2 = np.array([0, 0, 1])
        t3 = np.array([0, 1, 0])
        t4 = np.array([0, 1, 1])
        t5 = np.array([1, 0, 0])
        t6 = np.array([1, 0, 1])
        t7 = np.array([1, 1, 0])
        t8 = np.array([1, 1, 1])


        # c = np.array([1, 1, 0]) # Given but not used in the function

        # Define the objective function
        def objective(vars):
            s1, s2, s3, s4, s5, s6 = vars[:3], vars[3:6],vars[6:9],vars[9:12],vars[12:15],vars[15:18]  # Split the variables into x and y
            return np.linalg.norm(t1 - s1) + np.linalg.norm(t2 - s1) + np.linalg.norm(s2 - t3)+ np.linalg.norm(s2 - t4)+np.linalg.norm(s5- s1)+np.linalg.norm(s2 - s5)+np.linalg.norm(s5 - s6)+np.linalg.norm(s3 - s6)+np.linalg.norm(s4 -s6)+np.linalg.norm(s3 - t5)+np.linalg.norm(s3 - t6)+np.linalg.norm(s4 - t7)+np.linalg.norm(s4 - t8)

        # Initial guess for x and y
        initial_guess = np.repeat(0,18)  # Assuming both x and y start from the origin

        # Perform the optimization
        result = minimize(objective, initial_guess,method="Powell")

        # Extract the optimized values of x and y
        # x_opt, y_opt = result.x[:3], result.x[3:]
        s1, s2, s3, s4, s5, s6 = result.x[:3], result.x[3:6],result.x[6:9],result.x[9:12],result.x[12:15],result.x[15:18]  # Split the variables into x and y

        # print("Optimized x:", x_opt)
        # print("Optimized y:", y_opt)

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