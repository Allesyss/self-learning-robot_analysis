'''
adapted from:
https://blog.csdn.net/dgut_guangdian/article/details/
79762409?ops_request_misc=%257B%2522request%255Fid%2522%253A%252216018
9713019724836715552%2522%252C%2522scm%2522%253A%252220140713.130102334
..%2522%257D&request_id=160189713019724836715552&biz_id=0&utm_medium=d
istribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v28
-1-79762409.pc_first_rank_v2_rank_v28&utm_term=python%E8%BF%90%E5%8A%A
8%E7%89%A9%E4%BD%93%E8%BF%BD%E8%B8%AA&spm=1018.2118.3001.4187

This project is too sensitive to image changes.
Even the slightest change could trigger detection.
Considering using similarity comparison to reduce sensitivity.
Modifications will follow 2020-10-6
'''
import cv2
import time
#import datetime
import os
import easygui


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print
        ("---  new folder...  ---")
        print
        ("---  OK  ---")

    else:
        print
        ("---  There is this folder!  ---")


file = "C:/Users/86189/Desktop/MotionDetTest"  # 保存位置
mkdir(file)
print("文件储存于C:/Users/86189/Desktop/MotionDetTest")
# 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头
camera = cv2.VideoCapture(0)
title = easygui.msgbox(msg="将于5s后开始记录摄像头移动情况！""\n""请离开保证背景稳定""\n"
                       , title="运动检测追踪拍照", ok_button="开始执行")
msg = easygui.msgbox(msg="C:/Users/86189/Desktop/MotionDetTest")
time.sleep(5)  # 延迟5s执行
background = None  # 初始化背景


def nothing(x):
    pass


cv2.namedWindow("fps")  # 新建一个窗口
cv2.createTrackbar('level', 'fps', 21, 255, nothing)  # 新建阈值滑动条
shot_idx = 0

while True:
    text = "No Target"
    flat = 0
    # 滑动条赋值
    kerne = cv2.getTrackbarPos('level', 'fps')
    if kerne % 2 == 0:
        kerne = kerne + 1  # 解决滑动条赋值到高斯滤波器是偶数异常抛出
    (grabbed, frame) = camera.read()
    # 对帧进行预处理，先转灰度图，再进行高斯滤波。
    # 用高斯滤波对图像处理，避免亮度、震动等参数微小变化影响效果
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (kerne, kerne), 0)
    # 将第一帧设置为整个输入的背景
    if background is None:
        background = gray
        continue
    # 当前帧和第一帧的不同它可以把两幅图的差的绝对值输出到另一幅图上面来
    frameDelta = cv2.absdiff(background, gray)
    # 二值化
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # 腐蚀膨胀
    thresh = cv2.dilate(thresh, None, iterations=2)
    # 取轮廓
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    # 遍历轮廓
    for c in cnts:
        if cv2.contourArea(c) < 1800:  # 对于较小矩形区域，选择忽略
            continue
        flat = 1  # 设置一个标签，当有运动的时候为1
        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        text = "Find Target! save as C:/Users/86189/Desktop/MotionDetTest"
        print("Find Target!")
    cv2.putText(frame, text, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
     #           (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # cv2.imshow("Frame Delta", frameDelta)

    cv2.imshow("fps", frame)
    # cv2.imshow("Thresh", thresh)

    key = cv2.waitKey(1) & 0xFF

    # 如果q键被按下，跳出循环
    ch = cv2.waitKey(1)
    if key == ord("q"):
        break

    if flat == 1:  # 设置一个标签，当有运动的时候为1
        fn = 'C:/Users/86189/Desktop/MotionDetTest/shot%d.jpg' % (shot_idx)
        cv2.imwrite(fn, frame)
        shot_idx += 1
        time.sleep(0.5)
        continue
camera.release()
cv2.destroyAllWindows()