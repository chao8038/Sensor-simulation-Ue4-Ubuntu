import csv
import pandas as pd 
import numpy as np
import cv2

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# data = pd.read_csv("/home/aiotlab/Documents/Unreal-data/LIDAR-test/frame0000.csv")

# print(data)

A = np.array([
                [395,0,640],
                [0,395,360],
                [0,0,1]
             ], dtype='float32')


tvec = np.array([[0,-8,-15]], dtype='float32')

# 60度
rmat  = np.array([[0,-1,0],
                  [0.5,0,-0.866],
                  [0.866,0,0.5]], dtype='float32')

# 45度
# rmat  = np.array([[0,-1,0],
#                   [0.707,0,-0.707],
#                   [0.707,0,0.707]], dtype='float32')

# 30度
# rmat  = np.array([[0,-1,0],
#                   [0.866,0,-0.5],
#                   [0.5,0,0.866]], dtype='float32')

# rmat  = np.array([[0,-1,0],
#                   [0,0,-1],
#                   [1,0,0]], dtype='float32')

rvec, _ = cv2.Rodrigues(rmat)

dist_coef = np.zeros(4, dtype='float32')

with open("/home/aiotlab/Documents/Unreal-data/2020-11-08-17-01-42/point_cloud_new.csv", newline='') as csvfile:
    # 讀取 CSV 檔案內容
    csv_row = list(csv.reader(csvfile))
    # for data in csv_row:
    data = csv_row[1]

    # print(len(data))
    pointcloud = np.empty((0,3), dtype='float32')
    step = int(len(data)/3)
    for i in range(step):
        index = i*3
        # pc = {'x':float(data[index]), 'y':float(data[index+1]), 'z':float(data[index+2])}
        pc = np.float32([[float(data[index]), float(data[index+1]), float(data[index+2])]])
        pointcloud = np.append(pointcloud, pc, axis=0)
    print(pointcloud[0])
    # plt.figure()  # 得到畫面
    # ax1 = plt.axes(projection='3d')
    # for x in pointcloud[:10]:
    #     print(x[0])
    #     ax1.scatter(x[0], x[1], x[2], marker='.' , cmap='spectral')  # 用散點函數畫點
    # plt.show()


    image_point, _ = cv2.projectPoints(pointcloud, rvec, tvec, A, dist_coef)

    test = np.zeros((720, 1280), dtype='float32')
    for point in image_point:
        print(point[0][0].astype(int), point[0][1].astype(int))
        u = point[0][0].astype(int) -1
        v = point[0][1].astype(int) -1
        if v >= 720:
            v = 719
        elif v<0:
            v = 0
        if u >= 1280:
            u = 1279
        elif u<0:
            u = 0
        test[v][u] = 1


    cv2.imshow("Image",test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        # for point in pointcloud:
        #     print(point)