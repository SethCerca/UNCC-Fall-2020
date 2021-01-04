#!/usr/bin/env python


from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan

import rospy

def pointCallback(data):
	print(data.data)

def imageCallback(data):
	print("Width: " + str(data.width) + "   Height: " + str(data.height) )
	print(data.data)

def scanCallback(data):
	print("Field of view:" + str(data.angle_max - data.angle_min))
	print("Max range: " + str(data.range_max))
	print("Min range: " + str(data.range_min))
	print("Ranges: " + str(ranges))

def listener():
	rospy.init_node('sensors', anonymous=True)
	rospy.Subscriber("/camera/depth_registered/points", PointCloud2, pointCallback)
	rospy.Subscriber("/camera/rgb/image_raw", Image, imageCallback)
	rospy.Subscriber("/scan", LaserScan, scanCallback)
	rospy.spin()


if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
		pass