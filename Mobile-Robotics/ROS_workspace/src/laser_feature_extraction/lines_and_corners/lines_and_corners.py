#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point


pub_rviz = rospy.Publisher('visualization_marker', Marker, queue_size=10)


#Returns a tuple containing the x any y coordinates of a point on the unit circle
#scaled using the radius
def getXYFromAngle(rad, dist):
    return (dist * math.cos(rad), dist * math.sin(rad))


#Makes a point using radians and a distance to a point
def getRosPointFromAngle(rad, dist):
    p = getXYFromAngle(rad, dist)
    point = Point()

    point.x = p[0]
    point.y = p[1]
    
    return point


def findDistanceBetweenAngles(a,b):
    result = 0
    
    difference = b - a
    if difference > math.pi:
        difference = math.fmod(difference, math.pi)
        result = difference - math.pi

    elif difference < -math.pi:
        result = difference + (2.0*math.pi)

    else:
        result = difference

    return result


def displaceAngle(a, b):

    b = math.fmod(b, 2.0*math.pi)
    if b > math.pi:
        b = math.fmod(b, math.pi) - math.pi

    return findDistanceBetweenAngles(-a, b)


def scanCb(data):
    out = []

    for i in range(0, len(data.ranges)):

        # Get the angle. This is in [0,2PI] range.
        angle = (i * data.angle_increment) + data.angle_min

        p = getRosPointFromAngle(angle, data.ranges[i])

        if (not (math.isnan(p.x) or  math.isnan(p.y))):
            out.append(p)

        print("Len of out: " + str(len(out)))
    # Call this to publish your points on topic /visualization_marker
    # Rviz will display each point as a red dot
    plotPoints(out)


# Publish a list of points for rviz to show
# points should be a list of geometry_msgs/Point objects
def plotPoints(points):
    m = getMarkerWithPoints(points)

    # Need to sleep before publishing 
    rospy.sleep(0.15)

    # Publish the marker
    pub_rviz.publish(m)

# points is a list of geometry_msgs/Point objects
def getMarkerWithPoints(points):
    #print 'In plotPoint'

    marker = Marker()

    # TB2
    #marker.header.frame_id = 'camera_depth_frame'

    # TB3
    marker.header.frame_id = 'base_scan'

    marker.header.stamp = rospy.Time(0)
    marker.ns = ''

    # Id of marker will always be 0
    marker.id = 0
    marker.type = 8 # Points
    marker.action = 0 # Add

    # Set color and then append to colors array
    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 1.0
    marker.color.a = 1.0

    for p in points:
        marker.points.append(p)
        marker.colors.append(marker.color)

    # Set size 
    marker.scale.x = 0.02
    marker.scale.y = 0.02
    marker.scale.z = 0.02

    # Show for 10 seconds. Maybe pass this as a param?
    marker.lifetime = rospy.Duration(10.0)

    return marker


def main():

    print 'In main'

    rospy.init_node('plot_scans', anonymous=True)

    # Subscribers
    sub_scans = rospy.Subscriber('scan', LaserScan, scanCb)

    print 'Spinning'
    rospy.spin()



if __name__ == '__main__':
    main()
