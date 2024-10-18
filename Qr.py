import serial
import time
import uart
from uart import Uart
import serial
import socket
from window import showStr


def __GetTaskColor(qrstr:str):
    t1=(int(qrstr[0]),int(qrstr[1]),int(qrstr[2]))
    t2=(int(qrstr[4]),int(qrstr[5]),int(qrstr[6]))
    return t1,t2


def Task_Scan(u:Uart):
    message=Scan(u)
    if(message==None):
        return None,None
    showStr(message)
    u.S4_Uart.write("y".encode())
    t1,t2=__GetTaskColor(message)
    return t1,t2


def Scan(u:Uart)->str:
    try:
        qr_uart=serial.Serial("/dev/ttyACM0", 115200)

        res=""
        s=time.time()
        while(True):
            temp=qr_uart.read().decode()
            if(time.time()-s>15):
                raise Exception
            if(u.Task_id!=0x01):
                return None
            if(temp=='\r'):
                break
            res+=temp
    except:
        res="123+321"
    print(res)
    return res

