# 本部分用来识别图片中的QR码和颜色
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar import pyzbar

lower_red = np.array([0, 43, 46])
upper_red = np.array([15, 255, 255])

lower_blue = np.array([95, 43, 46])
upper_blue = np.array([124, 255, 255])

lower_g = np.array([35, 43, 46])
upper_g = np.array([70, 255, 255])




IMG_PATH_COLOR = "color_capture.jpg"
IMG_PATH_QR = "qr_capture.jpg"


def classify_color(img):
    frame = img
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Masks for each color range
    mask_b = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_r = cv2.inRange(hsv, lower_red, upper_red)
    mask_g = cv2.inRange(hsv, lower_g, upper_g)

    # Resulting images showing only the color within mask
    res_r = cv2.bitwise_and(frame, frame, mask=mask_r)
    res_g = cv2.bitwise_and(frame, frame, mask=mask_g)
    res_b = cv2.bitwise_and(frame, frame, mask=mask_b)

    # Count non-zero values for each color mask
    r_sum = np.array(np.nonzero(mask_r)).shape[1]
    g_sum = np.array(np.nonzero(mask_g)).shape[1]
    b_sum = np.array(np.nonzero(mask_b)).shape[1]

    # Determine the dominant color
    if max(r_sum, g_sum, b_sum) == r_sum:
        return "Red"
    elif max(r_sum, g_sum, b_sum) == g_sum:
        return "Green"
    else:
        return "Blue"


def QRScan(img):
    myData = "No QR code detected"
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(f"QR Code Data: {myData}")
    return myData


def catch_picture(IMG_PATH='qr_capture.jpg'):
    # 读取摄像头
    cap = cv2.VideoCapture(0)
    # 摄像头是否打开
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # 检测是否有二维码
        barcodes = pyzbar.decode(frame)
        if barcodes:
            # 如果是二维码，则保存图片
            cv2.imwrite(IMG_PATH, frame)
            print(f"QR code detected and image saved to {IMG_PATH}")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return frame




print("Capturing image for QR code detection...")
# 读取存下的图片：
img = cv2.imread('qr_capture.jpg')
# img = catch_picture(IMG_PATH_QR)
qr_data = QRScan(img)

print("Capturing image for color classification...")

dominant_color = classify_color(IMG_PATH_COLOR)


print(f"Dominant color in the image: {dominant_color}")