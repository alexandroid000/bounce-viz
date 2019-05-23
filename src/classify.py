# classify segments of polygon boundary according to whether they admit
# contraction mappings under a given angle theta

from helper.shoot_ray_helper import ShootRayFromVect
from helper.geometry_helper import IsRightTurn, IsLeftTurn, AngleBetween
from simple_polygon import *
from partial_local_sequence import *
from bounce_visibility_diagram import *
from bounce_graph import *
from maps import *
from settings import *

import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


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
    [e1v1, e1v2] = e1
    [e2v1, e2v2] = e2
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

# compute whether transition is contracting and what the coefficient is
def isContraction(e1, e2, theta):
    [e1v1, e1v2] = e1
    [e2v1, e2v2] = e2
    phi = AngleBetween(e1v2-e1v1, e2v2-e2v1) # in range [0,pi]

    try:
        _, _, int_pt = ShootRayFromVect(e1v1, e1v2, e2v1, e2v2)
    except: # lines are parallel, inducing neutrally stable 2-period cycle
        return True, 1.0

    # determine handedness of transition

    # left transition
    if la.norm(e1v1-e2v2) < EPSILON:
        c_th = np.sin(theta)/np.sin(theta-phi)
    # right transition
    elif la.norm(e1v2-e2v1) < EPSILON:
        c_th = np.sin(theta)/np.sin(theta+phi)
    # left transition
    elif IsLeftTurn(e1v1, e2v1, int_pt):
        c_th = np.sin(theta)/np.sin(theta-phi)
    # right transition
    else:
        c_th = np.sin(theta)/np.sin(theta+phi)

    if abs(c_th) < 1.0:
        return True, c_th
    else:
        return False, c_th

# brute force, O(n^2) way. Can be reduced by checking viz info first
# first pass: do not consider holes
def classifyBoundary(poly, theta):
    components = poly.vertex_list_per_poly
    outer_boundary = [v for i,v in components[0]]
    n = len(outer_boundary)
    class_data = {i:[] for i in range(n)}
    for i in range(n):
        e1 = [outer_boundary[i], outer_boundary[(i+1) % n]]
        for j in range(n):
            if j != i:
                e2 = [outer_boundary[j], outer_boundary[(j+1) % n]]
                subset = findDomain(e1, e2, theta)
                admitsTransition = subset.size != 0
                isContract, c = isContraction(e1, e2, theta)
                if admitsTransition and isContract:
                    class_data[i].append([True, subset, c])
                elif admitsTransition:
                    class_data[i].append([False, subset, -1000])
                else:
                    pass
    return class_data

def color(c):
    if abs(c) <= 1.:
        return 'b'
    else:
        return 'r'

def test():
    theta = 1.5
    init_poly = Simple_Polygon("sh", simple_nonconv[0])
    pls = Partial_Local_Sequence(init_poly)
    bvd = Bounce_Visibility_Diagram(pls)
    bvg = Bounce_Graph(bvd)
    poly = pls.inserted_polygon
    data = classifyBoundary(poly, theta)

    vs = poly.vertex_list_per_poly[0]
    n = len(vs)
    #for i in range(n):
    #    print(data[i])
    xs = [pt[0] for i,pt in vs]
    ys = [pt[1] for i,pt in vs]
    for i in range(n):
        xpair = [xs[i], xs[(i+1) % n]]
        ypair = [ys[i], ys[(i+1) % n]]
        plt.plot(xpair, ypair, 'ko-')
    for i in range(n):
        dat = data[i]
        plot_dat = [(subset, color(c)) for val, subset, c in dat]
        for [pt1, pt2], c in plot_dat:
            plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], c+'-')
    plt.savefig("test.png")
    plt.clf



test()

