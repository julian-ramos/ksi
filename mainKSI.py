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
#         pygame.init()
        clock=pygame.time.Clock()
        screen=glob.screen
        myfont=glob.myfont
#         buf=[mini.miniQueue(10) for i in range(4)]
        bufDepth=mini.miniQueue(10)

        
        kill=glob.kill
        
        
        while kill==False:
            coords=glob.coords
            
            
            screen.fill((0,0,0))
            draw.circles(screen,coords)
            
            events.estimates(coords)
            
            dep=dp.depthEstimate(coords)
                        
            mess='Depth = %.4f'%(dep)
            draw.text(screen,mess,myfont,10,80)
            
            bufDepth.put(dep)
            mess='averaged depth = %.4f'%(bufDepth.mean())
            draw.text(screen,mess,myfont,10,100)
            
            
            
            
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
