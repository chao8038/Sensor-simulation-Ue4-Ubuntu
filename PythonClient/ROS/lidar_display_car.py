#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import rospy
import airsim
import numpy  as np
from geometry_msgs.msg import Point32
from sensor_msgs.msg import LaserScan,PointCloud

def pub_pointcloud(points):
	pc = PointCloud()
	pc.header.stamp = rospy.Time.now()
	pc.header.frame_id = 'airsim'

	for i in range(len(points)):
		pc.points.append(Point32(points[i][0],points[i][1],points[i][2]))
	# print('pc:',pc)
	return pc

def main():

	# connect the simulator
	client = airsim.CarClient()
	client.confirmConnection()
	client.enableApiControl(False)
	# car_controls = airsim.CarControls()

	pointcloud_pub = rospy.Publisher('/pointcloud', PointCloud, queue_size=10)
	rate = rospy.Rate(100)

	while not rospy.is_shutdown():
		# get the lidar data
		lidarData = client.getLidarData()
		#print('lidar',lidarData)

		if len(lidarData.point_cloud) >3:

			points = np.array(lidarData.point_cloud,dtype=np.dtype('f4'))
			points = np.reshape(points,(int(points.shape[0]/3),3))
			# print('points:',points)
			pc = pub_pointcloud(points)
			pointcloud_pub.publish(pc)
			rate.sleep()
		else:
			print("\tNo points received from Lidar data")

if __name__ == "__main__":
	rospy.init_node('car1_lidar',anonymous=True)
	main()