from pygame.locals import *

import pygame


pygame.init()
clock=pygame.time.Clock()
infoObject = pygame.display.Info()
width=infoObject.current_w
height=infoObject.current_h
screen=pygame.display.set_mode((width/2,height/2))
kill=False

while kill==False:

    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,0,0), (100,100),10)
    
    pygame.display.update()
    msElapsed=clock.tick(100)
        
    for event in pygame.event.get(): 
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            kill=True
            pygame.quit()
            break