#!/usr/bin/env python

# geom_utils.py
# util functions for geometry in simple polygons

import random, math
from math import sqrt,cos,sin,atan2,pi

def PolyToWindowScale(poly, ydim):
    newpoly = []
    for p in poly:
        newpoly.append((p[0]/2.0, ydim - p[1]/2.0))
    return newpoly

def PointToWindowScale(p, ydim):
     return (p[0]/2.0, ydim - p[1]/2.0)

# r is left of the vector formed by p->q
def IsLeftTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) > 0

# r is right of the vector formed by p->q
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

# checks if vector sp->bp points within edge p1p2
# start point, boundary point, edge p1, edge p2
def BouncePointInEdge(sp,bp,ep1,ep2):
    return ((IsLeftTurn(sp,bp,ep2) and
             IsRightTurn(sp,bp,ep1)) or
            (IsRightTurn(sp,bp,ep2) and
             IsLeftTurn(sp,bp,ep1)))

# find line intersection parameter of edge (v1,v2)
# state :: (x,y,theta) initial point and angle of ray
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
    t = (-c - b*y1 - a*x1)/(a*cos(theta)+b*sin(theta))
    pint = (x1 + cos(theta)*t, y1 + sin(theta)*t)
    return t, pint

# test if point p is in poly using crossing number
def IsInPoly(p, poly):
    intersects = 0
    theta = random.random()*2*pi
    state=(p[0],p[1],theta)
    psize = len(poly)
    for j in range(psize):
        v1, v2 = poly[j], poly[(j+1) % psize]
        t, pt = ShootRay(state, v1, v2)
        if t>0 and BouncePointInEdge(p, pt, v1, v2):
            intersects += 1
    return not (intersects%2 == 0)

# shoot a ray starting at p1, along vector p1->p2
# find intersection with edge v1,v2
def ShootRayFromVect(p1, p2, v1, v2):
    (x1,y1), (x2,y2) = p1, p2
    (x,y) = (x2-x1, y2-y1) # recenter points so p1 is at origin
    theta = FixAngle(math.atan2(y,x))
    return ShootRay((x2, y2, theta), v1, v2)

def ClosestPtAlongRay(p1,p2,last_bounce_edge,poly):
    psize = len(poly)
    closest_bounce = 100000000000
    bounce_point = (0.0, 0.0)

    # check each edge for collision
    for j in range(psize):
        if (j != last_bounce_edge):
            v1, v2 = poly[j], poly[(j+1) % psize]
            x1, y1 = p2[0], p2[1]
            # The line parameter t; needs divide by zero check!
            t,pt = ShootRayFromVect(p1, p2, v1, v2)
            
            # Find closest bounce for which t > 0
            pdist = PointDistance(pt,p2)
            if ((t > 0) and (pdist < closest_bounce) and
                BouncePointInEdge((x1,y1),pt,v1,v2)):
                bounce_point = pt
                closest_bounce = pdist
                #bounce_param = t
                #b_edge = j
    return bounce_point

def FindReflexAngles(poly):
    psize = len(poly)
    reflex_verts = []

    for j in range(psize):
        v1, v2, v3 = poly[(j-1) % psize], poly[j], poly[(j+1) % psize]
        if IsRightTurn(v1,v2,v3):
            reflex_verts.append(j)

    return reflex_verts
