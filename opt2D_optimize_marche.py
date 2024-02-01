import numpy as np
from scipy.optimize import minimize

# Define the points a, b, and c
a = np.array([10, 10])
b = np.array([10, 20])
c = np.array([20, 10])
d = np.array([20, 20])
# c = np.array([1, 1, 0]) # Given but not used in the function

# Define the objective function
def objective(vars):
    x, y = vars[:2], vars[2:]  # Split the variables into x and y
    return np.linalg.norm(x - a) + np.linalg.norm(x - b) + np.linalg.norm(y - c) + np.linalg.norm(y -d) + np.linalg.norm(x-y)

# Initial guess for x and y
initial_guess = np.zeros(4)  # Assuming both x and y start from the origin

# Perform the optimization
result = minimize(objective, initial_guess)

# Extract the optimized values of x and y
x_opt, y_opt = result.x[:2], result.x[2:]

print("Optimized x:", x_opt)
print("Optimized y:", y_opt)
print("FUN FINAL  = ",result.fun)