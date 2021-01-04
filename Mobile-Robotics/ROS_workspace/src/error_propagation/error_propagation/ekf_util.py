import numpy
import tf
import math


###############################################################
# Turtlebot3 hardware data
# TB3 encoders have 12-bit resolution so 4096 ticks per revolution
# TB3 Rw = 143.5mm = 0.1435m
TICKS_PER_REV = 4096.0
WHEEL_CIRCUMFERENCE = 0.2073 #m
Rw = 0.1435 #m
###############################################################


def findDistanceBetweenAngles(a, b):
    #print 'In findDistanceBetweenAngles'
    
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
    #print('In displaceAngle')

    a2 = a2 % (2.0*math.pi)

    if a2 > math.pi:
        a2 = (a2 % math.pi) - math.pi


    #print('Exiting displaceAngle')
    return findDistanceBetweenAngles(-a1,a2)


def getG(x, u):
    #print('In getG')
 
    theta = tf.transformations.euler_from_quaternion([x.orientation.x, x.orientation.y, x.orientation.z, x.orientation.w])[2]

    d = (u[0] + u[1]) / 2.0
    dtheta = (u[1] - u[0]) / (2.0*Rw)

    G = numpy.matrix('1 0 -1; 0 1 -1; 0 0 1', float)
    G[0,2] = -d*math.sin(displaceAngle(theta,dtheta))
    G[1,2] = d*math.cos(displaceAngle(theta,dtheta))

    return G

def getV(x, u):
    #print('In getV')
    
    d = (u[0] + u[1]) / 2.0
    dtheta = (u[1] - u[0]) / (2.0*Rw)

    #print('u: %s' % u)
    #print('d: %s dtheta: %s cos(%s): %s' % (d, dtheta, dtheta, math.cos(dtheta)))
    
    theta = tf.transformations.euler_from_quaternion([x.orientation.x, x.orientation.y, x.orientation.z, x.orientation.w])[2]


    # Create the matrix
    V = numpy.matrix('-1 -1; -1 -1; 0 1', float)
    V[0,0] = ( (-d*math.sin(displaceAngle(theta, dtheta))) / (2.0*Rw)) + ( math.cos(displaceAngle(theta,dtheta)) / 2.0)

    V[0,1] = (d*math.sin(displaceAngle(theta, dtheta))  / (2.0*Rw)) + ( math.cos(displaceAngle(theta,dtheta)) / 2.0)

    V[1,0] = (d*math.cos(displaceAngle(theta, dtheta))  / (2.0*Rw)) + ( math.sin(displaceAngle(theta,dtheta)) / 2.0)

    V[1,1] = (-d*math.cos(displaceAngle(theta, dtheta))  / (2.0*Rw)) + ( math.sin(displaceAngle(theta,dtheta)) / 2.0)
    
    V[2,0] = (1.0 / (2.0*Rw))

    V[2,1] = (-1.0/(2.0*Rw))

    return V

def getE(prev_E, G, V, M):
    #print('In getE')
    
    E = G * prev_E * G.T
    F = (V * M * V.T)
    E += F

    return E

def getM(u, alpha):
    #print('In getM')
    M = numpy.mat('25.0 0.0; 0.0 25.0')


    # a = encoder difference for this tick?
    a_l = u[0]
    a_r = u[1]

    # b is standard deviation. +- 5 ticks
    b = 5


    M[0,0] = alpha*a_l
    M[1,1] = alpha*a_r

    #print('M: %s' % M)

    return M



def getH(corner, meanPose, q):

    H = numpy.mat('0.0 0.0 0.0; 0.0 0.0 -1.0; 0.0 0.0 0.0')
    H[0,0] = -( corner.p.x - meanPose.position.x   / math.sqrt(q))
    H[0,1] = -( corner.p.y - meanPose.position.y   / math.sqrt(q))


    return H