# 本模块用来识别二维码并返回二维码中的信息

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

def QR_scanner(image):
    # 读取图片
    img = cv2.imread(image)
    # 识别二维码
    decodedObjects = pyzbar.decode(img)
    # 返回二维码中的信息
    return decodedObjects[0].data.decode('utf-8')

# 图片测试
# cap = cv2.imread('QR_code.png')
# print(QR_scanner(cap))


# 相机测试
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if QR_scanner(frame) != None:
        print(QR_scanner(frame))
        break

cap.release()
cv2.destroyAllWindows()



