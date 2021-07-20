import airsim
import cv2
import numpy as np
import os
import time

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

# setup segmentation SM_NYC_Sidewalks_Straight_3

found = client.simSetSegmentationObjectID("SM_NYC_Sidewalks_Straight[\w]*", 19, True)
found = client.simSetSegmentationObjectID("thsnbarhx_LOD[\w]*", 19, True) # --- all objectID = 12	color=[242, 107, 146]
found = client.simSetSegmentationObjectID("SM_BuildingFull[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_BGBuilding[\w]*", 19, True)
# found = client.simSetSegmentationObjectID("Cube[\w]*", 19, True)
found = client.simSetSegmentationObjectID("Plane[\w]*", 19, True)
found = client.simSetSegmentationObjectID("Conifer[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_NYC_Deco_StreetLight[\w]*", 19, True)
found = client.simSetSegmentationObjectID("Sky[\w]*", 19, True)
found = client.simSetSegmentationObjectID("BP_Sky_Sphere[\w]*", 19, True)
# found = client.simSetSegmentationObjectID("Pothole[\w]*", 4, True)
found = client.simSetSegmentationObjectID("Cube[\w]*", 4, True)
found = client.simSetSegmentationObjectID("road[\w]*", 19, True)
found = client.simSetSegmentationObjectID("縱向裂縫[\w]*", 19, True)
found = client.simSetSegmentationObjectID("縱向列縫[\w]*", 19, True)
found = client.simSetSegmentationObjectID("橫向裂縫[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_MERGED_ON_Brep[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_ShopSet_Corner[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_Awning_[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_Infil1_City_Decos_Bench[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_HU_Deco_SM_Trashcan[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_ShopSet_Corner[\w]*", 19, True)
found = client.simSetSegmentationObjectID("thsnbc3hx_LOD[\w]*", 19, True)
found = client.simSetSegmentationObjectID("thsnbc3hx_LOD[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_ShopSet_Wall[\w]*", 19, True)
found = client.simSetSegmentationObjectID("SM_ShopSet_Sign[\w]*", 19, True)
found = client.simSetSegmentationObjectID("PostProcessVolume[\w]*", 19, True)
found = client.simSetSegmentationObjectID("Material_decal[\w]*", 19, True)
idx = 900
while idx<1200:
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
    responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene)])
    response = responses[0]

    responses1 = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Segmentation)])
    response1 = responses1[0]

    for response in responses:
        save_path = 'd:/pothole/UE4/20210714/img/'
        filename = save_path + 'frame' + str(idx)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        if response.pixels_as_float:
            print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
            airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
        elif response.compress: #png format
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
        else: #uncompressed array
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
            img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 3 channel image array H X W X 3
            cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png

    for response1 in responses1:
        save_path = 'd:/pothole/UE4/20210714/seg/'
        filename = save_path + 'frame' + str(idx)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        if response1.pixels_as_float:
            print("Type %d, size %d" % (response1.image_type, len(response1.image_data_float)))
            airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response1))
        elif response1.compress: #png format
            print("Type %d, size %d" % (response1.image_type, len(response1.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response1.image_data_uint8)
        else: #uncompressed array
            print("Type %d, size %d" % (response1.image_type, len(response1.image_data_uint8)))
            img1d = np.fromstring(response1.image_data_uint8, dtype=np.uint8) # get numpy array
            img_rgb = img1d.reshape(response1.height, response1.width, 3) # reshape array to 3 channel image array H X W X 3
            cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png

    car_controls.throttle = 0.6
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go Forward")
    time.sleep(0.4)
    idx += 1 
        
            
            
#restore to original state
client.reset()

client.enableApiControl(False)

