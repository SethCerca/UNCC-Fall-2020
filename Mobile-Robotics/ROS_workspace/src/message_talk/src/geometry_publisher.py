#!/usr/bin/env python

import rospy
import random
from geometry_msgs.msg import Point

def talker():
	pub = rospy.Publisher('my_points', Point, queue_size=10)
	rospy.init_node("testing_msgs_a", anonymous=True)
	msg = Point()
	rate = rospy.Rate(30)
	while not rospy.is_shutdown():
		msg.x = random.random()
		msg.y = random.random()
		pub.publish(msg)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass