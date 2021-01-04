#!/usr/bin/env python

import rospy
from message_talk.msg import MyMsg

def talker():
	pub = rospy.Publisher('mymsg_a', MyMsg, queue_size=10)
	rospy.init_node("testing_msgs_a", anonymous=True)
	msg = MyMsg()
	msg.id = 1159
	msg.message = "Hello There"
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		pub.publish(msg)
		rate.sleep()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass