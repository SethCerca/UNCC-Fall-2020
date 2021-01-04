#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import String

def callbackA(data):
	print(data.data)

def callbackB(data):
	print(data.data)

def listener():
	rospy.init_node('node_c', anonymous=True)
	rospy.Subscriber('topic_a', String, callbackA)
	rospy.Subscriber('topic_b', UInt32, callbackB)
	rospy.spin()


if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
		pass