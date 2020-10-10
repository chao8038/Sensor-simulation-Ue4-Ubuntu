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

pub = rospy.Publisher("airsim/image_raw", Image, queue_size=1)
rospy.init_node('image_raw', anonymous=True)
rate = rospy.Rate(100) # 10hz

def publish_data(data):
    # Populate image message
    msg=Image() 
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = "airsim"
    msg.encoding = "rgb8"
    msg.height = 720  # resolution should match values in settings.json 
    msg.width = 1280
    msg.data = np.array(data).tostring()
    msg.is_bigendian = 0
    msg.step = msg.width * 3

    # log time and size of published image
    # rospy.loginfo(len(response.image_data_uint8))
    # publish image message
    pub.publish(msg)
    # sleep until next cycle
    rate.sleep()

def main():
    # connect to the AirSim simulator 
    client = airsim.CarClient()
    client.confirmConnection()

    bridge = CvBridge()

    while not rospy.is_shutdown():
         # get camera images from the car
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        if responses != None:
            response = responses[0]
            
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

            img_rgb = img1d.reshape(response.height, response.width, 3)
            
            pub.publish(bridge.cv2_to_imgmsg(img_rgb))
            rate.sleep()
            # publish_data(img_rgb)
            # cv2.imshow('img', image_rgb)
            # key=cv2.waitKey(1)
            # if key==ord('q'):
            #     break

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass