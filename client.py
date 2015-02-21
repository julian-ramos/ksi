#!/usr/bin/env python

"""
This client connects to a wiiRemote
The macAddress of the wiiMote has to be specified on
the file wiiMAC.dat. This file should have the next format
XXXXXXX
XXXXXXX
Where each line is the MAC address

"""
from time import sleep
import cwiid
import socket
import sys





host = 'localhost'
port = 50010
size = 2048
socketCon=False
# s.send('identity wiiMote1')
wiiMAC=[]   
#wiiMACAddr: Write your wiimote address in the file 'wiiMAC.data'.
#Such as:
#xx:xx:xx:xx:xx:xx
#xx:xx:xx:xx:xx:xx

#Home motes
# wiiMACFile = 'wiiMAC.data'

#Office motes
wiiMACFile = 'wiiMAC2.data'
wiiNum = 0
try:
    wiiNum = int(sys.argv[1])
except:
    print 'Add a wiiNum to select a wiimote device'

done=False
while not done:
    wiiMACAddr = []
    try:
        wiiMACReader = open(wiiMACFile, 'r')
        wiiMACAddr = wiiMACReader.readlines()
        wiiMACReader.close()
        # print wiiMACAddr
    except:
        print 'Error: Wiimote MAC addr file not found.'
        continue
    # wiiMACReader = open(wiiMACFile, 'r')
    # wiiMACAddr = wiiMACReader.readlines()
    # wiiMACReader.close()

    if len(wiiMACAddr) < 2:
        print 'Error: Invalid wiimote MAC addr.'
        continue

    wiiMAC = wiiMACAddr[wiiNum].strip()
    wiiID = 'wiiMote' + str(wiiNum+1)
    
    print "Trying to connect to " + wiiID + " " + wiiMAC
    print "Press 1 & 2 on the Wiimote simultaneously, to find it"
    
    try:
        wii = cwiid.Wiimote(wiiMAC)
        wii.enable(cwiid.FLAG_MESG_IFC)
        wii.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN
        print wiiMAC + " connected successfully"
        data=[0,0]
        done=True
        connected=True
    except:
        print('Couldnt initialize the wiiMote')

rpt=[ [0,0] for i in range(4)]
while 1:
    messages = wii.get_mesg()  
    for mesg in messages:   # Loop through Wiimote Messages
        if mesg[0] == cwiid.MESG_IR: # If message is IR data
                cont=-1
                for m in mesg[1]:   # Loop through IR LED sources
                    cont+=1
                    if m:   # If a source exists
                        rpt[cont][0]=m['pos'][0]
                        rpt[cont][1]=m['pos'][1]
    
    mess2send='%s,0|x%.3fy%.3f,1|x%.3fy%.3f,2|x%.3fy%.3f,3|x%.3fy%.3f,'%(wiiID,\
                                                      rpt[0][0],rpt[0][1],\
                                                      rpt[1][0],rpt[1][1],\
                                                      rpt[2][0],rpt[2][1],\
                                                      rpt[3][0],rpt[3][1])
    if socketCon==False:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
        except:
            s=None
        if not s==None:
            socketCon=True
    else:
        s.send(mess2send)

s.close()
