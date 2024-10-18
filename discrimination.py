import cv2
import numpy as np
import collections
import Usual
x_buf=0
y_buf=0
def GetZhuanPanCenter(mat:cv2.Mat):
    # 定义边框的宽度和颜色  
    border_width = 100
    border_color = (255, 255, 255)  # 白色  
    wide,heigth= mat.shape[:2]
    #mat=cv2.resize(mat,(int(heigth/2),int(wide/2)))
    grayImg:cv2.Mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.GaussianBlur(grayImg, (3, 3), 0) 
    #res = cv2.copyMakeBorder(grayImg, border_width, border_width, border_width, border_width, cv2.BORDER_CONSTANT, value=border_color)  
    circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 100, param1=150, param2=45, minRadius=200, maxRadius=400)
    resx=None
    resy=None
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(mat, (int(x), int(y)), r, (0, 255, 0), 3)
            resx=int(x)
            resy=int(y+r*(2/3))
            cv2.circle(mat, (resx,resy), 3, (255, 255, 0), 3)        
    return resx,resy
    #cv2.imshow("win",grayImg)
def GetRingColor(mat:cv2.Mat):
    wide=2
    rings=DiscriminateRing(mat,5,100)
    for x,y in rings:
        iy=int(y)
        ix=int(x)
        roi=mat[iy-wide:iy+wide, ix-wide:ix+wide]
        
        print(x,y,GetRoiColor(roi))

        cv2.circle(mat, (int(ix), int(iy)), 3, (0, 255, 0), 3)
    if(len(rings)==3):
        cx,cy=GetZhuanPanCenter(rings)
        cv2.circle(mat, (int(cx), int(cy)), 3, (0, 0, 255), 3)
        


def ring_classify(examples:list,datas:list)->list:
    res=[]
    for e in examples:
        res.append([])
    for (x, y, r) in datas:      
        temp=()
        d_min=65534
        for i in range(len(res)):
            dx=x-examples[i][0]
            dy=y-examples[i][1]
            distance = dx*dx+dy*dy
            if(distance<d_min):
                d_min=distance
                temp=((x,y,r),i)
        c:list=res[temp[1]]
        c.append(temp[0])
    return res
    
PARAM1=150
PARAM2=100
def DiscriminateRing_Pro(mat:cv2.Mat,lastmat:cv2.Mat,r_min=10,r_max=70)->list:
    example=[]
    datas=[]
    res_list=[]
    frames=[]
    frames.append(lastmat)
    grayImg:cv2.Mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.GaussianBlur(grayImg, (5, 5), 0) 
    circles_pre = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 100, param1=PARAM1, param2=PARAM2, minRadius=r_min, maxRadius=r_max)
    #第一次检测
    if circles_pre is not None:
        circles_pre = np.round(circles_pre[0, :]).astype("int")
        #得到第一次的粗略坐标
        for (x, y, r) in circles_pre:
            example.append((x,y,r))
        if(True):
            grayImg1:cv2.Mat = cv2.cvtColor(lastmat, cv2.COLOR_BGR2GRAY)
            grayImg1 = cv2.GaussianBlur(grayImg1, (5, 5), 0)
            circles = cv2.HoughCircles(grayImg1, cv2.HOUGH_GRADIENT, 1, 3, param1=PARAM1, param2=PARAM2, minRadius=10, maxRadius=70)
            if circles is not None:        
                circles = np.round(circles[0, :]).astype("int")
                for(x,y,r) in circles:
                    datas.append((x,y,r))
                circles_list=ring_classify(example,datas)
                for i in range(len(example)):
                    x_sum=0
                    y_sum=0
                    size=len(circles_list[i])
                    #print(size)
                    for x,y,r in circles_list[i]:
                        cv2.circle(mat, (x, y), r, (0, 0, 255), 1)
                        x_sum+=x
                        y_sum+=y
                    x_avg=x_sum/size
                    y_avg=y_sum/size
                    res_list.append((x_avg,y_avg))
                    cv2.circle(mat, (int(x_avg), int(y_avg)), 3, (0, 255, 0), 3)
    return res_list

    

    


#识别圆环    
def DiscriminateRing(mat:cv2.Mat,r_min=10,r_max=70)->list:
    grayImg:cv2.Mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.GaussianBlur(grayImg, (5, 5), 0) 
    circle_size=0
    pre_list=[]
    circles_list=[]
    res_list=[]
    circles_pre = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 100, param1=PARAM1, param2=PARAM2, minRadius=r_min, maxRadius=r_max)
    #第一次检测
    if circles_pre is not None:
        circles_pre = np.round(circles_pre[0, :]).astype("int")
        circle_size=len(circles_pre)
        #得到第一次的粗略坐标
        for (x, y, r) in circles_pre:
            pre_list.append((x,y,r))
            circles_list.append([])
            
        #进行第二次精确检测
        circles = cv2.HoughCircles(grayImg, cv2.HOUGH_GRADIENT, 1, 3, param1=PARAM1, param2=PARAM2, minRadius=10, maxRadius=70)  
        
        if circles is not None:
            
            circles = np.round(circles[0, :]).astype("int")
            # datas=[]
            # datas.append(pre_list[0])
            # for(x,y,r) in circles:
            #     datas.append((x,y,r))
            # circles_list=ring_classify(pre_list,datas)
            #与第一次的坐标匹配
            for (x, y, r) in circles:  
                
                temp=()
                d_min=65534
                for i in range(circle_size):
                    dx=x-pre_list[i][0]
                    dy=y-pre_list[i][1]
                    
                    distance = dx*dx+dy*dy
                    if(distance<d_min):
                        d_min=distance
                        temp=((x,y,r),i)
                
                
                
                c:list=circles_list[temp[1]]
                c.append(temp[0])
                #print(d_min)
            #滤波得到精细坐标
            for i in range(circle_size):
                x_sum=0
                y_sum=0
                size=len(circles_list[i])
                #print(size)
                
                for x,y,r in circles_list[i]:
                    cv2.circle(mat, (x, y), r, (0, 0, 255), 1)
                    x_sum+=x
                    y_sum+=y
                if(size!=0):
                    x_avg=x_sum/size
                    y_avg=y_sum/size
                    res_list.append((x_avg,y_avg))
                    cv2.circle(mat, (int(x_avg), int(y_avg)), 3, (0, 255, 0), 3)
    return res_list
            
