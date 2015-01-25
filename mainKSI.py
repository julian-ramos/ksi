import sys
import pygame
from pygame.locals import *
import server as Server
import subprocess
import globalVars as glob
import threading

class mainThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        pygame.init()
        clock=pygame.time.Clock()
        infoObject = pygame.display.Info()
        width=infoObject.current_w
        height=infoObject.current_h
        screen=pygame.display.set_mode((width/2,height/2))
        
        kill=glob.kill
        
        
        while kill==False:
            coords=glob.coords
            
            screen.fill((0,0,0))
            pygame.draw.circle(screen, (255,0,0), (int(coords[0][0][0])/3,int(coords[0][0][1])/3),10)
            pygame.draw.circle(screen, (0,255,0), (int(coords[1][0][0])/3,int(coords[1][0][1])/3),10)
            
            pygame.display.update()
            msElapsed=clock.tick(glob.frameRate)
            
            if kill==True:
                pygame.quit()
                sys.exit()
                break
            
            for event in pygame.event.get(): 
                if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                    break



subprocess.call("/home/julian/git/ksi/runner.sh",shell=True)

a=mainThread()
a.start()

s = Server.Server()
s.run()
