import csv
from math import cos
import numpy as np
import cv2
import math

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rotation_Xmatrix(degrees: int) -> np.array:
    red = math.pi/180 * degrees

    matrix  = np.array([[1,0,0],
                        [0, math.cos(red),math.sin(red)],
                        [0,-math.sin(red),math.cos(red)]], dtype='float32')    
    return matrix

def rotation_Ymatrix(degrees: int) -> np.array:
    red = math.pi/180 * degrees

    matrix  = np.array([[math.cos(red),0,math.sin(red)],
                        [0,1,0],
                        [-math.sin(red),0,math.cos(red)]], dtype='float32')    
    return matrix

def rotation_Zmatrix(degrees: int) -> np.array:
    red = math.pi/180 * degrees

    matrix  = np.array([[math.cos(red),-math.sin(red),0],
                        [math.sin(red), math.cos(red),0],
                        [0,0,1]], dtype='float32')    
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


tvec = np.array([[0,-1,0]], dtype='float32')


# 沿X軸旋轉90度
r3mat = rotation_Xmatrix(90) 


# 沿Z軸旋轉90度
r2mat  = rotation_Zmatrix(90)

# 沿Y軸旋轉180度
r1mat  = rotation_Ymatrix(180)

# rmat = r3mat.dot(r2mat.dot(r1mat))

# rmat = r1mat

# rmat = r2mat.dot(r1mat)

rmat  = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]], dtype='float32')

rmat = rmat.dot(rotation_Zmatrix(90).dot(rotation_Ymatrix(90).dot(rotation_Xmatrix(180))))

# 旋轉矩陣轉換為旋轉向量
rvec, _ = cv2.Rodrigues(rmat)

dist_coef = np.zeros(4, dtype='float32')
with open(r"C:\Users\chaoyu\Downloads\2020-11-26-21-09-45\point_cloud_new.csv", newline='') as csvfile:
    # 讀取 CSV 檔案內容
    csv_row = list(csv.reader(csvfile))
    count = -1
    # data2 = csv_row[1]
    for data in csv_row:
        if count == -1:
            count+=1
            continue
    # data = csv_row[1]

    # print(len(data))
        pointcloud = np.empty((0,3), dtype='float32')
        step = int(len(data)/3)
        for i in range(step):
            index = i*3
            # 移除坑洞內的點雲
            if float(data[index+2])>1.05:
                # print({'x':float(data[index]), 'y':float(data[index+1]), 'z':float(data[index+2])})
                continue
                
            pc = np.float32([[float(data[index]), float(data[index+1]), float(data[index+2])]])
            pointcloud = np.append(pointcloud, pc, axis=0)

        # draw3DpointCloud(pointcloud[:1000])


        image_point, _ = cv2.projectPoints(pointcloud, rvec, tvec, A, dist_coef)

        test = np.zeros((720, 1280, 3), dtype='float32')

        test[:,:, :] = 1

        # test = np.zeros((720, 1280), dtype='float32')
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
            test[v,u,:] = 0


        # 鏡像翻轉np.fliplr(test)
        test = np.fliplr(test)

        # show the numpy array

        cv2.imshow("Image", test)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # save to png image
        save_img = test.astype(np.int16)
        file = 'output/test3/test' + str(count) + '.png' 
        cv2.imwrite(file,save_img)
        count+=1