def GetRoiColor(roi:cv2.Mat)->str:
    roi=cv2.GaussianBlur(roi, (9, 9), 0) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2Lab)
    
    channels = cv2.split(roi) 
    averages = [np.mean(channel) for channel in channels] 
    color_str='N'
    if(abs(averages[1]-128)<10 and abs(averages[2]-128)<10):
        color_str='N'
    elif(averages[1]>128 and averages[2]>128):
        color_str='R'
    elif(averages[1]<128 and averages[2]>128):
        color_str='G'
    elif(averages[1]>128 and averages[2]<128):
        color_str='B'
    return color_str
def GetThreeColor(mat:cv2.Mat,dx=0,dy=-40,wide=220):
    rect_wide=30
    border_wide=wide
    height, width = mat.shape[:2]  
    cx=int(width / 2 +dx) 
    cy=int(height / 2+dy)
    lx=cx-border_wide
    rx=cx+border_wide

    x = cx
    y = cy
    roi2 = mat[y:y+rect_wide, x:x+rect_wide]

    x = lx
    y = cy
    roi1 = mat[y:y+rect_wide, x:x+rect_wide]

    x = rx
    y = cy
    roi3 = mat[y:y+rect_wide, x:x+rect_wide]
    color_str1=GetRoiColor(roi1)
    color_str2=GetRoiColor(roi2)
    color_str3=GetRoiColor(roi3)
    x = cx
    y = cy
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    x = rx
    y = cy
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    x = lx
    y = cy
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)  
    print(color_str1+color_str2+color_str3)
    res=Usual.GetReturnType(color_str1+color_str2+color_str3)
    return res

def GetThreeColor_Auto(mat:cv2.Mat):
    res='g'
    rings_temp=DiscriminateRing(mat.copy(),5,50)
    if(len(rings_temp)==3):
        rings=rings_temp
    rings=rings_temp
    wide=2
    for x,y in rings:
        iy=int(y)
        ix=int(x)
        roi=mat[iy-wide:iy+wide, ix-wide:ix+wide]
        
        print(x,y,GetRoiColor(roi))

        cv2.circle(mat, (int(ix), int(iy)), 3, (0, 255, 0), 3)
    # rect_wide=30
    # border_wide=220
    # height, width = mat.shape[:2]  
    # cx=int(width / 2 ) 
    # cy=int(height / 2-40)
    # lx=cx-border_wide
    # rx=cx+border_wide

    # x = cx
    # y = cy
    # roi2 = mat[y:y+rect_wide, x:x+rect_wide]

    # x = lx
    # y = cy
    # roi1 = mat[y:y+rect_wide, x:x+rect_wide]

    # x = rx
    # y = cy
    # roi3 = mat[y:y+rect_wide, x:x+rect_wide]
    # color_str1=GetRoiColor(roi1)
    # color_str2=GetRoiColor(roi2)
    # color_str3=GetRoiColor(roi3)
    # x = cx
    # y = cy
    # cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    # x = rx
    # y = cy
    # cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)
    # x = lx
    # y = cy
    # cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2)  
    # print(color_str1+color_str2+color_str3)
    # res=Usual.GetReturnType(color_str1+color_str2+color_str3)
    return res
#识别中心颜色
def DiscriminateColor(mat:cv2.Mat):
    rect_wide=100
    height, width = mat.shape[:2]  
    x = int(width / 2 - 50)  
    y = int(height / 2 - 50-100)  
    
    # lab = cv2.cvtColor(mat, cv2.COLOR_BGR2Lab)
    # roi = lab[y:y+rect_wide, x:x+rect_wide]
    roi = mat[y:y+rect_wide, x:x+rect_wide]
    color_str=GetRoiColor(roi)
    # channels = cv2.split(roi) 
    # averages = [np.mean(channel) for channel in channels]  
    # # averages[0]-=128
    # # averages[1]-=128
    # # averages[2]-=128
    # color_str="else"
    # if(abs(averages[1]-128)<5 and abs(averages[2]-128)<5):
    #     color_str="white"
    # elif(averages[1]>128 and averages[2]>128):
    #     color_str="red"
    # elif(averages[1]<128 and averages[2]>128):
    #     color_str="green"
    # elif(averages[1]>128 and averages[2]<128):
    #     color_str="blue"
    
    if(color_str!="N"):
        print(color_str)
    cv2.rectangle(mat, (x, y), (x + rect_wide, y + rect_wide), (0, 255, 0), 2) 
    return color_str