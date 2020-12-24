import airsim
import cv2
import numpy as np
import os
import time
import math

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

def pointCloud2image(pointCloud, file_name):
    rmat  = np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]], dtype='float32')
    rmat = rmat.dot(rotation_Zmatrix(90).dot(rotation_Ymatrix(90).dot(rotation_Xmatrix(180))))
    A = np.array([
                [790,0,640],
                [0,395,360],
                [0,0,1]
             ], dtype='float32')

    dist_coef = np.zeros(4, dtype='float32')
    tvec = np.array([[0,-1,0.5]], dtype='float32')

    rvec, _ = cv2.Rodrigues(rmat)

    # 移除坑洞內的點雲
    pointCloud = pointCloud[~(pointCloud[:,2]>1.05)]

    image_point, _ = cv2.projectPoints(pointCloud, rvec, tvec, A, dist_coef)

    img = np.zeros((720, 1280), dtype='float32')


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
        img[v][u] = 255


    # 鏡像翻轉np.fliplr(test)
    img = np.fliplr(img)

    # show the numpy array

    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # save to png image

    save_img = img.astype(np.int16)
    file = '/home/aiotlab/AirSim/output/20201206/pointCloudimg/' + file_name + '.png' 
    cv2.imwrite(file,save_img)
    return
# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

# setup segmentation SM_NYC_Sidewalks_Straight_3

client.simSetSegmentationObjectID("Cube[\w]*", 19, True)
client.simSetSegmentationObjectID("Conifer[\w]*", 19, True)
client.simSetSegmentationObjectID("road[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_MERGED_ON_Brep[\w]*", 19, True)

# set color
client.simSetSegmentationObjectID("SM_NYC_Sidewalks_Straight[\w]*", 19, True)
client.simSetSegmentationObjectID("thsnbarhx_[\w]*", 19, True) # --- all objectID = 12	color=[242, 107, 146]
client.simSetSegmentationObjectID("SM_BuildingFull[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_BGBuilding[\w]*", 19, True)
client.simSetSegmentationObjectID("Plane[\w]*", 4, True)
client.simSetSegmentationObjectID("SM_NYC_Deco_StreetLight[\w]*", 19, True)
client.simSetSegmentationObjectID("Sky[\w]*", 19, True)
client.simSetSegmentationObjectID("BP_Sky_Sphere[\w]*", 19, True)
client.simSetSegmentationObjectID("road[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_ShopSet_Corner[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_Awning_[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_Infil1_City_Decos_Bench[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_HU_Deco_SM_Trashcan[\w]*", 19, True)
client.simSetSegmentationObjectID("thsnbc3hx_LOD[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_ShopSet_Wall[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_ShopSet_Sign[\w]*", 19, True)
client.simSetSegmentationObjectID("PostProcessVolume[\w]*", 19, True)
client.simSetSegmentationObjectID("Material_decal[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_NYC_Deco_Exterior01_FireHydrant[\w]*", 19, True)
client.simSetSegmentationObjectID("MSM_NYC_Deco_Exterior01[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_HU_Deco_SM_Dumpster2[\w]*", 19, True)
client.simSetSegmentationObjectID("thsnbarhx_LOD[\w]*", 19, True)
client.simSetSegmentationObjectID("SM_NYC_Deco_Exterior01_Bollard[\w]*", 19, True)


img_save_path = '/home/aiotlab/AirSim/output/20201206/img/'
seg_save_path = '/home/aiotlab/AirSim/output/20201206/seg/'
if not os.path.exists(img_save_path):
    os.makedirs(img_save_path)
if not os.path.exists(seg_save_path):
    os.makedirs(seg_save_path)

idx = 650
while(idx < 900):
    car_state = client.getCarState()
    pd = car_state.kinematics_estimated.position
    # if idx % 150 == 0:
    #     client.reset()
    #     idx += 1
    # else:
    print("times:", idx)
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))
    print("x value: ",pd.x_val)
    print("y value: ",pd.y_val)

    # apply brakes
    car_controls.brake = 1
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Apply brakes")
    time.sleep(2)   # let car drive a bit
    car_controls.brake = 0 #remove brake
    # get camera images from the car
    # if idx % 150 > 3 :

    lidarData = client.getLidarData()
    points = np.array(lidarData.point_cloud,dtype=np.dtype('f4'))
    points = np.reshape(points,(int(points.shape[0]/3),3))

    pointCloud2image(points, 'frame' + str(idx))

    img_result = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False),
                                             airsim.ImageRequest("0", airsim.ImageType.Segmentation, False, False)])

    try:
        img_response = img_result[0]
        img1d = np.fromstring(img_response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(img_response.height, img_response.width, 3)

        img_filename = img_save_path + 'frame' + str(idx)
        cv2.imwrite(os.path.normpath(img_filename + '.png'), img_rgb)

        seg_response = img_result[1]
        seg1d = np.fromstring(seg_response.image_data_uint8, dtype=np.uint8)
        seg_rgb = seg1d.reshape(seg_response.height, seg_response.width, 3)

        seg_filename = seg_save_path + 'frame' + str(idx)
        cv2.imwrite(os.path.normpath(seg_filename + '.png'), seg_rgb) # write to png
        
    except ValueError:
        img1d = np.zeros((2764800,), dtype=np.uint8)
        img_rgb = img1d.reshape(720, 1280, 3)
        seg1d = np.zeros((2764800,), dtype=np.uint8)
        seg_rgb = img1d.reshape(720, 1280, 3)


    car_controls.throttle = 0.6
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go Forward")
    time.sleep(0.4)
    idx += 1 
        
            
            
#restore to original state
client.reset()

client.enableApiControl(False)

