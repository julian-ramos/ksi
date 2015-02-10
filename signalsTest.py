from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import depth as dep
import pickle

def signalUnpacker(data):
    touchS=[]
    touchB=[]
    coords=[]
    sx1=[]
    sx2=[]
    sy1=[]
    sy2=[]
    sdepth=[]
    
    bsx1=[]
    bsx2=[]
    bsy1=[]
    bsy2=[]
    bsdepth=[]
    
    for i in data:
        a=i[0]
        b=i[1]
        c=i[2]
        
        touchS.append(a)
        touchB.append(b)
        coords.append(c)
        
        sx1.append(i[3])
        sx2.append(i[4])
        sy1.append(i[5])
        sy2.append(i[6])
        sdepth.append(i[7])
        
        bsx1.append(i[8])
        bsx2.append(i[9])
        bsy1.append(i[10])
        bsy2.append(i[11])
        bsdepth.append(i[12])
        
    return touchS, touchB, coords,sx1,sx2,sy1,sy2,sdepth,bsx1,bsx2,bsy1,bsy2,bsdepth

def coordsUnpacker(data):
    x1=[]
    x2=[]
    y1=[]
    y2=[]
    depth=[]
    for i in data:
        x1.append(i[0][0][0])
        x2.append(i[1][0][0])
        y1.append(i[0][0][1])
        y2.append(i[1][0][1])
        depth.append(dep.depthEstimate(i))
    return x1,y1,x2,y2,depth

file=open('signalsData-tapping-11.dat','rb')
data=pickle.load(file)
touchS,touchB,coords,sx1,sx2,sy1,sy2,sdepth,bsx1,bsx2,bsy1,bsy2,bsdepth=signalUnpacker(data)
touchSNum=np.array(touchS)+0
touchBNum=np.array(touchB)+0


plt.figure()
plt.plot(sdepth-np.mean(sdepth),'b')
plt.plot(bsdepth-np.mean(bsdepth),'r')
plt.plot(touchB,'r')
plt.plot(touchS,'b')

fig=plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(sx1,sy1,sdepth,c='b')
ax.plot(bsx1,bsy1,bsdepth,c='r')
plt.show()