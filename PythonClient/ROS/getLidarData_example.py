#!/usr/bin/env python
# -*-coding:utf-8 -*-

import cv2
import numpy as np

import airsim
import time
import datetime
import pprint



client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

lidarData = client.getLidarData()
print('lidar',lidarData)

if len(lidarData.point_cloud) >3:
	points = np.array(lidarData.point_cloud,dtype=np.dtype('f4'))
	points = np.reshape(points,(int(points.shape[0]/3),3))
	print('number of points'),len(points)
else:
	print("\tNo points received from Lidar data")