#2023/12/8
import cv2
from uart import Uart
from Qr import Task_SaoMa
from discrimination import DiscriminateColor,DiscriminateRing,GetZhuanPanCenter,GetThreeColor
from Usual import *
from zhijiao import *
from wifi_thread import Wifi_Thread
from zhuanpanConfirm import Task_ZhuanPanConfirm
Task_Color_1=(1,2,3)#第一次任务编号
Task_Color_2=(2,3,1)#第二次任务编号
Task_Moment=Task_Color_2#当前任务编号
def Set_Task_id(u:Uart):
    u.Task_id=0x00


def Task(mat:cv2.Mat,u:Uart,w:Wifi_Thread=None):
    global Task_Color_1,Task_Color_2,Task_Moment
    if(u.Task_id==0x01):#二维码获取任务码
        temp1,temp2=Task_SaoMa(u)
        if(temp1!=None):
            Task_Color_1=temp1
            Task_Color_2=temp2
            u.Task_id=0x00
    if(u.Task_id==0x04):#WiFi获取任务码
        temp1,temp2=Task_SaoMa(u,w)
        if(temp1!=None):
            Task_Color_1=temp1
            Task_Color_2=temp2
            u.Task_id=0x00
    elif(u.Task_id//0x10==0x0A):#转盘抓取
        check=Task_ZuanPanZhua(mat,u,Task_Color_1,Task_Color_2)
        print(Task_Color_1,Task_Color_2)
        Task_Moment=Task_Color_1
        if(check=='y'):
            u.Task_id=0x00
    elif(u.Task_id//0x10==0x0B):#转盘抓取
        check=Task_ZuanPanZhua_B(mat,u,Task_Color_1,Task_Color_2)
        if(check=='y'):
            u.Task_id=0x00
    elif(u.Task_id==0x02 or u.Task_id==0x03 ):
        if(u.Task_id==0x02):
            res=IntToType(tNum=Task_Color_1)
        elif(u.Task_id==0x03):
            res=IntToType(tNum=Task_Color_2)
        print(res)
        u.writeStr(res)
        u.Task_id=0x00
    elif(u.Task_id==0x11):
        Task_GetRingCenter(mat,u)
    elif(u.Task_id==0x10):
        Task_ZhuanPanCenter(mat,u)
    elif(u.Task_id==0x05):
        Task_ThreeColor(mat,u,Task_Color_1)
    elif(u.Task_id==0x06):
        Task_ThreeColor(mat,u,Task_Color_2)
    elif(u.Task_id==0x07):
        Task_GetRingCenter(mat,u,30)
    elif(u.Task_id==0x12):#回库
        Task_FindCorner(mat,u)

    elif(u.Task_id==0x21):
        Task_ZhuanPanConfirm(mat,u)
        
    # elif(u.Task_id==0x07):
    #     Task_ThreeColor(mat,u,Task_Color_1,True)
    # elif(u.Task_id==0x08):
    #     Task_ThreeColor(mat,u,Task_Color_2,True)
        #u.Task_id=0x00
def Task_ThreeColor(mat:cv2.Mat,u:Uart,task_color_1,istop=False):
    if(not istop):
        t=GetThreeColor(mat)
    else:
        t=GetThreeColor(mat,0,-50,240)
    if(t!='g'):
        send=Type_Task05(task_color_1,TypetoRGB[t])

        print(send)
        u.writeStr(send)
        u.Task_id=0x00
    else:
        pass
def Task_FindCorner(mat:cv2.Mat,u:Uart):
    cx,cy=FindCorner(mat)
    if(cx!=None):
        send=[int(cx),int(cy)]
        print(send)
        u.writeStr(str(send))
def Task_GetRingCenter(mat:cv2.Mat,u:Uart,content_side=120,content_bottom=240):
    rings=DiscriminateRing(mat)
    if(len(rings)>0):
        for r in rings:
            if(abs(r[0]-320)<content_side and r[0]-240<content_bottom):
                cv2.circle(mat, (int(r[0]), int(r[1])), 3, (255, 0, 0), 5)
                send=[int(r[0]),int(r[1])]
                print(send)
                u.writeStr(str(send))
                #u.writeStr(str(send))
def Task_ZhuanPanCenter(mat:cv2.Mat,u:Uart):
    x,y=GetZhuanPanCenter(mat)
    if(x!=None):
        send=[x,y]
        print(send)
        u.writeStr(str(send))

    

def Task_ZuanPanZhua_B(mat:cv2.Mat,u:Uart,t1:tuple,t2:tuple):
    
    if(u.Task_id==0xB0 or u.Task_id==0xB7):
        res='n'
        t=t2
        if(u.Task_id==0xB0):
            t=t1
        # elif(u.Task_id==0xB7):
        #     t=t2
        colorType=DiscriminateColor(mat)
        if(colorType!=RGBT[t[0]-1]):
            res='y'
            u.writeStr(res)
        
        return res
    else:
        u.Task_id-=0x10
        return Task_ZuanPanZhua(mat,u,t1,t2)

def Task_ZuanPanZhua(mat:cv2.Mat,u:Uart,t1:tuple,t2:tuple):
    n=0
    t=t1
    Task_id=u.Task_id
    if(Task_id>0xA3):
        n=Task_id-0xA0-3
        t=t2
    else:
        n=Task_id-0xA0
        t=t1
    colorType=DiscriminateColor(mat)
    print(colorType)
    res='n'
    if(colorType!='N'):
        if(RGBDIR[colorType]==t[n-1]):
            res='y'
    if(res=='y'):
        u.writeStr(res)
    return res

