import numpy as np
from scipy.optimize import minimize

# Define the points a, b, and c
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
print(s1)
print(s2)
print(s3)
print(s4)
print(s5)
print(s6)
print(result)
