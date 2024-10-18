import cv2
import numpy as np
import math
 
cap = cv2.VideoCapture('./asset/road.mp4')#(这是我提前拍摄的模拟小车运行时摄像头的画面)
# cap = cv2.VideoCapture(0)
 
def FindRoad():
    area2 = []
    b = []
    Inf = -1
    if len(contour1) >= 1:                             #找到目标至少为一
        for i in range(len(contour1)):
            if cv2.contourArea(contour1[i])>50:
                area2.append(cv2.contourArea(contour1[i]))  #将找到目标面积储存到area2
        if len(area2)!=0:
            for j in range(4):   #只对前4个最大的面积进行操作
                b.append(area2.index(max(area2)))           #把目标按照面积大小从大到小存入列表b
                area2[area2.index(max(area2))] = Inf        #把刚刚存入列表的面积重新赋值为-1
        else:
            return 1
        b.sort()   #因为目标赛道检测到的面积有可能并不是按照顺序排列，所以在这里进行排列
        return b
    else:
        return 1
 
def JudgeRoad(n):
    s = []
    try:
        if n[2]-n[1]!=n[1]-n[0]:
            s.append(n[1])                    #列表s储存赛道边缘位置横坐标
        else:
            s.append(min(n))
        try:
            for i in range(len(n)):
                if n[i + 1] - n[i] >= 55:  #赛道的间距>50
                    s.append(n[i])
                    s.append(n[i + 1])
                if i==len(n)-2:
                    if n[len(n)-1] - n[len(n)-2]<5:
                        s.append(n[len(n)-1])
                        break
                    else:
                        s.append(n[len(n)-2])
                        break
        except:
            pass
        return s                   #返回赛道横坐标列表
    except Exception :
        return 1                   #错误时一定要返回值
        pass
 
def calc_angle(x1,y1,x2,y2):
    angle = 0
    k = 0
    h = 0
    y = y1-y2
    x = x1-x2
    if x == 0:
        pass
    else:
        k = y/x
        h = math.atan(k)
        angle = 90 - abs(math.degrees(h))
    return angle
 
while True:
    success , img = cap.read()
    img = cv2.resize(img, (640, 480))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerblack = np.array([0, 0, 0])
    upperblack = np.array([255, 255, 100])
    maskblack = cv2.inRange(imgHSV, lowerblack, upperblack)
    contour1, hierarchy1 = cv2.findContours(maskblack, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    color = maskblack[380]                          #遍历掩膜第380行全部像素值
    color2 = maskblack[420]
 
    blackindex = np.where(color == 100)                      #储存像素为255的索引值
    blackindex2 = np.where(color2 == 255)
    npindex = np.array(blackindex)
    npindex2 = np.array(blackindex2)
    a = npindex.ravel()                                 #将数组维度拉成一维数组
    c = npindex2.ravel()
 
    FindRoad()
    o = FindRoad()  #为赛道的索引
    b = JudgeRoad(a)  #赛道边缘的横坐标，为偶数个
    b1 = []   #储存赛道中点横坐标
    blackindex2 = JudgeRoad(c)
 
    npindex2 = []
 
    if o == 1:
        print('未找到赛道')
        pass
    else:
        if len(str(b)) <= 1:       #b类型转换成字符串(防止报错)
            b1.append(1)
        else:
            for i in range(len(b)):
                if i % 2 == 0:
                    b1.append((b[i] + b[i + 1]) / 2)
                else:
                    pass
        if len(str(blackindex2)) <= 1:
            npindex2.append(1)
        else:
            for i in range(len(blackindex2)):
                if i % 2 == 0:
                    npindex2.append((blackindex2[i] + blackindex2[i + 1]) / 2)
                else:
                    pass
        if len(b1)==len(npindex2):
            for i in range(len(b1)):
                angle = calc_angle(npindex2[i], 420, b1[i], 380)
                cv2.circle(img, (int(npindex2[i]), 420), 3, 255, -1)
                cv2.circle(img, (int(b1[i]), 380), 3, 255, -1)
                print('赛道{}角度:{},中点横坐标:{}'.format(i+1,angle,b1[i]))
        else:
            pass
    cv2.imshow('s',maskblack)
    cv2.imshow('s1', img)
    if cv2.waitKey(30) & 0xFF == 27:  # 按Esc关闭
        break