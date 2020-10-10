#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import rospy
import airsim
import numpy  as np
from sensor_msgs.msg import LaserScan

# 获取无人机的xyz坐标，为后面计算距离做准备
def get_drone_position(client):
	position = client.getMultirotorState().kinematics_estimated.position
	return position

# 将点云数据转换成相应角度和距离
def point_cloud_to_angle_position(pos,points):
	obs_distance = []
	angles = []
	for i in range(len(points)):
		x = round(points[i][0],2)
		y = round(points[i][1],2)
		z = round(points[i][2],2)
		if x != 0:
			angle = math.atan(y/x) * 180 / 3.14 # 利用三角函数关系求当前角度
			angle = math.floor(angle) #向下取整
			angles.append(angle)
			distance = math.sqrt((pos.x_val -x) **2 + (pos.y_val-y) **2 +(pos.z_val - z)**2) # 根据激光点坐标和无人机当前点坐标求解距离
			obs_distance.append(distance)
		#print([i,angle,distance])
	angles,obs_distance = scale_point_cloud(angles,obs_distance) # 进行相应变换
	return angles,obs_distance

# 在180度范围内，每隔1度，取一个值，即将会取181个值（中间有0度）
# 对每个角度，求出其对应的下标有哪些，然后求均值，表示当前角度的激光点距离
def scale_point_cloud(angles,obs_distance):
	angle_min = -90.0
	angle_max = 90.0
	new_angles = []
	new_obs_distance = []
	# address_index = [x for x in range(len(list_position_name)) if list_position_name[x] == i]
	for i in range(int(angle_max - angle_min + 1)):
		address_index = [x for x in range(len(angles)) if angles[x] == angle_min + i ] # 求每个角度的下标
		if len(address_index) == 0: #如果某个角度没有值，则直接给最大值
			distance = 100.0
		else: # 否则，求均值
			total_dis = 0
			for j in range(len(address_index)):
				total_dis += obs_distance[address_index[j]]
			distance = total_dis / len(address_index)
		new_angles.append(angle_min + i)
		new_obs_distance.append(distance)
		#print(new_angles[i],new_obs_distance[i])
	return new_angles,new_obs_distance

# 发布ros数据
def pub_laserscan(obs_distance):
	laserscan = LaserScan()
	laserscan.header.stamp = rospy.Time.now()
	laserscan.header.frame_id = 'lidar'
	laserscan.angle_min = -1.57
	laserscan.angle_max = 1.57 # 对应180度
	laserscan.angle_increment = 3.14 / 180 #弧度的增量，这样就是隔1度取值
	laserscan.time_increment = 1.0  / 10   / 180 # 中间的10对应于json中的RotationsPerSecond
	laserscan.range_min = 0.0
	laserscan.range_max = 100.0
	laserscan.ranges = [] # 距离
	laserscan.intensities = [] # 强度
	for i in range(1,len(obs_distance)):
		laserscan.ranges.append(obs_distance[i])
		laserscan.intensities.append(0.0)
	print(laserscan)
	return laserscan

def main():

	# connect the simulator
	client = airsim.MultirotorClient()
	client.confirmConnection()
	client.enableApiControl(True)
	client.armDisarm(True)

	scan_pub = rospy.Publisher('/scan', LaserScan, queue_size=10)
	rate = rospy.Rate(1.0)

	while not rospy.is_shutdown():

		# get the lidar data
		lidarData = client.getLidarData()
		#print('lidar',lidarData)

		if len(lidarData.point_cloud) >3:

			points = np.array(lidarData.point_cloud,dtype=np.dtype('f4'))
			points = np.reshape(points,(int(points.shape[0]/3),3))
			#print('points:',points)
			pos = get_drone_position(client)
			angles,obs_distance = point_cloud_to_angle_position(pos,points)
			print('number of points'),len(points)
			laserscan = pub_laserscan(obs_distance)
			scan_pub.publish(laserscan)
			rate.sleep()
		else:
			print("\tNo points received from Lidar data")

if __name__ == "__main__":
	rospy.init_node('drone1_lidar',anonymous=True)
	main()