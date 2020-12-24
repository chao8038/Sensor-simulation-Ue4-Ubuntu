#!/usr/bin/env python

# Example ROS node for publishing AirSim images.

import rospy

# ROS Image message
from sensor_msgs.msg import Image

# AirSim Python API
import airsim

import cv2
import numpy as np

from cv_bridge import CvBridge

pub = rospy.Publisher("airsim/image_seg", Image, queue_size=10)
rospy.init_node('image_raw', anonymous=True)
rate = rospy.Rate(100) # 10hz

def main():
    # connect to the AirSim simulator 
    client = airsim.CarClient()
    client.confirmConnection()

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
    

    bridge = CvBridge()

    while not rospy.is_shutdown():
         # get camera images from the car
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Segmentation, False, False)])
        try:
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            
        except Exception as e:
            print(e)
            img1d = np.ones((2764800,), dtype=np.uint8)
            img_rgb = img1d.reshape(720, 1280, 3)
        pub.publish(bridge.cv2_to_imgmsg(img_rgb, "bgr8"))
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass