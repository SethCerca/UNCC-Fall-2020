#!/usr/bin/env python

import rospy
from turtlebot3_msgs.msg import SensorState

def talker():
	pub = rospy.Publisher('sensor_state', SensorState, queue_size=10)
	rospy.init_node("sensor_output", anonymous=True)
	msg = SensorState()
	msg.left_encoder = 1159
	msg.right_encoder = 859
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		pub.publish(msg)
		rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass