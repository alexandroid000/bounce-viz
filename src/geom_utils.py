''' Utility functions for geometry in simple polygons
'''
import numpy as np

# Do we have theta1 <= theta <= theta2 (mod 2pi) ?
# It is just a particular cyclic permutation

def FixAngle(theta):
    return theta % (2.0*pi)

def PointDistance(p,q):
    return np.sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]))

def Points2Vect(p1,p2):
    return (p2[0]-p1[0], p2[1]-p1[1])

def GetVectorLen(v):
    return np.sqrt(sum((a*b) for a, b in zip(v, v)))

# angle between two vectors in range [0,pi]
def GetVector2Angle(v1, v2):
    dot_prod = v1[0]*v2[0]+v1[1]*v2[1]
    ratio = max(min(dot_prod/(GetVectorLen(v1)*GetVectorLen(v2)), 1), -1)
    return np.arccos(ratio)

# r is left of the vector formed by p->q
def IsLeftTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) > 0

# r is right of the vector formed by p->q
def IsRightTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) < 0

def IsIntersectSegments(p1, p2, q1, q2):
    return (IsLeftTurn(p1, p2, q1) != IsLeftTurn(p1, p2, q2)) and (IsLeftTurn(q1, q2, p1) != IsLeftTurn(q1, q2, p2))

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
    den = (a*np.cos(theta)+b*np.sin(theta))
    # case when lines are parallel
    if abs(den) < 0.000001:
        if DEBUG:
            print('divide by zero in ray shoot')
            print('shot from ',state,'to',v1,v2)
        raise ValueError
    else:
        t = (-c - b*y1 - a*x1)/den
        pint = (x1 + np.cos(theta)*t, y1 + np.sin(theta)*t)
    return t, pint

# shoot a ray starting at p1, along vector p1->p2
# find intersection with edge v1,v2
# will return first intersection *after* p2
def ShootRayFromVect(p1, p2, v1, v2):
    (x1,y1), (x2,y2) = p1, p2
    (x,y) = (x2-x1, y2-y1) # recenter points so p1 is at origin
    theta = FixAngle(np.arctan2(y,x))
    state = (p2[0], p2[1], theta)
    return ShootRay(state, v1, v2)

# shoot ray from p1 toward p2 in poly, return closest intersect point
# will not return point on 'last_bounce_edge'
def ClosestPtAlongRay(p1,p2,poly,last_bounce_edge=-1):
    psize = len(poly)
    closest_bounce = 100000000000
    bounce_point = (0.0, 0.0)
    found_coll = False
    bounce_edge = last_bounce_edge

    # check each edge for collision
    for j in range(psize):
        if (j != last_bounce_edge):
            v1, v2 = poly[j], poly[(j+1) % psize]
            x1, y1 = p2[0], p2[1]
            # The line parameter t; needs divide by zero check!
            try:
                t,pt = ShootRayFromVect(p1, p2, v1, v2)
                
                # Find closest bounce for which t > 0
                pdist = PointDistance(pt,p2)
                if ((t > 0) and (pdist < closest_bounce) and
                    BouncePointInEdge((x1,y1),pt,v1,v2)):
                    found_coll = True
                    bounce_point = pt
                    closest_bounce = pdist
                    bounce_edge = j
            # bounce was parallel to edge j
            # check if it's parallel and overlapping for degenerate polys
            except:
                pass
    if found_coll:
        return bounce_point, bounce_edge
    else:
        return False

#def MaxPreimage(e1, e2):


