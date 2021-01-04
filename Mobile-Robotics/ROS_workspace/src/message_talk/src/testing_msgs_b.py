#!/usr/bin/env python

import rospy
from message_talk.msg import MyMsg
from nav_msgs.msg import Odometry

def callbackA(data):
	print(data)

def callbackB(data):
	print("(X,Y): " + "(" + str(data.pose.pose.position.x) + "," + str(data.pose.pose.position.y) + ")")

def listener():
	rospy.init_node('testing_msgs_b', anonymous=True)
	#rospy.Subscriber('mymsg_a', MyMsg, callbackA)
	rospy.Subscriber('odom', Odometry, callbackB)
	rospy.spin()

if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
		pass