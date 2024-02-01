import re
import os
import traceback
import matplotlib.pyplot as plt
import numpy as np 


def extract_coordinates_from_sections(text):

    # Splitting the text into two parts
    part_define_terminals = text.split('DefineTerminals')[
        1].split('%%EndSetup')[0]
    part_certificate_of_solution = text.split('Certificate of solution:')[
        1].split('%%Page:')[0]
    length = float(text.split("length =")[1][:5])

    # Regular expression to find patterns of two floating point numbers
    pattern = r'(\d+\.\d+)\s+(\d+\.\d+)'

    # Extracting coordinates and converting to doubles
    coordinates_define_terminals = [(float(x), float(y)) for x, y in re.findall(pattern, part_define_terminals)]
    coordinates_certificate_of_solution = [(float(x), float(y)) for x, y in re.findall(pattern, part_certificate_of_solution)]

    return coordinates_define_terminals, coordinates_certificate_of_solution, length

def extract_connections(input_texte,terminals,sterminals):


    input_text = input_texte
    plot_text = re.search(r"BeginPlot(.*?)EndPlot", input_text, re.DOTALL).group(1)
    lines = plot_text.strip().split('\n')

    # Initialize a list to store the connections
    connections = []

    # Regular expression to match the lines with connections
    connection_pattern = re.compile(r"(\d+ T)\s+([\d.]+)\s+([\d.]+)|([\d.]+)\s+([\d.]+)\s+(\d+ T)|([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+S")

    for line in lines:
        # Check if line matches the connection pattern
        match = connection_pattern.findall(line)
        for m in match:
            #print(m)
            if m[0]:  # If the first group is not empty, format is "ID, x, y"
                connections.append([(m[0]), (float(m[1]), float(m[2]))])
            elif m[3]:  # Format is "x, y, ID"
                connections.append([(float(m[3]), float(m[4])), m[5]])
            else:
                connections.append([(float(m[6]), float(m[7])), (float(m[8]), float(m[9]))])


    connection_matrix = np.zeros(6)
    connection_index = np.zeros([len(connections),2])
    sommets = terminals + sterminals

    pr

    print( f'len connection : {len(connections)}')
    for i, connection in enumerate(connections):
        for j, point in enumerate(connection):
            if 'T' in  point:
                connections[i][j] = terminals[int(point[0])]
    
    for i in range(len(connections)):
        for j in range(2):

            for k in range(len(sommets)):
                if connections[i][j] == sommets[k]:
                    connection_index[i,j] = int(k )
    
    connection_matrix = np.zeros((len(sommets), len(sommets)))
    print(connection_matrix)
    print(len(sommets))

    # for i in range(len(sommets)):
    #     connection_matrix[int(sommets[i][0]),int( sommets[i][1])] = 1
    
        

    

    
    return connections, connection_index, connection_matrix


class EST2D:
    def __init__(self,tspPath) -> None:
        self.tspPath= tspPath
        self.sterminals = None
        self.terminals = None
        self.connections = None
        self.distance = 0
        self.connection_matrix = None
        
        

    def solve(self):
        try:
            resFileName= "result.txt"
            command="lib_points < {} | efst | bb > {}".format(self.tspPath,resFileName)
            os.system(command)
            resFile= open(resFileName,"r")
            text = resFile.read()

            terminals, sterminals,length=extract_coordinates_from_sections(text)

            self.terminals = terminals
            self.sterminals = sterminals
            self.distance = float(length)

            connection , connexion_index, connexion_matrix= extract_connections(text,self.terminals, self.sterminals)
            self.connections = connection
            self.connection_matrix = connexion_matrix


            print("sommets du graph",terminals)
            print("sommets du Steiner",sterminals)
            print(f'connection : {connection}')
            print(f'connexion index : {connexion_index}')
            print(f'connexion matrix : {connexion_matrix}')


        except():
            print("Solver command failed ")
            traceback.print_exc() 

    def draw(self):
        plt.style.use("default")
        assert(self.terminals)
        x=[]
        y=[]
        for point in self.terminals:
            x.append(float(point[0]))
            y.append(float(point[1]))

        sx=[]
        sy=[]
        for point in self.sterminals:
            sx.append(float(point[0]))
            sy.append(float(point[1]))
        
        plt.scatter(np.array(x),np.array(y),label="Graph")
        plt.scatter(np.array(sx),np.array(sy),label="points de steiner")
        plt.legend()
        plt.show()





    def plot_steiner_tree(self):
        plt.style.use("default")
        """
        Plots the Euclidean Steiner Tree.

        Parameters:
        - terminals: List of tuples representing the terminal points (x, y).
        - steiners: List of tuples representing the Steiner points (x, y).
        - connections: List of tuples representing the connections between points.
                    Each tuple is of the form [(x1, y1), (x2, y2)], where
                    (x1, y1) and (x2, y2) are the coordinates of the connected points.
        """
        terminals = self.terminals
        steiners = self.sterminals
        connections = self.connections
        # Plot terminal points
        for x, y in terminals:
            plt.plot(x, y, 'ro',label="terminals")  # red for terminals

        # Plot Steiner points
        for x, y in steiners:
            plt.plot(x, y, 'bo',label="steiner points")  # blue for Steiner points

        # Draw connections
        for connection in connections:
            x1, y1 = connection[0]
            x2, y2 = connection[1]
            plt.plot([x1, x2], [y1, y2], 'k-')  # black for connections

        plt.axis('equal')
        plt.xlabel('X coordinate')
        plt.ylabel('Y coordinate')
        plt.title('Euclidean Steiner Tree')
        #plt.legend()
        plt.show()










                