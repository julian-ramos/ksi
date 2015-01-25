import os
import select
import socket
import sys
import threading
import globalVars as glob

def messageDecypher(messageData):
        mess=messageData.split(',')
        for i in range(len(mess)):
            if mess[i]=='':
                mess.pop(i)
    
        data=[[0,0] for i in range(4)]
    
        for i in mess:
    
            if i.find('wii')>=0:
                wiiID=i
    
    
            if i.find('|')>=0:
                ind=int(i[int(i.find('|')-1)])
                indx=i.find('x')
                indy=i.find('y')
                data[ind][0]=float(i[indx+1:indy])
                data[ind][1]=float(i[indy+1:])
        
        return wiiID,data




class Client(threading.Thread):
    
    
    
    def __init__(self,(client,address)):
        print('Started client comm')
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 2048
        self.data=[]
#         vals.wiimoteNum = vals.wiimoteNum + 1

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)                
            if data:
#                 print(data)
                try:
                    if data.find('mflt')>=0:
                        print('got something from the mflt client')
                        print(data)
                        #The next section sends the mouse state
                        #for now I just inhabilitated it
    #                         self.client.send(str(vals.mouse_flg))
    #                         print(vals.mouse_flg)
                    elif data.find('click')>=0:
                        print "click cliked"
    #                         vals.newClick_flg = 1 
                    elif data.find('switch')>=0:
                        print "switch switched"
    #                         vals.mouse_flg = not vals.mouse_flg
                    elif data.find('wii')>=0:
                        self.wiiID,self.data=messageDecypher(data)
                except:
                    print "User quit."
                    return
                
                
                if data.find('wii')>=0:
                    if self.wiiID.find('1')>=0:
                        glob.coords[0]=self.data
                    else:
                        glob.coords[1]=self.data
                
            else:
#                 self.client.close()
#                 global kill
#                 kill=True
                running = 0