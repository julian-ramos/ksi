import numpy as np
import globalVars as gV
topX=gV.topX
botX=gV.botX
topY=gV.topY
botY=gV.botY
delta=gV.delta

def move(x,y,touchS):
    px=x.allData()[0]
    x=x.allData()[1]
    
    py=y.allData()[0]
    y=y.allData()[1]
    
    if px<=topX and px>=botX and py>=topY and py<=botY:
        
        if gV.relative and touchS:
            x,y=scale(x,y)
            px,py=scale(px,py)
            dx=x-px
            dy=y-py
            cx,cy=gV.mouse.position()
#             print(cx,cy)
            if np.abs(dx)+np.abs(dy)>delta:
                gV.mouse.move(cx+dx,cy+dy)
            
        if gV.absolute:
            x,y=scale(x,y)
            gV.mouse.move(x,y)
            
    #click
    if gV.keystatus[2]:
        tx,ty=gV.mouse.position()
        gV.mouse.click(tx,ty)
        print('click')
        gV.keystatus[2]=False

def scale(x,y):
    x= gV.width*(-x+topX)/(topX-botX)
    y= gV.height*(y-topY)/(botY-topY)
    return x,y