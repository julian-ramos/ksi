import numpy as np
import matplotlib.pyplot as plt

x=[2.5,0.5,2.2,1.9,3.1,2.3,2  ,1  ,1.5,1.1]
y=[2.4,0.7,2.9,2.2,3.0,2.7,1.6,1.1,1.6,0.9]


def pcaTrans(X,graph=False):
    means=np.mean(X,0)
    cX=X-means
    cov=np.cov(cX.T)
    eigva,eigve=np.linalg.eig(cov)
    
    print cov
    print(eigve)
    print(eigva)
    print(X.shape)
    
    idx = eigva.argsort()

    eigva=eigva[idx]
    eigve=eigve[:,idx]
    
    print(eigve)
    nX=np.dot(eigve.T,cX.T)
    nX=nX.T+means
    print('\n',nX)
    
    if graph:
        plt.plot(x,y,'x')
#         print(nX)
        plt.plot(nX[:,0],nX[:,1],'rx')
        plt.show()
        

X=np.vstack((x,y)).T
pcaTrans(X,graph=True)

# a=[1,2,3,4]
# a=np.array(a)
# print(a.argsort())