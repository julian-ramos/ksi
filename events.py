import pickle
import miniQueue as mini
import globalVars as gV
import sys
from pygame.locals import *
import pygame
import draw
import depth as dp

def keyboardEvents(eventsObject,screen,myfont):
    
    if gV.keystatus[0] and gV.fingersOn:
        gV.fingersOn=False
    elif gV.keystatus[0] and gV.fingersOn==False:
        gV.fingersOn=True
    
    
    
    for event in eventsObject:
        
        if event.type == KEYDOWN:
            if event.key == pygame.K_q:
#                 draw.text(screen,'s pressed',myfont,10,120)
#                 print('s pressed')
                gV.planeCapture=True
            if event.key == pygame.K_w:
#                 draw.text(screen,'s pressed',myfont,10,120)
#                 print('s pressed')
                gV.planeCapture=False
                gV.planeDone=True
                
            if event.key == pygame.K_a:
                gV.keybpCapture=True
                
            if event.key == pygame.K_s:
                gV.keybpCapture=False
                gV.keybpDone=True
                
            #Starts calculating touch
            if event.key == pygame.K_z:
                gV.touchEstimate=True
                
            if event.key == pygame.K_x:
                gV.touchEstimate=False
                
            #Record mainKSI signals
            if event.key == pygame.K_e:
                gV.signalsRec=True
                
            if event.key == pygame.K_r:
                gV.signalsRec=False
                
                
            #Absolute 
            if event.key == pygame.K_d:
                gV.absolute=True
                gV.relative=False
                
            if event.key == pygame.K_f:
                gV.absolute=False
                
            #Relative
            if event.key == pygame.K_c:
                gV.absolute=False
                gV.relative=True
                
            if event.key == pygame.K_v:
                gV.relative=False
                
            if event.key == pygame.K_KP_PLUS:
                if gV.deltaToggle:
                    gV.delta+=1
                if gV.touchthToggle:
                    gV.touchRange+=0.05
            if event.key == pygame.K_KP_MINUS:
                if gV.deltaToggle:
                    gV.delta-=1
                if gV.touchthToggle:
                    gV.touchRange-=0.05
            
            #Change movement delta with +/-
            if event.key == pygame.K_1 and gV.deltaToggle==False:
                gV.deltaToggle=True
                gV.touchthToggle=False
                print('delta Toggle true')
            
#             if event.key == pygame.K_1 and gV.deltaToggle==True:
#                 gV.deltaToggle=False
#                 print('delta Toggle false')
                
            #Change touch range thold with +/-
            if event.key == pygame.K_2 and gV.touchthToggle==False:
                gV.touchthToggle=True
                gV.deltaToggle=False
                print('touch Toggle true')
            
#             if event.key == pygame.K_2 and gV.touchthToggle==True:
#                 gV.touchthToggle=False
#                 print('touch Toggle false')
                
            
            
                
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
#                     break
                    
def estimates(coords):
    
    #The next simply stores data in plane.dat
    if gV.planeCapture:
        gV.planeList.append(coords[:])
        draw.text(gV.screen,'Recording points',gV.myfont,10,120)
        
        
    if gV.planeDone:    
#         print(gV.planeList)
        file=open('plane.dat','wb')
        pickle.dump(gV.planeList,file)
        file.close()
        draw.text(gV.screen,' File stored',gV.myfont,10,120)
        gV.planeDone=False
    
    
    #The next stores data in keybp.dat and calculates the
    #keyboard plane which will later be used to find out
    #whether someone is touching or not the keyboard
    
    if gV.keybpCapture:
        gV.keybpData.append(coords[:])
        draw.text(gV.screen,'Capturing keyboard plane',gV.myfont,10,120)
    
    if gV.keybpDone:
        #Storing plane data
        file=open('keybp.dat','wb')
        pickle.dump(gV.keybpData,file)
        file.close()
        #Calculating and storing betas
        dp.keybplaneCalc(gV.wlen)
        draw.text(gV.screen,' File stored',gV.myfont,10,120)
        gV.keybpDone=False
        
    if gV.signalsRec:
        gV.signalsData.append([gV.touchS,gV.touchB,coords[:],gV.sx1,gV.sx2,gV.sy1,gV.sy2,\
                               gV.sdepth,gV.bsx1,gV.bsx2,gV.bsy1,gV.bsy2,gV.bsdepth])
        draw.text(gV.screen,' Recording signals',gV.myfont,10,140)
        draw.text(gV.screen,'Current size %d'%(len(gV.signalsData)),gV.myfont,10,160)
    elif gV.signalsRec == False and gV.signalsData!=[]:
        draw.text(gV.screen,' Storing file',gV.myfont,10,180)
        file=open('signalsData-tapping-%d.dat'%(gV.wlen),'wb')
        pickle.dump(gV.signalsData,file)
        file.close()
        gV.signalsData=[]
        

    
        
          
        
        