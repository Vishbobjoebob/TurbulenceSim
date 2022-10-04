import numpy as np
from numpy import loadtxt

grid_size = 101

arr = np.loadtxt(r"C:\Users\pasam\Documents\CCL\Turbulence Research\Drag\VelocityData100.csv")

load_original_arr = arr.reshape(grid_size, grid_size, 3)



print(load_original_arr[0][0][0])
