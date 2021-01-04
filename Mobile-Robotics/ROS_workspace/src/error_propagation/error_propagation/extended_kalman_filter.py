#!/usr/bin/env python

from turtlebot3_msgs.msg import SensorState
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Pose, Point
from nav_msgs.msg import Odometry 
from ekf_util import *
import rospy
import math
import numpy


pose = Pose()
encoder = [0, 0]
past = [0, 0, 0]
cov = numpy.mat('1 1 1; 1 1 1; 1 1 1', float)  
z = numpy.mat('0; 0; 0', float)
u = [0, 0]
H = 0
corners = []



class Lines():
	def __init__(self, p_a, p_b, msg): 
		self.p_a = p_a
		self.p_b = p_b
		self.length = self.setLength()
		self.slope = self.setSlope()
		self.A = self.setA()
		self.B = self.setB()		
		self.C = self.setC()
		self.msg = msg

	def setLength(self):
		length = math.fabs(math.sqrt(math.pow(self.p_b.x - self.p_a.x, 2) + 
			math.pow(self.p_b.y - self.p_a.y, 2)))		
		return length

	def setSlope(self):
		rise = (self.p_b.y - self.p_a.y)
		run = (self.p_b.x - self.p_a.x)
		if(run == 0):
			return 1
		slope = rise / float(run)
		return slope

	def setA(self):
		a = (self.p_a.y - self.p_b.y)
		return a

	def setB(self):
		b = (self.p_b.x - self.p_a.x)
		return b

	def setC(self):
		c = ((self.p_a.x * self.p_b.y) - (self.p_b.x * self.p_a.y))
		return c


class Corners():
	def __init__(self, p, psi, id, l_a, l_b, ):
		self.p = p
		self.psi = psi
		self.id = id
		self.l_a = l_a
		self.l_b = l_b


def getAllLines(points):
	lines = []
	toProcess = []
	done, index = getLine(points, True)

	if done:
		lines.append(getLineBetweenPoints(points[0], points[len(index) - 1]))

	for i in range(0, len(points)):
		if points[i] == index:
			partition1 = points[:i + 1]
			partition2 = points[i + 1:]
			toProcess.append(partition1)
			toProcess.append(partition2)

	while len(toProcess) > 0:

		done, index = getLine(toProcess[0], False)
		if index == 1:
			toProcess.pop(0)

		elif done:
			if index.length != 0.0:
				if not (0.0 in (index.p_a.x, index.p_a.y, index.p_b.x, index.p_b.y)):
					lines.append(index)
			toProcess.pop(0)
			
		else:
			c = toProcess[0].index(index)
			partition1 = toProcess[0][: c + 1]
			partition2 = toProcess[0][c + 1 :]
			toProcess.append(partition1)
			toProcess.append(partition2)
			toProcess.pop(0)
	
	return lines


def getLine(points, first):

	dMax = 0
	point = []

	if first:
		for i in points:
			dTemp = math.fabs(math.sqrt(math.pow(points[0].x - i.x, 2) + 
				math.pow(points[0].y - i.y, 2)))
			if dTemp > dMax:
				dMax = dTemp
				point = i
		if dMax < .01:
			return True, point
		return False, point

	line = getLineBetweenPoints(points[0], points[len(points) - 1])

	if line.p_a == line.p_b:
		return 1, 1 

	for i in points:
		if (i.x != 0 and i.y != 0):
			dTemp = getDistanceToLine(line, i)
			if dTemp > dMax:
				dMax = dTemp
				point = i

	if dMax < .06:
		return True, line

	return False, point


def getDistanceToLine(line, point):

	n = math.fabs(math.sqrt(math.pow(line.A, 2) + math.pow(line.B, 2)))
	a = line.A / n
	b = line.B / n
	c = line.C / n
	d = math.fabs((a * point.x) + (b * point.y) + c)
	return d


def getLineBetweenPoints(pointA, pointB):

	line = Lines(pointA, pointB, 0)
	return line


def getCornersFromLines(lines):

	corners = []

	for i in range(0, len(lines) - 1):
		dist = getLineBetweenPoints(lines[i].p_b, lines[i + 1].p_a)
		angle = getAngleBetweenLines(lines[i], lines[i + 1])

		if (dist.length < .4) and (angle < 2):
			corner = Point(( dist.p_a.x + dist.p_b.x ) / 2, (dist.p_a.y + dist.p_b.y ) / 2, 0) 
			cornerObj = Corners(corner, 0, 0, lines[i], lines[i + 1])
			corners.append(cornerObj)

	return(corners)


