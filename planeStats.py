import scipy.stats as sp
import scipy as sci
import signalpro as spo
import depth as dep
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pickle

def bootstrapFilter(data,wlen,sims):
    '''
    Creates a bootstrap sample
    '''
    if wlen>len(data):
        print('error : wlen greather than data')
        return False
    data=np.array(data)
    outSignal=[]
    for i2 in range(len(data)-wlen):
        bstrap=[]
        sample=data[i2:i2+wlen]
        for i in range(sims):
            inds=np.random.randint(wlen,size=wlen)
            bstrap.append(np.mean(sample[inds]))
#             bstrap.append(spo.smooth(sample[inds],window_len=wlen,window='blackman'))
        outSignal.append(np.mean(bstrap))
    return outSignal

def pcaTrans(X,graph=False):
    means=np.mean(X,0)
    cX=X-means
    cov=np.cov(cX.T)
    eigva,eigve=np.linalg.eig(cov)
    
    
    
    idx = eigva.argsort()
    idx=idx[::-1]
    
    eigva=eigva[idx]
    eigve=eigve[:,idx]  
    
    
    nX=np.dot(eigve.T,cX.T)
    nX=nX.T+means
#     print('/n',nX)
    
    if graph:
        plt.plot(x,y,'x')
#         print(nX)
        plt.plot(nX[:,0],nX[:,1],'rx')
        plt.show()
    return nX

file=open('keybp.dat','rb')
data=pickle.load(file)
wii1=[]
wii2=[]
depth=[]
x1=[]
x2=[]
y1=[]
y2=[]

for i in data:
    wii1.append(i[0][0])
    wii2.append(i[1][0])   
    
    x1.append(i[0][0][0])
    x2.append(i[1][0][0])
    y1.append(i[0][0][1])
    y2.append(i[1][0][1])
    
    depth.append(dep.depthEstimate(i))
    
wlen2=10
sims=30

wlen=20


bx1=bootstrapFilter(x1, wlen2,sims)
bx2=bootstrapFilter(x2, wlen2,sims)
by1=bootstrapFilter(y1, wlen2,sims)
by2=bootstrapFilter(y2, wlen2,sims)
bdepth=[dep.depthEstimate2(bx1[i],by1[i],bx2[i],by2[i]) for i in range(len(bx1))]

sbx1=spo.smooth(bx1,window_len=wlen2,window='blackman')
sbx2=spo.smooth(bx2,window_len=wlen2,window='blackman')
sby1=spo.smooth(by1,window_len=wlen2,window='blackman')
sby2=spo.smooth(by2,window_len=wlen2,window='blackman')
sbdepth=[dep.depthEstimate2(sbx1[i],sby1[i],sbx2[i],sby2[i]) for i in range(len(sbx1))]

wii1=np.array(wii1)
wii2=np.array(wii2)
depth=np.array(depth)
x1=np.array(x1)
x2=np.array(x2)
y1=np.array(y1)
y2=np.array(y2)

dist=np.sqrt((x1-x2)**2+(y1-y2)**2)


#Experiments


smoDepth=spo.smooth(depth,window_len=wlen,window='blackman')
sx1=spo.smooth(x1,window_len=wlen,window='blackman')
sx2=spo.smooth(x2,window_len=wlen,window='blackman')
sy1=spo.smooth(y1,window_len=wlen,window='blackman')
sy2=spo.smooth(y2,window_len=wlen,window='blackman')
sdepth=[dep.depthEstimate2(sx1[i],sy1[i],sx2[i],sy2[i])  for i in range(len(sx1))]

# plt.plot(smoDepth)
# plt.show()




#3D plane

 
 



#Normal depth no smoothing
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(x1,y1,zs=depth)
plt.title('Normal depth no smoothing')
# plt.show()

#Smoother depth
X=np.vstack((wii1[:,0],wii1[:,1]))
X=np.vstack((np.ones((1,len(wii1[:,0]))),X))
Y=smoDepth[0:-wlen+1]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(X[1,:],X[2,:],zs=Y,c='r')
plt.title('Smoothed depth')


# plt.plot(X[1,:],X[2,:],zs=Y,c='r')
# plt.plot(NX[:,0],NX[:,1],zs=NX[:,2])
# plt.show()

#Smoothing on the original signals
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(sx1,sy1,zs=sdepth)
plt.title('Smoothing on source')
# plt.show()



#Original signals\
# plt.plot(x1,y1,'b')
# plt.plot(x2,y2,'r')
# plt.show()

#Smoothing over x and y

#PCA rotated over source smoothed data
# NX=np.vstack((X[1:3,:],Y)).T
NX=np.vstack((sx1,sy1))
NX=np.vstack((NX,sdepth)).T
NX=pcaTrans(NX)
ax = fig.add_subplot(111, projection='3d')
plt.plot(NX[:,0],NX[:,1],zs=NX[:,2])
plt.title('PCA rotated over source smoothed data')
# plt.scatter(V[:,1],V[:,1],zs=V[:,2])

X=np.vstack((sx1,sy1)).T
X=np.hstack((np.ones((X.shape[0],1)),X))
Y=sdepth
betas=np.linalg.lstsq(X,Y)

# file=open('betas.dat','rb')
# betas2=pickle.load(file)
# print(betas[0])
# print(betas2[0])
Z=np.inner(betas[0],X)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# plt.scatter(X[1,:],X[2,:],zs=Y)
ax.plot(x1,y1,zs=depth,c='r')
ax.plot(sx1,sy1,zs=sdepth,c='b')
ax.plot(X[:,1],X[:,2],zs=Z,c='k')

# ax.plot_wireframe(x1,y1,depth)
# plt.show()

#Bootstrapped plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x1,y1,zs=depth,c='r')
# ax.plot(bx1,by1,zs=bdepth,c='b')
ax.plot(sbx1,sby1,zs=sbdepth,c='b')
ax.plot(X[:,1],X[:,2],zs=Z,c='k')
plt.title('bootstrap')



plt.show()