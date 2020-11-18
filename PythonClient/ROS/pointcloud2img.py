import csv

with open("/home/aiotlab/Documents/Unreal-data/LIDAR-test/frame0000.csv", newline='') as csvfile:
    # 讀取 CSV 檔案內容
    csv_row = list(csv.reader(csvfile))
    data = csv_row[0]
    # print(len(data))
    pointcloud =[]
    step = int(len(data)/3)
    for i in range(step):
        index = i*3
        pc = {'x':float(data[index]), 'y':float(data[index+1]), 'z':float(data[index+2])}
        pointcloud.append(pc)
    # print(pointcloud)
    # for point in pointcloud:
    #     print(point)