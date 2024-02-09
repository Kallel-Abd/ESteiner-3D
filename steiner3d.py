from EST3D import EST3D 
from EST2D import EST2D


estprob = EST2D("square.tsp")


estprob2 = EST2D("square.tsp")

estprob3d = EST3D(estprob, estprob2)
estprob3d.solve_geosteiner()
estprob3d.solve_minimize()
estprob3d.draw()