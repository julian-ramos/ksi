import miniQueue as mini
import pygame
from pymouse import PyMouse

#Mouse stuff
mouse = PyMouse()


#Control variables
bootstrap=False
smoothing=True

#Wii variables
coords=[[],[]]
coords[0]=[[0,0] for i in range(4)]
coords[1]=[[0,0] for i in range(4)]

#State variables
kill=False
planeCapture=False
planeDone=False
keybpCapture=False
keybpDone=False
touchEstimate=False
signalsRec=False
relative=False
absolute=False


#Touch signal from the smoothing
touchS=False
#Touch signal from the bootstrap
touchB=False

#Drawing variables
frameRate=100
pygame.init()
infoObject = pygame.display.Info()
width=infoObject.current_w
height=infoObject.current_h
myfont=pygame.font.SysFont("monospace",30)
screen=pygame.display.set_mode((width/2,height/2))


#Buffers
planeList=[]
signalsData=[]

sx1=0
sx2=0
sy1=0
sy2=0
sdepth=0

bsx1=0
bsx2=0
bsy1=0
bsy2=0
bsdepth=0


#Depth variables
betas=[]
keybpData=[]

#Signal processing Variables 
#Window length
wlen=11

#bootstrap
#Number of boot strap samples
bootsNum=50

print('bootstrap',bootstrap)
print('smothing',smoothing)
print('wlen',wlen)