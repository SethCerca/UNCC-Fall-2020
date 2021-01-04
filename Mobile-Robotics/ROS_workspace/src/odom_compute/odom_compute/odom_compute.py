#!/usr/bin/env python


from turtlebot3_msgs.msg import SensorState
from nav_msgs.msg import Odometry 
import rospy
import math
import tf.transformations


class State:
	def __init__(self, x, y, theta, vx, vy, vtheta):
		self.x = x
		self.y = y
		self.theta = theta
		self.vx = vx
		self.vy = vy
		self.vtheta = vtheta


x_primt = State(0, 0, 0, 0, 0, 0)
x = State (0, 0, 0, 0, 0, 0) 


class Encoder:
	def __init__(self, value):
		self.value = value
		self.past = None

up = Encoder([0, 0])


def transitionModel(x, u):
	rw = 0.1435
	tickDist = .0000506
	theta = 0
	dist = 0

	dr = (u[1] - up.past[1]) * tickDist
	dl = (u[0] - up.past[0]) * tickDist
	theta = ((dr-dl)/(2*rw))

		##     calculations for x.theta    ##

	x.theta +=  displaceAngle(theta, x.theta) -  x.theta

  		##    calculations for x and y componets    ##

	dist +=  ((dl + dr) / 2)
	x.x += dist*math.cos(theta)
	x.y += dist*math.sin(theta)

		##    calculations for velocity    ##
	
	vl = dl/.0333
	vr = dr/.0333
	v = (vl + vr)/2
	x.vtheta = (vr - vl)/(2 * rw)
	x.vx = v*math.cos(theta)
	x.vy = v*math.sin(theta)

	return x	


def findDistanceBetweenAngles(a, b):
	result = 0
	difference = b - a
    
	if difference > math.pi:
		difference = math.fmod(difference, math.pi)
		result = difference - math.pi

	elif(difference < -math.pi):
		result = difference + (2*math.pi)
	else:
		result = difference

	return result


def displaceAngle(a1, a2):

	a2 = a2 % (2.0*math.pi)
	if a2 > math.pi:
		a2 = (a2 % math.pi) - math.pi

	return findDistanceBetweenAngles(-a1,a2)


def buildOdomMsg(state, odomMsg):
	odomMsg.pose.pose.position.x = x.x
	odomMsg.pose.pose.position.y = x.y
	q = tf.transformations.quaternion_from_euler(0, 0, x.theta )
	odomMsg.pose.pose.orientation.z = q[2]
	odomMsg.pose.pose.orientation.w = q[3]
	odomMsg.twist.twist.linear.x = x.vx
	odomMsg.twist.twist.linear.y = x.vy
	q = tf.transformations.quaternion_from_euler(0, 0, x.vtheta)
	odomMsg.twist.twist.angular.z = q[2]
	pub = rospy.Publisher('my_odom', Odometry, queue_size=10)
	pub.publish(odomMsg)

def talker():
	rospy.init_node('sensor_state', anonymous=True)
	rate = rospy.Rate(10)
	listener()
	while not rospy.is_shutdown():
		rate.sleep()


def callback(data):
	u = [data.left_encoder, data.right_encoder]
	up.past = up.value
	up.value = u
	x_prime = transitionModel(x, u)
	odomMsg = Odometry()
	buildOdomMsg(x_prime, odomMsg)


def listener():
	rospy.Subscriber('sensor_state', SensorState, callback)

	

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass