import cv2
import numpy as np
#WIN_SIZE=(720,480)
WIN_SIZE=(int(720),int(480))
Str=cv2.namedWindow("Str",cv2.WINDOW_NORMAL)
#win=cv2.namedWindow("win",cv2.WINDOW_NORMAL)

#cv2.resizeWindow("win",WIN_SIZE[0],WIN_SIZE[1])
#cv2.resizeWindow("win",72,48)
cv2.resizeWindow("Str",WIN_SIZE[0],WIN_SIZE[1])
def showCapture(mat:cv2.Mat):
    cv2.imshow("win",mat)
white_mat:cv2.Mat= np.zeros((WIN_SIZE[1], WIN_SIZE[0], 3), dtype=np.uint8)  
white_mat[:]=(255,255,255)
def showStr(message:str):
    global white_mat
    white_mat=np.zeros((WIN_SIZE[1], WIN_SIZE[0], 3), dtype=np.uint8)  
    cv2.putText(
    white_mat,           # 图像
    message,        # 文字
    (0,200),          # 文字左下角，(w_idx, h_idx)
    cv2.FONT_HERSHEY_SIMPLEX,   # 字体
    5,                  # 字体大小
    (0,0,255),      # 字体颜色
    8,                  # 线宽 单位是像素值
    cv2.LINE_AA         # 线的类型
    )
    cv2.imshow("Str",white_mat)
