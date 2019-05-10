# classify segments of polygon boundary according to whether they admit
# contraction mappings under a given angle theta

from helper.shoot_ray_helper import ShootRayFromVect
from helper.geometry_helper import IsRightTurn, IsLeftTurn
import numpy as np
import numpy.linalg as la

def normalize(vector):
    norm = np.linalg.norm(vector)
    return vector/norm

def rotate_vector(v, theta):
    vx, vy = v[0], v[1]
    return np.array( [np.cos(theta)*vx - np.sin(theta)*vy,
                     np.sin(theta)*vx + np.cos(theta)*vy])

# find subset of e1 that can map to e2 under theta
# returns (pt1, pt2), subset of e1 which is domain of transition
# assumes e1, e2, entirely visible to each other
# returns empty array if domain is empty
def findDomain(e1, e2, theta):
    e1v1, e1v2 = e1
    e2v1, e2v2 = e2
    pt1, pt2 = [], []
    bounce_vector = rotate_vector(e1v2-e1v1, theta)
    f_e1v1 = e1v1 + bounce_vector
    f_e1v2 = e1v2 + bounce_vector

    # if the domain is empty
    if IsRightTurn(e1v2, f_e1v2, e2v2) or IsLeftTurn(e1v1, f_e1v1, e2v1):
        return np.array([pt1, pt2])

    # check left hand side of interval
    if IsRightTurn(e1v1, f_e1v1, e2v2):
        # project back to originating segment
        pt_start = e2v2 + bounce_vector
        _, _, pt1 = ShootRayFromVect(pt_start, e2v2, e1v1, e1v2)
    else:
        pt1 = e1v1

    # check right hand side of interval
    if IsLeftTurn(e1v2, f_e1v2, e2v1):
        pt_start = e2v1 + bounce_vector
        _, _, pt2 = ShootRayFromVect(pt_start, e2v1, e1v1, e1v2)
    else:
        pt2 = e1v2

    return np.array([pt1, pt2])

#def isContraction(s1, s2, theta):
