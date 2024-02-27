from EST3D import EST3D
from EST2D import EST2D


estprob = EST2D("square.tsp")


estprob2 = EST2D("square.tsp")

estprob3d = EST3D(estprob, estprob2, 1)
estprob3d.solve_geosteiner()
estprob3d.solve_minimize()
# uncomment if you want to draw the result
# estprob3d.draw()
print(estprob3d.dist)
