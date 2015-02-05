import numpy as np


data=[1,2,3,4,5,6,7,8,9]
data=np.array(data)
inds=[0,1,1,3,4,5]
inds=np.array(inds)
data2=data[inds]
print data2