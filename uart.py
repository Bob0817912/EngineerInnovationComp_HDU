import serial
import threading
Uart_interface=None
class Uart:
    S4_Uart:serial.Serial
    close_flag=True
    # QR_buffer:str
    # __QR_code:str
    __thread=threading.Thread
    Task_id=0x00
    def __init__(self,task_id=0x00) -> None:
        global Uart_interface
        #self.QR_Uart = serial.Serial("/dev/ttyACM0", 115200)
        try:
            self.S4_Uart = serial.Serial("/dev/ttyS4", 115200)
        except:
            print("未检测到串口！")
            self.S4_Uart=None
        self.__thread = threading.Thread(name="UartThread",target=Uart_function,args=(self,))
        # self.QR_buffer=''
        # self.__QR_code=''
        Uart_interface=self
        self.Task_id=task_id

    # def QR_code(self):
    #     if(self.__QR_code==''):
    #         return None
    #     else:
    #         return self.__QR_code
    def start(self):
        self.__thread.start()
        self.close_flag=True
    def close(self):
        self.close_flag=False
    def writeStr(self,s:str):
        self.S4_Uart.write(s.encode())
def Uart_function(uart:Uart):
    global TASK_ID
    while(uart.close_flag):
        buffer=uart.S4_Uart.read()
        uart.Task_id=buffer[-1]
        print(uart.Task_id)
        #uart.S4_Uart.write("y".encode())
        # uart.QR_thread_update()


#static




    