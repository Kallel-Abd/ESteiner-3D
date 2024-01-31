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

    # Regular expression to find patterns of two floating point numbers
    pattern = r'(\d+\.\d+)\s+(\d+\.\d+)'

    # Extracting coordinates
    coordinates_define_terminals = re.findall(pattern, part_define_terminals)
    coordinates_certificate_of_solution = re.findall(
        pattern, part_certificate_of_solution)

    return coordinates_define_terminals, coordinates_certificate_of_solution


class EST:
    def __init__(self,tspPath) -> None:
        self.sterminals = None
        self.terminals = None
        self.distance = 0
        self.tspPath= tspPath
        

    def solve(self):
        try:
            resFileName= "result.txt"
            command="lib_points < {} | efst | bb > {}".format(self.tspPath,resFileName)
            os.system(command)
            resFile= open(resFileName,"r")

            terminals, sterminals=extract_coordinates_from_sections(resFile.read())

            self.terminals = terminals
            self.sterminals = sterminals

            print("sommets du graph",terminals)
            print("sommets du Steiner",sterminals)


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










        