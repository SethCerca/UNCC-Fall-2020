#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt32
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('topic_a', String, queue_size=10)
	rospy.init_node("node_a", anonymous=True)
	rate = rospy.Rate(10)
	listener()
	while not rospy.is_shutdown():
		hello_str = "This is node a's output"
		pub.publish(hello_str)
		rate.sleep()

def callback(data):
	print("node b's output: " + str(data.data))
	
def listener():
   	rospy.Subscriber('topic_b', UInt32, callback)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
