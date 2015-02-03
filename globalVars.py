import miniQueue as mini
import pygame


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

#Depth variables
betas=[]
keybpData=[]

#Signal processing Variables 
wlen=21