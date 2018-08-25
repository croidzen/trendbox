import numpy as np

tsp = np.array([[4321, 95, float('NaN')]])
print(tsp)

tsp = np.append(tsp, [[1234, 12, 0.45]], axis=0)
print(tsp)

