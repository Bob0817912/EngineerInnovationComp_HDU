import cv2
import numpy as np
from discrimination import DiscriminateRing
from uart import Uart
TOP_BORDER=0
BOTTOM_BORDER=100
RING_BUFFER=np.zeros((640,480-TOP_BORDER),np.uint32)
RING_CHECK=np.zeros((64,48-TOP_BORDER//10),np.uint32)
def clearBuffer():
    global RING_BUFFER,RING_CHECK,TOP_BORDER
    RING_BUFFER=np.zeros((640,480-TOP_BORDER),np.uint32)
    RING_CHECK=np.zeros((64,48-TOP_BORDER//10),np.uint32)

def ZhuanPanConfirm(mat:cv2.Mat):
    global TOP_BORDER,RING_BUFFER,RING_CHECK
    rings_temp=DiscriminateRing(mat,30,60)
    rings=[]
    for ring in rings_temp:
        if(ring[1]>TOP_BORDER and ring[0]>0 and ring[0]<640 and ring[1]>0 and ring[1]<480):
            rings.append(ring)
    if(len(rings)==1):
        ring=rings[0]
        print(ring)
        RING_CHECK[int(ring[0]/10)][int(ring[1]/10)]+=1
        RING_BUFFER[int(ring[0])][int(ring[1])]+=1
        if(RING_CHECK[int(ring[0]/10)][int(ring[1]/10)]>10):
            t=np.where(RING_BUFFER==np.max(RING_BUFFER))
            x,y=0,0
            if(len(t[0])==1):
                x,y=t[0],t[1]
            else:
                x,y=t[0][0],t[1][0]
            return x,y
    return None,None
def Task_ZhuanPanConfirm(mat:cv2.Mat,u:Uart):
    x,y=ZhuanPanConfirm(mat)
    if(x!=None):
        clearBuffer()
        cv2.circle(mat, (int(x), int(y)), 5, (0, 255, 255), 7)
        print(x,y)
        for i in range(10):
            u.writeStr(str([int(x),int(y)]))
        u.Task_id=0x00
