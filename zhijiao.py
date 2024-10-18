import cv2
import numpy as np
import math
import time
def get_cross_point_linesegment(line1, line2):
    """
    求两条线段的交点, 兼容水平线和垂直线
    :param line1: ((x1,y1),(x2,y2))
    :param line2: ((x1,y1),(x2,y2))
    """
    # x = (b0*c1 – b1*c0)/D
    # y = (a1*c0 – a0*c1)/D
    # D = a0*b1 – a1*b0， (D为0时，表示两直线重合)

    line0_x1y1, line0_x2y2 = line1
    line1_x1y1, line1_x2y2 = line2
    line0_a = line0_x1y1[1] - line0_x2y2[1]
    line0_b = line0_x2y2[0] - line0_x1y1[0]
    line0_c = line0_x1y1[0] * line0_x2y2[1] - line0_x2y2[0] * line0_x1y1[1]
    line1_a = line1_x1y1[1] - line1_x2y2[1]
    line1_b = line1_x2y2[0] - line1_x1y1[0]
    line1_c = line1_x1y1[0] * line1_x2y2[1] - line1_x2y2[0] * line1_x1y1[1]

    d = line0_a * line1_b - line1_a * line0_b
    if d == 0:
        # 重合的边线没有交点
        return None,None
    x = (line0_b * line1_c - line1_b * line0_c) * 1.0 / d
    y = (line0_c * line1_a - line1_c * line0_a) * 1.0 / d
    return x, y

def fliter(gray:cv2.Mat,mode=1):
    if(mode==1):
        _,gray=cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
        kernel=np.ones((10,10),np.uint8)
        gray=cv2.erode(gray,kernel)
        kernel=np.ones((5,5),np.uint8)
        gray=cv2.dilate(gray,kernel)
        gray=cv2.dilate(gray,kernel)
    if(mode==2):
        _,gray=cv2.threshold(gray,140,255,cv2.THRESH_BINARY_INV)
        kernel=np.ones((20,20),np.uint8)
        gray=cv2.dilate(gray,kernel)
        # kernel=np.ones((5,5),np.uint8)
        # gray=cv2.erode(gray,kernel)
        # gray=cv2.erode(gray,kernel)
    cv2.imshow("gray",gray)
    return gray.copy()
def findMaxlength(line_t_list:list):
    maxVal=0
    resIndex=0
    i=0
    for i in range(len(line_t_list)):
        if(line_t_list[i][4]>maxVal):
            maxVal=line_t_list[i][4]
            resIndex=i
   
    return resIndex
def FindCorner(img:cv2.Mat):

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    y=0
    x=0
    gray=img[y:y+400, x:x+440]
    gray=cv2.GaussianBlur(gray,(9,9),0 )
    b,g,r=cv2.split(gray)

    

    #gray[gray > 170] = 0  
    # cv2.imshow("gray0",gray)
    #gray[gray < 150] = 0
    
    #二值化、膨胀腐蚀去噪
    #gray=fliter(gray,1)
    #_,gray=cv2.threshold(gray,180,255,cv2.THRESH_BINARY_INV)
    #_,gray=cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    #b=cv2.inRange(b,200,255)
    g=cv2.inRange(g,0,100)
    r=cv2.inRange(r,0,100)
    t=cv2.bitwise_and(r,g)
    #gray=cv2.bitwise_or(t,b)
    gray=t
    #cv2.imshow("gray",gray)
    kernel=np.ones((10,10),np.uint8)
    gray=cv2.erode(gray,kernel)
    kernel=np.ones((5,5),np.uint8)
    gray=cv2.dilate(gray,kernel)
    # gray=cv2.dilate(gray,kernel)
    cv2.imshow("gray",gray)
    #边缘检测
    edge=cv2.Canny(gray,1,2,apertureSize=3)
    kernel=np.ones((3,3),np.uint8)
    edge=cv2.dilate(edge,kernel)
    cv2.imshow("edge",edge)
    #霍夫变换检测直线
    try:
        lines=cv2.HoughLinesP(edge,1,np.pi/180,100,minLineLength=10,maxLineGap=10)
        if(len(lines)<2):#检测的线小于两条会被滤掉
            return None,None
    except:
        return None,None
    x1,y1,x2,y2=lines[0][0]
    line_a=(x1,y1,x2,y2,math.atan2(abs(x1-x2),abs(y1-y2)))
    line_b=(0,0,0,0,0)
    for line in lines:
        x1,y1,x2,y2=line[0]
        line_t=(x1,y1,x2,y2,math.atan2(abs(x1-x2),abs(y1-y2)))
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)
        if(abs(line_t[4]-line_a[4])>0.2):
            line_b=line_t
            break
        
        
        #print(x1,y1,x2,y2,(x1-x2)*(x1-x2)+(y1-y2)*(y1-y2),math.atan2(abs(x1-x2),abs(y1-y2)))
    # if(abs(line_a[4]-line_b[4])>0.6):
    #     return None,None
    cv2.line(img,(line_a[0],line_a[1]),(line_a[2],line_a[3]),(0,255,0),5)
    cv2.line(img,(line_b[0],line_b[1]),(line_b[2],line_b[3]),(0,255,255),5)
    if(line_b==(0,0,0,0,0)):#如果只检测到了一条线也会被滤掉
        return None,None
    cx,cy=get_cross_point_linesegment(((line_a[0],line_a[1]),(line_a[2],line_a[3])),((line_b[0],line_b[1]),(line_b[2],line_b[3])))
    if(cx==None):
        return None,None
    # if(abs(cx-320)>200 or abs(cy-240)>200):#坐标不在屏幕里面滤掉
    #     return None,None
    cv2.circle(img,(int(cx),(int(cy))),30,(0,0,255),30)
    return cx,cy
    

img = cv2.imread('asset/3.png')
img=cv2.resize(img,(640,480))

cx,cy=FindCorner(img)
s=time.time()
cv2.circle(img,(int(cx),(int(cy))),30,(0,0,255),30)
print(1/(time.time()-s))
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# def process_video_stream():
#     cap = cv2.VideoCapture('./asset/road.mp4')  # Use 0 for webcam, or provide the path to a video file
#     while True:
#         ret, img = cap.read()
#         if not ret:
#             break

#         img = cv2.resize(img, (640, 480))
#         cx, cy = FindCorner(img)

#         # if cx is not None and cy is not None:
#             # cv2.circle(frame, (int(cx), int(cy)), 30, (0, 0, 255), 30)

#         # cv2.imshow("Processed Video", frame)
        

#         # Press 'q' to exit the loop
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Run the video processing
# process_video_stream()

