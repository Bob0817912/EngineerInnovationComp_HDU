# 本部分是将视频流读取后拆分成图片的代码

import cv2
import os
import time

def divide_video(video_path, save_path):

    cap = cv2.VideoCapture(video_path)
    fps =cap.get(cv2.CAP_PROP_FPS)
    # 将视频拆分成对应帧率的图片
    count = 655
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(save_path + str(count) + '.jpg', frame)
            count += 1
        else:
            break
    cap.release()
    return count

video_path = './asset/1.mp4'
save_path = './dataset/image/'

if not os.path.exists(save_path):
    os.makedirs(save_path)

start = time.time()
count = divide_video(video_path, save_path)
end = time.time()
print('Time:', end - start)
print('Count:', count)
print('FPS:', count/(end - start))


