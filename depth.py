import pickle
import signalpro as spo
import numpy as np
import matplotlib.pylab as plt
import depth as dep
import globalVars as gV

def bootstrap(data,wlen,sims):
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

def liveSmoothingBootS(x1,x2,y1,y2,wlen=40,sims=30):
    '''
    wlen : Block length for the bootstrap and filter window size
    sims : Number of bootstrap samples
    '''
    wlen2=5
    bx1=bootstrap(x1, wlen2, sims)
    bx2=bootstrap(x2, wlen2, sims)
    by1=bootstrap(y1, wlen2, sims)
    by2=bootstrap(y2, wlen2, sims)
    
    sx1=spo.smooth(bx1,window_len=wlen,window='blackman')
    sx2=spo.smooth(bx2,window_len=wlen,window='blackman')
    sy1=spo.smooth(by1,window_len=wlen,window='blackman')
    sy2=spo.smooth(by2,window_len=wlen,window='blackman')
    sdepth=[dep.depthEstimate2(sx1[i],sy1[i],sx2[i],sy2[i])  for i in range(len(sx1))]
    return sx1[0],sx2[0],sy1[0],sy2[0],sdepth[0]
    

def liveSmoothing(x1,x2,y1,y2,wlen=40,miniQ=True):
    if miniQ:
        tx1=x1.allData()
        tx2=x2.allData()
        ty1=y1.allData()
        ty2=y2.allData()
    else:  
        tx1=x1
        tx2=x2
        ty1=y1
        ty2=y2
        
    
#     print(len(tx1))
    sx1=spo.smooth(tx1,window_len=wlen,window='blackman')
    sx2=spo.smooth(tx2,window_len=wlen,window='blackman')
    sy1=spo.smooth(ty1,window_len=wlen,window='blackman')
    sy2=spo.smooth(ty2,window_len=wlen,window='blackman')
    sdepth=[dep.depthEstimate2(sx1[i],sy1[i],sx2[i],sy2[i])  for i in range(len(sx1))]
    return sx1[0],sx2[0],sy1[0],sy2[0],sdepth[0]

def keybTouch(x,y,z):
    if gV.betas==[]:
        file=open('betas.dat','rb')
        betas=pickle.load(file)
        file.close()
    else:
        betas=gV.betas
        
    Z=np.inner(betas[0],[1,x,y])
#     print('expected',Z, 'got',z)
    return Z
    
    

def keybplaneCalc(wlen=40):
    '''
    this function calculates the keyboard plane
    using keybp.dat
    '''
    file=open('keybp.dat','rb')
    data=pickle.load(file)
    file.close()
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    depth=[]
    
    for i in data:
        x1.append(i[0][0][0])
        x2.append(i[1][0][0])
        y1.append(i[0][0][1])
        y2.append(i[1][0][1])
        depth.append(dep.depthEstimate(i))
    
    sx1=spo.smooth(x1,window_len=wlen,window='blackman')
    sx2=spo.smooth(x2,window_len=wlen,window='blackman')
    sy1=spo.smooth(y1,window_len=wlen,window='blackman')
    sy2=spo.smooth(y2,window_len=wlen,window='blackman')
    sdepth=[dep.depthEstimate2(sx1[i],sy1[i],sx2[i],sy2[i])  for i in range(len(sx1))]
      
    X=np.vstack((sx1,sy1)).T
    X=np.hstack((np.ones((X.shape[0],1)),X))
    Y=sdepth
    betas=np.linalg.lstsq(X,Y)
#     Z=np.inner(betas[0],X)
    file=open('betas.dat','wb')
    pickle.dump(betas,file)
    file.close()
#     print('betas estimated')
    return True

def depthEstimate(coords):
    x1=coords[0][0][0]
    y1=coords[0][0][1]
    x2=coords[1][0][0]
    y2=coords[1][0][1]
    
    dist=np.sqrt((x1-x2)**2+(y1-y2)**2)
    depthM=1380*13.2/dist
    
    return depthM

def depthEstimate2(x1,y1,x2,y2):
    dist=np.sqrt((x1-x2)**2+(y1-y2)**2)
    depthM=1380*13.2/dist
    
    return depthM

if __name__=='__main__':
#     keybplaneCalc()
    keybTouch(800,800,100)