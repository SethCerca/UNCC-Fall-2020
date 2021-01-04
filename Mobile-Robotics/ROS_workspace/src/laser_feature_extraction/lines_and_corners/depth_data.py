#!/usr/bin/env python

from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import rospy
import math

pub_rviz = rospy.Publisher('visualization_marker', Marker, queue_size=10)

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


def buildRvizCorners(corners):

	pointMarker = Marker()
	pointMarker.header.frame_id = 'base_scan'
	pointMarker.header.stamp = rospy.Time(0)
	pointMarker.ns = ''

	pointMarker.id = 10
	pointMarker.type = 8
	pointMarker.action = 0
    
	pointMarker.scale.x = 0.2
	pointMarker.scale.y = 0.2
	pointMarker.scale.z = 0.2

	pointMarker.color.b = 1.0
	pointMarker.color.a = 1.0
	pointMarker.colors.append(pointMarker.color)

    
	for c in corners:
		pointMarker.points.append(c.p)

	#pub_rviz.publish(pointMarker)
	return pointMarker


def buildRvizLineList(lines):

	line_list = Marker()
	line_list.header.frame_id = 'base_scan'
	line_list.header.stamp = rospy.Time(0)
	line_list.ns = ''

	line_list.id = 0
	line_list.type = 5
	line_list.action = 0
 
	line_list.scale.x = 0.02

	line_list.color.g = 1.0
	line_list.color.a = 1.0

	# Add the line endpoints to list of points
	for l in lines:
		line_list.points.append(l.p_a)
		line_list.points.append(l.p_b)
    
	return line_list


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


def callback(data):
	zeros = Point(0.0, 0.0, 0.0)
	out = []

	for i in range(0, len(data.ranges)):

		angle = (i * data.angle_increment) + data.angle_min

		p = getRosPointFromAngle(angle, data.ranges[i])


		if (not (math.isnan(p.x) or math.isnan(p.y))):
			out.append(p)

	lines = getAllLines(out)
	plotLines(lines)
	
	corners = getCornersFromLines(lines)
	plotCorners(corners)


def plotCorners(corners):
	m = buildRvizCorners(corners)

	rospy.sleep(0.15)

	pub_rviz.publish(m)


def plotLines(lines):
    m = buildRvizLineList(lines)

    # Need to sleep before publishing 
    rospy.sleep(0.15)

    # Publish the marker
    pub_rviz.publish(m)


def main():

    print 'In main'

    rospy.init_node('plot_scans', anonymous=True)

    # Subscribers
    sub_scans = rospy.Subscriber('scan', LaserScan, callback)

    print 'Spinning'
    rospy.spin()


if __name__ == '__main__':
    main()
