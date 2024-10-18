import socket
import threading

class Wifi_Thread:
    port:int
    buffer:bytes
    message:str
    udp_socket:socket.socket
    thread:threading.Thread
    def __init__(self,port=4210) -> None:
        self.udp_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port=port
        self.udp_socket.bind(("",port))
        self.thread=threading.Thread(name="wifi-thread",target=wifi_thread_fun,args=(self,))
        self.buffer=None
        self.message=""
    def start(self):
        self.thread.start()
def wifi_thread_fun(wt:Wifi_Thread):
    while(True):
        try:
            wt.buffer,_=wt.udp_socket.recvfrom(1024)
            #print(wt.buffer)
            if(wt.buffer!=None and wt.message=="" and wt.buffer.decode()[3]=="+"):
                wt.message=wt.buffer.decode()
                print("接收到WiFi任务码")

                

        except:
            pass
