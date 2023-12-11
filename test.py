import numpy as np

temp = np.array([1,2,3,4,5,4,3,2,1])
ind = np.where(temp == 2)
print(ind[0][1])