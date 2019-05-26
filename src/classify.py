# classify segments of polygon boundary according to whether they admit
# contraction mappings under a given angle theta

from helper.shoot_ray_helper import ShootRayFromVect
from helper.geometry_helper import IsRightTurn, IsLeftTurn, AngleBetween
from helper.bounce_graph_helper import whichComponent
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
        return np.array([[], []])

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

def classifyBoundary(poly, theta):

    # construct edge-edge visibility graph
    pls = Partial_Local_Sequence(poly)
    poly_prime = pls.inserted_polygon
    bvg = Bounce_Graph(Bounce_Visibility_Diagram(pls))
    viz_edges = bvg.visibility_graph.edges

    vs = poly_prime.complete_vertex_list
    components = poly_prime.vertex_list_per_poly
    outer_boundary = [v for i,v in components[0]]
    n = len(vs)
    class_data = {i:[] for i in range(n)}
    for (v1, v2) in viz_edges:
        c1 = whichComponent(v1, poly_prime)
        c2 = whichComponent(v2, poly_prime)
        e1 = [vs[v1], vs[next_v(v1, poly_prime)]]
        e2 = [vs[v2], vs[next_v(v2, poly_prime)]]

        subset = findDomain(e1, e2, theta)
        admitsTransition = subset.size != 0
        isContract, c = isContraction(e1, e2, theta)
        if admitsTransition and isContract:
            class_data[v1].append([True, subset, c])
        elif admitsTransition:
            class_data[v1].append([False, subset, -1000])
        else:
            pass
    return poly_prime, class_data

# wrapper to correct for sequential numbering across components
def next_v(i, poly):
    n = poly.size

    c1 = whichComponent(i, poly)
    c2 = whichComponent((i+1) % n, poly)

    if c1 != c2:
        return poly.vertex_list_per_poly[c1][0][0]
    else:
        return i+1

def color(c):
    if abs(c) <= 1.:
        return 'b'
    else:
        return 'r'

def plot_poly(vs, data, poly):

    all_vs = poly.complete_vertex_list
    n = len(vs)
    xs = [all_vs[i][0] for i in vs]
    ys = [all_vs[i][1] for i in vs]
    edges = list(zip(vs, vs[1:])) + [(vs[-1], vs[0])]
    for v1, v2 in edges:
        pt1 = all_vs[v1]
        pt2 = all_vs[v2]
        xpair = [pt1[0], pt2[0]]
        ypair = [pt1[1], pt2[1]]
        plt.plot(xpair, ypair, 'ko-')
        if v1 in data:
            dat = data[v1]
            plot_dat = [(subset, color(c)) for val, subset, c in dat]
            for [pt1, pt2], c in plot_dat:
                plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], c+'-')


def test():
    theta = 1.57
    poly = Simple_Polygon("sh", simple_holes[0], simple_holes[1])
    pprime, data = classifyBoundary(poly, theta)

    outer_vs = [i for i,v in pprime.vertex_list_per_poly[0]]
    outer_data = {i:data[i] for i in data.keys() if i in outer_vs}
    plot_poly(outer_vs, outer_data, pprime)

    components = pprime.vertex_list_per_poly[1:]
    for c in components:
        vs = [i for i,v in c]
        vs.reverse()
        c_data = {i:data[i] for i in data.keys() if i in vs}
        plot_poly(vs, c_data, pprime)
    #for i in range(n):
    #    print(data[i])
    plt.savefig("test.png")
    plt.clf



test()

