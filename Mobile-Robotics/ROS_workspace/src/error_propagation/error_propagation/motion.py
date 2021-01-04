#!/usr/bin/env python


from turtlebot3_msgs.msg import SensorState
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry 
from jacobians import *
import tf.transformations
import rospy
import math
import numpy


pose = Pose()
pose.position.x = 0
pose.position.y = 0
pose.orientation.z = 0
cov = numpy.mat('1 1 1; 1 1 1; 1 1 1', float)  
controlInput = [0, 0]
leftData = [0]
rightData = [0]

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


def calcCovariance():
	global cov
	global pose
	global controlInput
	global leftData
	global rightData

	G = getG(pose, controlInput)
	V = getV(pose, controlInput)
	M = numpy.mat('0, 0; 0, 0', float)
	M[0, 0] = .05 * controlInput[0]
	M[1, 1] = .05 * controlInput[1]

	cov = G * cov * numpy.transpose(G) + V * M * numpy.transpose(V)
	print("Pose: ")
	print(pose)
	print("Covariance: ")
	print(cov)
	#print("G:\n" + str(G))
	#print("V:\n" + str(v))
	

def transitionModel(x, u):
	global pose
	global controlInput

	rw = 0.1435
	tickDist = .0000506
	theta = 0
	dist = 0

	dr = (u[1] - up.past[1]) * tickDist
	dl = (u[0] - up.past[0]) * tickDist
	theta = ((dr-dl)/(2*rw))
	controlInput[0] = dl
	controlInput[1] = dr
	leftData.append(dl)
	rightData.append(dr)

		##     calculations for x.theta    ##

	x.theta +=  displaceAngle(theta, x.theta) -  x.theta
	pose.orientation.z = x.theta

  		##    calculations for x and y componets    ##

	dist +=  ((dl + dr) / 2)
	x.x += dist*math.cos(theta)
	x.y += dist*math.sin(theta)
	pose.position.x = x.x
	pose.position.y = x.y

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
	calcCovariance()


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