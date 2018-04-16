#!/usr/bin/env python

# bounce.py
# This program simulates the bouncing of balls
# under various bouncing strategies
#
# Written by Steve LaValle
# November 2011

import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2,pi
from time import sleep
from maps import *

#constants
XDIM = 500
YDIM = 500
WINSIZE = [XDIM, YDIM]
EPSILON = 1.0
NUMBOUNCES = 100000
MAXDIST = 10000000.0

def PolyToWindowScale(poly):
    newpoly = []
    for p in poly:
        newpoly.append((p[0]/2.0,YDIM - p[1]/2.0))
    return newpoly

def PointToWindowScale(p):
     return (p[0]/2.0,YDIM - p[1]/2.0)

def IsLeftTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) > 0

def IsRightTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) < 0

# Do we have theta1 <= theta <= theta2 (mod 2pi) ?
# It is just a particular cyclic permutation
def AngleBetween(theta,theta1,theta2):
    return (((theta1 <= theta) and (theta <= theta2)) or \
            ((theta2 <= theta1) and (theta1 <= theta)) or \
            ((theta <= theta2) and (theta2 <= theta1)))

def AngleDistance(theta1,theta2):
    d = abs(theta1-theta2)
    return min(d,2.0*pi-d)

def AngleDifference(theta1,theta2):
    d = theta2 - theta1
    if (d < pi):
        d += 2.0*pi;
    if (d > pi):
        d -= 2.0*pi;
    return d

def PointDistance(p,q):
    return sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]))

def FixAngle(theta):
    return theta % (2.0*pi)

# n is the inward edge normal (in degrees 0 to 2pi)

def PerformBounce(s,bp,n,strategy):

    # Random bounce
    if strategy == 0:
        dir = n + random.random()*pi - pi/2.0
    elif strategy == 1:
    # Right angle bounce
        dir = s[2] + pi/2.0
        if AngleDistance(dir,n) > pi/2.0:
            dir += pi
    elif strategy == 2:
    # Billiard bounce
        rebound = FixAngle(s[2] + pi)
#    print "ad:",AngleDifference(rebound,n),"rebound:",rebound,"n:",n
        dir = rebound + 2.0*AngleDifference(rebound,n)
    elif strategy == 3:
    # Normal bounce
        dir = n

    dir = FixAngle(dir)
    if AngleDistance(dir,n) > pi/2.0:
        print("Error: Illegal bounce.  n:",n,"dir:",dir)
#    print "n:",n,"dir:",dir,"angledist:",AngleDistance(dir,n)
    return (bp[0], bp[1], dir)

# r is left of the vector formed by p->q
def IsLeftTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) > 0


# r is right of the vector formed by p->q
def IsRightTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) < 0

# checks if vector sp->bp points within edge p1p2
# start point, boundary point, edge p1, edge p2
def BouncePointInEdge(sp,bp,ep1,ep2):
    return ((IsLeftTurn(sp,bp,ep2) and
             IsRightTurn(sp,bp,ep1)) or
            (IsRightTurn(sp,bp,ep2) and
             IsLeftTurn(sp,bp,ep1)))

# find line intersection parameter from p1 at angle theta with edge e1
def ShootRay(state, v1, v2):
    x1 = state[0]
    y1 = state[1]
    theta = state[2]
    x2 = v1[0]
    y2 = v1[1]
    x3 = v2[0]
    y3 = v2[1]
    a = y3 - y2
    b = x2 - x3
    c = y2*(x3-x2) - x2*(y3-y2)
    return (-c - b*y1 - a*x1)/(a*cos(theta)+b*sin(theta))

# test if point p is in poly using crossing number
def IsInPoly(p, poly):
    intersects = 0
    theta = random.random()*2*pi
    state=(p[0],p[1],theta)
    psize = len(poly)
    for j in range(psize):
        v1, v2 = poly[j], poly[(j+1) % psize]
        t = ShootRay(state, v1, v2)
        x1, y1 = p[0], p[1]
        pint = (x1 + cos(theta)*t, y1 + sin(theta)*t)
        if t>0 and BouncePointInEdge(p, pint, v1, v2):
            intersects += 1
    return not (intersects%2 == 0)

def main():
    # Initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Bouncing Strategies    University of Illinois     November 2011')
    white = 255, 240, 200
    black = 20, 20, 40    
    green = 50, 130, 50
    screen.fill(black)
    pint = (0.0,0.0)

    # This sets the billiard boundary
    poly = bigpoly

    # Set the initial ball state (x,y,theta)
    state = (200.0, 200.0, 2.0)

    last_bounce_edge = -1

    for i in range(NUMBOUNCES):

        psize = len(poly)
        closest_bounce = MAXDIST
        bnormal = -1.0  # The inward edge normal of the bounce point

        pygame.draw.polygon(screen,white,PolyToWindowScale(poly),5)
        # check each edge for collision
        for j in range(psize):
            if (j != last_bounce_edge):
                v1, v2 = poly[j], poly[(j+1) % psize]
                x1, y1 = state[0], state[1]
                # The line parameter t; needs divide by zero check!
                t = ShootRay(state, v1, v2)
                #t = (-c - b*y1 - a*x1)/(a*cos(state[2])+b*sin(state[2]))
                pint = (x1 + cos(state[2])*t, y1 + sin(state[2])*t)
                
                # Find closest bounce for which t > 0
                pdist = PointDistance(pint,(state[0],state[1]))
                if ((t > 0) and (pdist < closest_bounce) and
                    BouncePointInEdge((x1,y1),pint,v1,v2)):
                    bounce_point = pint
                    closest_bounce = pdist
                    bnormal = FixAngle(pi/2.0 + 
                                       atan2(poly[(j+1)%psize][1]-poly[j][1],\
                                             poly[(j+1)%psize][0]-poly[j][0]))
                    bounce_edge = j
#                    print "bnormal:",bnormal
#                    print "pdist:",pdist,"closest_bounce:",closest_bounce,"pint:",pint

#            pygame.draw.circle(screen,green,PointToWindowScale(pint),5)
#        raw_input("Press Enter to continue...")

#        print "closest_bounce:",closest_bounce,"bounce_point:",bounce_point
        pygame.draw.line(screen,green,PointToWindowScale(bounce_point),\
                         PointToWindowScale((state[0],state[1])))
        pygame.display.update()
#        print "state:",state
        sleep(0.1)

# Set the last argument to PerformBounce:
# 0 = random, 1 = right angle, 2 = billiard, 3 = normal
        state = PerformBounce(state,bounce_point,bnormal,3)
        last_bounce_edge = bounce_edge

        for e in pygame.event.get():
	        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
	            sys.exit("Leaving because you requested it.")
    while (1):
        1 == 1

# if python says run, then we should run
if __name__ == '__main__':
    main()


