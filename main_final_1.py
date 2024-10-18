import cv2
import window
import time
import numpy as np  
from discrimination import *
from zhijiao import *
from uart import Uart
from task import Task,Set_Task_id
from wifi_thread import Wifi_Thread
Timeout_t=10
CAM:cv2.VideoCapture
def GetCamera()->cv2.VideoCapture:
    i:int=0
    res:cv2.VideoCapture=None
    start=time.time()
    while(time.time()-start<Timeout_t):
        try:
            res=cv2.VideoCapture(i%10)
            if(res.isOpened()):
                print("get the capture[{}]".format(i%10))
                b=False
                i=0
                while(i<5):
                    b,frame=res.read()
                    #cv2.imshow("tmp",frame)
                    if(b==True):
                        i+=1
                #CAM=res
                return res
        except:
            print("can't find capture[{}]".format(i%10))
        i+=1
    print("get capture timeout")
    #CAM=None
    return None 
GET_IMG_BUF:cv2.Mat=np.zeros((720,480))
def GetImg():
    global CAM
    global GET_IMG_BUF
    frame:cv2.Mat=None
    b:bool=False
    if(CAM!=None):
        #print("摄像头打开了")
        b,frame=CAM.read()
    else:
        print("摄像头未打开")
    if(b):
        
        GET_IMG_BUF=frame
        return True,frame
    else:
        
        print("重新加载摄像头中...")
        CAM=GetCamera()
        return False,GET_IMG_BUF





u=Uart()
u.start()
# w=Wifi_Thread()
# w.start()
Set_Task_id(u)

mat_buf:cv2.Mat=np.zeros((480, 640, 3), dtype=np.uint8)  
mat_buf[:]=(255,255,255)
CAM=GetCamera()
#print("WIDTH",CAM.get(cv2.CAP_PROP_FRAME_WIDTH))
#print("HEIGHT",CAM.get(cv2.CAP_PROP_FRAME_HEIGHT))
#640x480

while(True):
    _,mat_buf=GetImg()
    #DiscriminateColor(mat_buf)
    #t=time.time()
    #print(Scan())
    #DiscriminateRing(mat_buf)
    #GetRingColor(mat_buf)
    #GetZhuanPanCenter(mat_buf)
    #DiscriminateRing(mat_buf)
    #print(1/(time.time()-t))
    #GetThreeColor(mat_buf,0,-50,240)
    Task(mat_buf,u,None)
    #FindCorner(mat_buf)
    #GetThreeColor_Auto(mat_buf)
    #window.showCapture(mat_buf)
    #window.showStr("")
    c=cv2.waitKey(1)
    if c==27:
        break
u.close()
