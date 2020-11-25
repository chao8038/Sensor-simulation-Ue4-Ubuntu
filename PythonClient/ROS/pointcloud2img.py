import csv
from math import cos
import numpy as np
import cv2
import math

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_rmatrix(degrees: int) -> np.array:
    red = math.pi/180 * degrees

    matrix  = np.array([[1,0,0],
                  [0, math.cos(red),math.sin(red)],
                  [0,-math.sin(red),math.cos(red)]], dtype='float32')    
    return matrix

def draw3DpointCloud(point_cloud: np.array) -> None:
    plt.figure()  # 得到畫面
    ax1 = plt.axes(projection='3d')
    for x in point_cloud[:10]:
        ax1.scatter(x[0], x[1], x[2], marker='.' , cmap='spectral')  # 用散點函數畫點
    plt.show()
    return

# data = pd.read_csv("/home/aiotlab/Documents/Unreal-data/LIDAR-test/frame0000.csv")

# print(data)

A = np.array([
                [790,0,640],
                [0,395,360],
                [0,0,1]
             ], dtype='float32')


tvec = np.array([[-0.3,-0.3,-3]], dtype='float32')

# 80度
r3mat = get_rmatrix(90) 


# 沿Z軸旋轉90度
r2mat  = np.array([[0,1,0],
                  [-1,0,0],
                  [0,0,1]], dtype='float32')

# 沿Y軸旋轉180度
r1mat  = np.array([[-1,0,0],
                  [0,1,0],
                  [0,0,-1]], dtype='float32')

rmat = r3mat.dot(r2mat.dot(r1mat))

# rmat  = np.array([[1,0,0],
#                   [0,1,0],
#                   [0,0,1]], dtype='float32')

# 旋轉矩陣轉換為旋轉向量
rvec, _ = cv2.Rodrigues(rmat)

dist_coef = np.zeros(4, dtype='float32')

with open("/home/aiotlab/Documents/Unreal-data/2020-11-08-17-01-42/point_cloud_new.csv", newline='') as csvfile:
    # 讀取 CSV 檔案內容
    csv_row = list(csv.reader(csvfile))
    count = 0
    # data2 = csv_row[1]
    for data in csv_row:
        if count == 0:
            count+=1
            continue
    # data = csv_row[1]

    # print(len(data))
        pointcloud = np.empty((0,3), dtype='float32')
        step = int(len(data)/3)
        for i in range(step):
            index = i*3
            # 移除坑洞內的點雲
            if float(data[index+2])>1.5:
                print({'x':float(data[index]), 'y':float(data[index+1]), 'z':float(data[index+2])})
                continue
                
            pc = np.float32([[float(data[index]), float(data[index+1]), float(data[index+2])]])
            pointcloud = np.append(pointcloud, pc, axis=0)

        # draw3DpointCloud(pointcloud)


        image_point, _ = cv2.projectPoints(pointcloud, rvec, tvec, A, dist_coef)

        test = np.zeros((720, 1280), dtype='float32')
        for point in image_point:
            # print(point[0][0].astype(int), point[0][1].astype(int))
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
            test[v][u] = 255


        # 鏡像翻轉np.fliplr(test)
        test = np.fliplr(test)

        # show the numpy array

        cv2.imshow("Image", test)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # save to png image
        # save_img = test.astype(np.int16)
        # file = 'output/test1/test' + str(count) + '.png' 
        # cv2.imwrite(file,save_img)
        # count+=1
