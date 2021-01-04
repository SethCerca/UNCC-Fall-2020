#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher("topic_b", UInt32, queue_size=10)
	rospy.init_node("node_b", anonymous=True)
	rate = rospy.Rate(10)
	num = 0
	listener()
	while not rospy.is_shutdown():
		pub.publish(num)
		num += 1
		rate.sleep()		

def callback(data):
	print(data.data)
	
def listener():
   	rospy.Subscriber('topic_a', String, callback)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass