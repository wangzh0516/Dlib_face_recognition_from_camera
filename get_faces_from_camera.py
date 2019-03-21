# 进行人脸录入 / face register
# 录入多张人脸 / support multi-faces

# Author:   coneypo
# Blog:     http://www.cnblogs.com/AdaminXie
# GitHub:   https://github.com/coneypo/Dlib_face_recognition_from_camera
# Mail:     coneypo@foxmail.com

# Created at 2018-05-11
# Updated at 2019-02-21

import dlib         # 人脸处理的库 Dlib
import numpy as np  # 数据处理的库 Numpy
import cv2          # 图像处理的库 OpenCv

import os           # 读写文件
import shutil       # 读写文件

# Dlib 正向人脸检测器 frontal face detector
detector = dlib.get_frontal_face_detector()

# Dlib 68 点特征预测器 68 points features predictor
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# OpenCv 调用摄像头 use camera
cap = cv2.VideoCapture(0)

# 设置视频参数 set camera
cap.set(3, 480)

# 人脸截图的计数器 the counter for screenshoot
cnt_ss = 0

# 存储人脸的文件夹 the folder to save faces
current_face_dir = 0

# 保存 photos/csv 的路径 the directory to save photos/csv
path_photos_from_camera = "data/data_faces_from_camera/"
path_csv_from_photos = "data/data_csvs_from_camera/"


# 新建保存人脸图像文件和数据CSV文件夹
# mkdir for saving photos and csv
def pre_work_mkdir():

    # 新建文件夹
    if os.path.isdir(path_photos_from_camera):
        pass
    else:
        os.mkdir(path_photos_from_camera)
    if os.path.isdir(path_csv_from_photos):
        pass
    else:
        os.mkdir(path_csv_from_photos)


pre_work_mkdir()


##### optional/可选, 默认关闭 #####
# 删除之前存的人脸数据文件夹
# delete the old data of faces
def pre_work_deldir():
    # 删除之前存的人脸数据文件夹
    # 删除 "/data_faces_from_camera/person_x/"...
    folders_rd = os.listdir(path_photos_from_camera)
    for i in range(len(folders_rd)):
        shutil.rmtree(path_photos_from_camera+folders_rd[i])

    csv_rd = os.listdir(path_csv_from_photos)
    for i in range(len(csv_rd)):
        os.remove(path_csv_from_photos+csv_rd[i])

# 这里在每次程序录入之前, 删掉之前存的人脸数据
# 如果这里打开，每次进行人脸录入的时候都会删掉之前的人脸图像文件夹
# pre_work_deldir()
##################################


# 如果有之前录入的人脸
# 在之前 person_x 的序号按照 person_x+1 开始录入
# if old face exists
# start from person_x+1
if os.listdir("data/data_faces_from_camera/"):
    # 获取已录入的最后一个人脸序号
    person_list = os.listdir("data/data_faces_from_camera/")
    person_list.sort()
    person_num_latest = int(str(person_list[-1]).split("_")[-1])
    person_cnt = person_num_latest

# 如果第一次存储或者没有之前录入的人脸, 按照 person_1 开始录入
# start from person_1
else:
    person_cnt = 0

# 之后用来控制是否保存图像的 flag
# the flag to control if save
save_flag = 1

while cap.isOpened():
    # 480 height * 640 width
    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)

    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)
    
    # 人脸数 faces
    faces = detector(img_gray, 0)

    # 待会要写的字体
    # font to write
    font = cv2.FONT_HERSHEY_COMPLEX

    # 按下 'n' 新建存储人脸的文件夹
    # press 'n' to create the folders for saving faces
    if kk == ord('n'):
        person_cnt += 1
        current_face_dir = path_photos_from_camera + "person_" + str(person_cnt)
        os.makedirs(current_face_dir)
        print('\n')
        print("新建的人脸文件夹/creating folders: ", current_face_dir)

        # 将人脸计数器清零
        # clear the cnt of faces
        cnt_ss = 0

    # 检测到人脸
    # if detect face
    if len(faces) != 0:
        # 矩形框
        # show the rectangle box
        for k, d in enumerate(faces):
            # 计算矩形大小
            # we need to compute the width and height of the box
            # (x,y), (宽度width, 高度height)
            pos_start = tuple([d.left(), d.top()])
            pos_end = tuple([d.right(), d.bottom()])

            # 计算矩形框大小
            height = (d.bottom() - d.top())
            width = (d.right() - d.left())

            hh = int(height/2)
            ww = int(width/2)

            # 设置颜色 / The color of rectangle of faces detected
            color_rectangle = (255, 255, 255)
            if (d.right()+ww) > 640 or (d.bottom()+hh > 480) or (d.left()-ww < 0) or (d.top()-hh < 0):
                cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                color_rectangle = (0, 0, 255)
                save_flag = 0
            else:
                color_rectangle = (255, 255, 255)
                save_flag = 1

            cv2.rectangle(img_rd,
                          tuple([d.left() - ww, d.top() - hh]),
                          tuple([d.right() + ww, d.bottom() + hh]),
                          color_rectangle, 2)

            # 根据人脸大小生成空的图像
            # create blank image according to the size of face detected
            im_blank = np.zeros((int(height*2), width*2, 3), np.uint8)

            if save_flag:
                # 按下 's' 保存摄像头中的人脸到本地
                # press 's' to screen shot
                if kk == ord('s'):
                    if os.path.isdir(current_face_dir):
                        cnt_ss += 1
                        for ii in range(height*2):
                            for jj in range(width*2):
                                im_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
                        cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", im_blank)
                        print("写入本地：", str(current_face_dir) + "/img_face_" + str(cnt_ss) + ".jpg")
                    else:
                        print("请在按 'S' 之前先按 'N' 来建文件夹 / Please press 'N' before 'S'")

    # 显示人脸数
    # show the numbers of faces detected
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    # 添加说明
    # and some statements
    cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "N: New face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

    # 按下 'q' 键退出
    # press 'q' to exit
    if kk == ord('q'):
        break

    # 窗口显示
    # cv2.namedWindow("camera", 0) # 如果需要摄像头窗口大小可调
    # cv2.imshow("camera", img_rd)

# 释放摄像头
# release camera
cap.release()

cv2.destroyAllWindows()
