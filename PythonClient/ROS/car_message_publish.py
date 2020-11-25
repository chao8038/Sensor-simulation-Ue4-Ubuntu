#!/usr/bin/env python

# Example ROS node for publishing AirSim images.

import rospy

# ROS Image message
from sensor_msgs.msg import Image

# AirSim Python API
import airsim

import numpy as np

from cv_bridge import CvBridge

from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32

img_pub = rospy.Publisher("airsim/image_raw", Image, queue_size=1)
seg_pub = rospy.Publisher("airsim/image_seg", Image, queue_size=1)
pointcloud_pub = rospy.Publisher('airsim/pointcloud', PointCloud, queue_size=1)
rospy.init_node('Airsim', anonymous=True)
rate = rospy.Rate(100) # 10hz

def pub_pointcloud(points):
	pc = PointCloud()
	pc.header.stamp = rospy.Time.now()
	pc.header.frame_id = 'airsim'

	for i in range(len(points)):
		pc.points.append(Point32(points[i][0],points[i][1],points[i][2]))
	return pc


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
        img_responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        seg_responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Segmentation, False, False)])
        # get the lidar data
        lidarData = client.getLidarData()
        try:
            img_response = img_responses[0]
            img1d = np.fromstring(img_response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(img_response.height, img_response.width, 3)

            seg_response = seg_responses[0]
            seg1d = np.fromstring(seg_response.image_data_uint8, dtype=np.uint8)
            seg_rgb = seg1d.reshape(seg_response.height, seg_response.width, 3)
            
        except ValueError:
            img1d = np.zeros((2764800,), dtype=np.uint8)
            img_rgb = img1d.reshape(720, 1280, 3)
            seg1d = np.zeros((2764800,), dtype=np.uint8)
            seg_rgb = img1d.reshape(720, 1280, 3)
        
        try:
            points = np.array(lidarData.point_cloud,dtype=np.dtype('f4'))
            points = np.reshape(points,(int(points.shape[0]/3),3))
            pc = pub_pointcloud(points)
            
            img_pub.publish(bridge.cv2_to_imgmsg(img_rgb, "bgr8"))
            seg_pub.publish(bridge.cv2_to_imgmsg(seg_rgb, "bgr8"))
            pointcloud_pub.publish(pc)

        except Exception as e:
            print(e)

        
        
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass