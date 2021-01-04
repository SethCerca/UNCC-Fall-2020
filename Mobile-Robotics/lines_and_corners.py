#!/usr/bin/env python

from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import rospy
import math

marker = Marker()

class Lines():
	def __init__(self, A, B, C, p_a, p_b, id, msg): 
		self.A = A
		self.B = B		
		self.C = C
		self.p_a = Point(p_a[0], p_a[1], 0)
		self.p_b = Point(p_b[0], p_b[1], 0)
		self.msg = msg
		self.length = self.setLength()
		self.slope = self.setSlope()

	def setLength(self):
		length = math.sqrt(math.pow(self.p_a.x - self.p_b.x, 2) + 
			math.pow(self.p_a.y - self.p_b.y, 2))		
		return length

	def setSlope(self):
		rise = (self.p_b.y - self.p_a.y)
		run = (self.p_b.x - self.p_a.x)
		slope = rise / float(run)
		return slope

class Corners():
	def __init__(self, p, psi, id, l_a, l_b, ):
		self.p = Point(p[0], p[1], 0)
		self.psi = psi
		self.id = id
		self.l_a = Lines(0, 0, 0, l_a[0], l_a[1], 0, 0)
		self.l_b = Lines(0, 0, 0, l_b[0], l_b[1], 0, 0)


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


# Make an rviz line list given a list of Line objects
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


def talker():
	global marker
	pub = rospy.Publisher('/visualization_marker', Marker, queue_size = 10)
	rate = rospy.Rate(30)
	while not rospy.is_shutdown():
		pub.publish(marker)
		rate.sleep()


def callback():
	pass

def listener():
	rospy.Subscriber('/scan', LaserScan, callback)


def main():
	global marker
	rospy.init_node('lines_and_corners', anonymous=True)
	lines = []
	corners = []
	lineA = Lines(0, 0, 0, [3, 5], [1, 8], 0, 0)
	lineB = Lines(0, 0, 0, [1, 2], [9, 5], 0, 0)
	cornerA = Corners([1, 1], 0, 0, [[3, 5], [1, 8]], [[3, 5], [2, 2]])
	cornerB = Corners([-1, -1], 0, 0, [[1, 2], [9, 5]], [[9, 5], [6, 3]])


	lines.append(lineA)
	lines.append(lineB)
	corners.append(cornerA)
	corners.append(cornerB)

	#marker = buildRvizLineList(lines)
	marker = buildRvizCorners(corners)
	print(marker)
	listener()
	talker()


if __name__ == '__main__':
	main()
