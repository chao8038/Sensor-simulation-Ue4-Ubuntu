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

pub = rospy.Publisher("airsim/image_raw", Image, queue_size=10)
rospy.init_node('image_raw', anonymous=True)
rate = rospy.Rate(100) # 10hz

def main():
    # connect to the AirSim simulator 
    client = airsim.CarClient()
    client.confirmConnection()

    bridge = CvBridge()

    while not rospy.is_shutdown():
         # get camera images from the car
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        try:
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            
        except ValueError:
            img1d = np.zeros((2764800,), dtype=np.uint8)
            img_rgb = img1d.reshape(720, 1280, 3)
        pub.publish(bridge.cv2_to_imgmsg(img_rgb, "bgr8"))
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass