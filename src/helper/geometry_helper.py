''' Utility functions for geometry in simple polygons
'''
import numpy as np
import numpy.linalg as la

from src.helper.shoot_ray_helper import *

# Do we have theta1 <= theta <= theta2 (mod 2pi) ?
# It is just a particular cyclic permutation
def FixAngle(theta):
    return theta % (2.0*np.pi)

# angle between two vectors in range [0,pi]
def GetVector2Angle(v1, v2):
    ratio = max(min(np.dot(v1, v2)/(la.norm(v1)*la.norm(v2)), 1), -1)
    return np.arccos(ratio)

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

def IsInPoly(p, poly):
    ''' test if point p is in poly using crossing number
    '''
    intersects = 0
    theta = np.random.rand()*2*np.pi
    state=(p[0],p[1],theta)
    psize = len(poly)
    for j in range(psize):
        v1, v2 = poly[j], poly[(j+1) % psize]
        try:
            t, pt = ShootRay(state, v1, v2)
            if t>0 and BouncePointInEdge(p, pt, v1, v2):
                intersects += 1
        except:
            pass
    return not (intersects%2 == 0)