def getAngleBetweenLines(l_a, l_b):

    nom = l_a.A - l_b.A;
    denom = 1.0 + (l_a.A*l_b.A)
    theta = math.atan2(nom, denom)

    return theta


def getXYFromAngle(rad, dist):
    return (dist * math.cos(rad), dist * math.sin(rad))


def getRosPointFromAngle(rad, dist):
    p = getXYFromAngle(rad, dist)
    point = Point()

    point.x = p[0]
    point.y = p[1]
    
    return point


def cornerCallback(data):
	global corners
	zeros = Point(0.0, 0.0, 0.0)
	out = []

	for i in range(0, len(data.ranges)):

		angle = (i * data.angle_increment) + data.angle_min

		p = getRosPointFromAngle(angle, data.ranges[i])


		if (not (math.isnan(p.x) or math.isnan(p.y))):
			out.append(p)

	lines = getAllLines(out)
	
	corners = getCornersFromLines(lines)
	
	


def findCorners():
    # Subscribers
    sub_scans = rospy.Subscriber('scan', LaserScan, cornerCallback)




def transitionModel(data):
	global u
	global pose
	global past

	# Initializes the variables to be used
	rw = 0.1435
	tickDist = .0000506
	theta = 0
	dist = 0

	# Calculates the distance traveled by each wheel

	dr = data[1] * tickDist
	dl = data[0] * tickDist
	u[0] = dl - past[0]
	u[1] = dr - past[1]
	past[2] = theta
	theta = ((dr - past[1]) - (dl - past[0])) / (2 * rw)
	past[0] = dl
	past[1] = dr


	# Calculations for orientation

	pose.orientation.z +=  displaceAngle(theta, past[2]) - past[2]

  	# Calculations for x and y componets

	dist +=  ((dl + dr) / 2)
	pose.position.x = dist*math.cos(theta)
	pose.position.y = dist*math.sin(theta)


def calcCovariance(oldPose):
	global cov
	global u

	G = getG(oldPose, u)
	V = getV(oldPose, u)
	M = getM(u, .05)

	cov = G * cov * numpy.transpose(G) + V * M * numpy.transpose(V)
	# print("Pose: ")
	# print(pose)
	# print("Covariance: ")
	# print(cov)


def predict(data):
	global pose
	global u

	oldPose = pose
	transitionModel(data)
	calcCovariance(oldPose)


def measure(data):
	global corners
	global cov
	global pose

	findCorners()

	z = numpy.mat('0; 0; 0', float)
	Q = numpy.mat('0 0 0; 0 0 0; 0 0 1', float)
	I = numpy.mat('1 0 0; 0 1 0; 0 0 1', float)

	# Observed locations
	poseRef = pose.position
	poseRef.y = pose.position.y + 1
	pointB = Point(pose.position.x, pose.position.y, pose.position.z)
	poseLine = getLineBetweenPoints(pointB, poseRef)

	# Actual locations
	locationA = Point(data.pose.pose.position.x, data.pose.pose.position.y, data.pose.pose.position.z)
	locationB = Point(data.pose.pose.position.x, data.pose.pose.position.y + 1, data.pose.pose.position.z)
	realPos = getLineBetweenPoints(locationA, locationB)


	for x in corners:
		pointA = x.p
		dist = getLineBetweenPoints(pointA, pointB)
		distActual = getLineBetweenPoints(pointA, data.pose.pose.position)
		r = dist.length
		phi = getAngleBetweenLines(poseLine, dist)

		# Calculating the percent error
		z[0, 0] = r 
		z[1, 0] = phi

		Q[0, 0] = z[0, 0]
		Q[1, 1] = z[1, 0]

		H = getH(x, pose, dist.length)
		S = H * cov * numpy.transpose(H) + Q
		K = cov * numpy.transpose(H) * numpy.linalg.inv(S)
		cov = (I - K * H) * cov


def kalmanUpdate(event):
	global encoder
	predict(encoder)
	rospy.Subscriber('/odom', Odometry, measure)
	print("\n-----------------\nkalmanUpdate: \n -----------------")
	print("\nPose: ")
	print(pose)
	print("\ncavariance: ")
	print(cov)



def callback(data):
	global encoder
	encoder = [data.left_encoder, data.right_encoder]
	

def listener():
	rospy.init_node('sensor_state', anonymous=True)
	rospy.Subscriber('sensor_state', SensorState, callback)
	rospy.Timer(rospy.Duration(.1), kalmanUpdate, oneshot=False)
	rospy.spin()


if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
		pass