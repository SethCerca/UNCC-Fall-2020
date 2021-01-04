#!/usr/bin/env python


from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry 
import tf.transformations
import rospy
import math

twist = Twist()
twist.linear.x = 0.2
twist.angular.z = 0
odo = Odometry()


def driveDistance(dist):
	global odo
	travel = math.sqrt(math.pow(odo.pose.pose.position.x, 2) + 
						math.pow(odo.pose.pose.position.y, 2))
	if travel  < dist:
		return(False)
	else:
		return True
		

def turnTo(theta):
	global odo
	global twist
	twist.angular.z = 0.2
	twist.linear.x = 0
	quaternion = (
		odo.pose.pose.orientation.x,
		odo.pose.pose.orientation.y,
		odo.pose.pose.orientation.z,
		odo.pose.pose.orientation.w)
	euler = tf.transformations.euler_from_quaternion(quaternion)
	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]
	theta = rosAngle(theta)
	print(theta)
	print(yaw)
	if theta + .01 > yaw and yaw > theta - .01: 
		return True
	else:
		return False	

def rosAngle(theta):
	theta %=  360
	if theta > 180:
		theta -= 360
	theta *= math.pi / 180 
	return theta


def callback(data):
	global odo
	odo = data


def listener():
	rospy.Subscriber('odom', Odometry, callback)


def talker():
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	rospy.init_node("drive_robot", anonymous = True)
	listener()
	dist = 1
	theta = 180
	rate = rospy.Rate(30)	
	while not rospy.is_shutdown():
		pub.publish(twist)
		if driveDistance(dist):
			break
		if turnTo(theta):
			break

		rate.sleep()
	

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass