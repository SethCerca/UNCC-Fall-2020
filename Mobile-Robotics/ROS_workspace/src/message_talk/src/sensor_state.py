#!/usr/bin/env python

import rospy
from turtlebot3_msgs.msg import SensorState

def callback(data):
	print("(Left, Right): " + "(" + str(data.left_encoder) + "," + str(data.right_encoder) + ")")

def listener():
	rospy.init_node('sensor_state', anonymous=True)
	rospy.Subscriber('sensor_state', SensorState, callback)
	rospy.spin()
	

if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
		pass