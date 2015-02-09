import mouse
import numpy as np
import miniQueue as mini
import depth as dp
import sys
import pygame
from pygame.locals import *
import server as Server
import subprocess
import globalVars as glob
import threading
import draw
import events

def coords2buf(coords,buf):
    buf[0].put(coords[0][0][0])
    buf[1].put(coords[0][0][1])
    buf[2].put(coords[1][0][0])
    buf[3].put(coords[1][0][1])

class mainThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        clock=pygame.time.Clock()
        screen=glob.screen
        myfont=glob.myfont
        wlen=glob.wlen
        bufDepth=mini.miniQueue(wlen)
        x1=mini.miniQueue(wlen)
        x2=mini.miniQueue(wlen)
        y1=mini.miniQueue(wlen)
        y2=mini.miniQueue(wlen)
        mx=mini.miniQueue(2)
        my=mini.miniQueue(2)
        
        kill=glob.kill
        
        
        while kill==False:
            coords=glob.coords
            x1.put(coords[0][0][0])
            y1.put(coords[0][0][1])
            x2.put(coords[1][0][0])
            y2.put(coords[1][0][1])
            
            
            screen.fill((0,0,0))
            draw.circles(screen,coords)
            
            events.estimates(coords)
            
            dep=dp.depthEstimate(coords)
                        
            mess='Depth = %.4f'%(dep)
            draw.text(screen,mess,myfont,10,80)
            
            bufDepth.put(dep)
            depthA=bufDepth.mean()
            mess='averaged depth = %.4f'%(depthA)
            draw.text(screen,mess,myfont,10,100)
            
            draw.text(screen,'x1 -y1 %.2f - %.2f'%(x1.mean(),y1.mean()),myfont,glob.width/2-200,20)
            draw.text(screen,'x2 -y2 %.2f - %.2f'%(x2.mean(),y2.mean()),myfont,glob.width/2-200,40)

            #Need to calculate x1 and y1 smoothed and then from that calculate
            #depth all in real time
            if x1.size()>wlen-1 and glob.touchEstimate:
                #Smoothing
                if glob.smoothing:
                    sx1,sx2,sy1,sy2,sdepth=dp.liveSmoothing(x1,x2,y1,y2,wlen)
                    glob.sx1=sx1
                    glob.sx2=sx2
                    glob.sy1=sy1
                    glob.sy2=sy2
                    glob.sdepth=sdepth
                    
                    depthK=dp.keybTouch(sx1,sy1,sdepth)
                    mess='smoothed depth = %.4f - expected %.4f'%(sdepth,depthK)
                    draw.text(screen,mess,myfont,10,120)
                    
                    if depthK-sdepth< 0.2:
                        mess='Touching <from smoothed>= %.4f'%(depthK-sdepth)
                        draw.text(screen,mess,myfont,10,160)
                        glob.touchS=True
                    else:
                        glob.touchS=False                
                
                #Bootstrap
                if glob.bootstrap:
                    bsx1,bsx2,bsy1,bsy2,bsdepth=dp.liveSmoothing(x1.bootstrap(),x2.bootstrap(),y1.bootstrap(),y2.bootstrap(),wlen,miniQ=False)
                    glob.bsx1=bsx1
                    glob.bsx2=bsx2
                    glob.bsy1=bsy1
                    glob.bsy2=bsy2
                    glob.bsdepth=bsdepth
    
                    
                    depthK=dp.keybTouch(bsx1,bsy1,bsdepth)
                    mess='bootS depth = %.4f - expected %.4f'%(bsdepth,depthK)
                    draw.text(screen,mess,myfont,10,140)
                    
                    if depthK-bsdepth< 0.2:
                        mess='Touching <from bootS>= %.4f'%(depthK-bsdepth)
                        draw.text(screen,mess,myfont,10,180)
                        glob.touchB=True
                    else:
                        glob.touchB=False
                        
                mx.put(sx1)
                my.put(sy1)
                        
                #Mouse events
                if mx.size()==2:
                    mouse.move(mx,my,glob.touchS)
                
                #Notes to self
                #First scale to screen
                #Implement absolute
                #Implement relative
                
                
                    
                   
            
            if kill==True:
                pygame.quit()
                sys.exit()
                break
            
            events.keyboardEvents(pygame.event.get(),screen,myfont)
            
#             eventsObject=pygame.event.get()
#             for event in eventsObject:
#                 if event.type == KEYDOWN:
#                     if event.key == pygame.K_s:
#                         draw.text(screen,'s pressed',myfont,10,120)
#                         print('s pressed')
#                 if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
#                     pygame.quit()
#                     sys.exit()
                    
            pygame.display.update()
            msElapsed=clock.tick(glob.frameRate)
            




subprocess.call("/home/julian/git/ksi/runner.sh",shell=True)

a=mainThread()
a.start()

s = Server.Server()
s.run()
