''' Functions for constructing and querying the bounce visibility graph
'''
from geom_utils import *
from settings import *
from partial_local_sequence import *

import networkx as nx
import os
import os.path as osp

# return minimum and maximum angles that allow transition from e1 to e2
# from *somewhere* on e1
# only need to check endpoints
def AnglesBetweenSegs(e1, e2):
    (p1,p2) = e1
    (p3,p4) = e2
    if DEBUG:
        print('finding angle between',e1,'and',e2)

    min_ang = GetVector2Angle(p2-p1,p3-p1)
    max_ang = GetVector2Angle(p2-p1,p4-p2)

    return min_ang, max_ang

# return angle range that allows transition from e1 to e2
# from *anywhere* on e1
# or return None if there is no such range
def SafeAngles(e1, e2):
    (p1,p2) = e1
    (p3,p4) = e2
    if p1 == p4:
        theta_l = np.pi
        theta_r = GetVector2Angle(p2-p1, p3-p2)
    elif p2 == p3:
        theta_r = 0.0
        theta_l = GetVector2Angle(p2-p1, p4-p1)
    else:
        theta_l = GetVector2Angle(p2-p1, p4-p1)
        theta_r = GetVector2Angle(p2-p1, p3-p2)
    not_parallel = abs(theta_l - theta_r) > 0.01
    if theta_l > theta_r and not_parallel: # declare lines parallel if within 1 deg
        return (theta_l, theta_r)
    else:
        return None

# the coefficent of 'contraction' for the mapping from edge i to edge j
# |f(x) - f(y)| = |x - y| * sin(theta) / sin (theta-phi)
# -1 < |f(x) - f(y)| < 1 leads to
# theta > phi/2
# theta < -phi/2
# for contraction mapping
def angleBound(poly, i, j):
    n = len(poly)
    v1 = poly[i] - poly[(i+1) % n]
    v2 = poly[j] - poly[(j+1) % n]
    phi = GetVector2Angle(v1, v2)
    return phi/2

# transition from edge i to edge j is a contraction map iff
# |coeff| < 1
def coeff(poly, i, j, theta):
    phi = 2*angleBound(poly, i, j)
    return sin(theta) / sin (theta-phi)

def intersect_intervals(i1, i2):
    (a,b) = i1
    (c,d) = i2
    return (max(a,c), min(b,d))

def interval_len(interval):
    return abs(interval[1]-interval[0])

# returns list of intervals of valid angles (at most two intervals)
# will return empty list if no bounces can create contraction map
# Poly -> Int -> Int -> [(Angle, Angle)]
def validAnglesForContract(poly, i, j):
    epsilon = 0.0001
    n = len(poly)
    phi = angleBound(poly, i, j)
    e1 = (poly[i], poly[(i+1) % n])
    e2 = (poly[j], poly[(j+1) % n])
    min_a, max_a = AnglesBetweenSegs(e1, e2)
    overlap_1 = intersect_intervals((0,phi),(min_a, max_a))
    overlap_2 = intersect_intervals((np.pi-phi,np.pi),(min_a, max_a))

    intervals = []

    if interval_len(overlap_1) > epsilon:
        intervals.append(overlap_1)
    if interval_len(overlap_2) > epsilon:
        intervals.append(overlap_2)

    return intervals

# creates directed edge-to-edge visibility graph
# edge information is angle ranges which create contraction mapping
def mkGraph(poly, requireContract = False):
    G = nx.DiGraph()
    r_vs = FindReflexVerts(poly)
    psize = len(poly)

    for start in range(psize):
        edges = [(start,v,validAnglesForContract(poly, start, v))
                for v in GetVisibleVertices(poly, start)
                # don't allow transition to edge 'around corner'
                # don't allow zero-measure transition from one endpoint
                # TODO: clean up logic
                if not (
                       ((v in r_vs) and (v == (start+1) % psize))
                       or
                       ((start in r_vs) and (start == (v+1) % psize))
                       or
                       ((v in r_vs) and IsThreePointsOnLine(poly[start], poly[v],
                                                            poly[(v+1)%psize])
                                    and start != ((v+1) % psize))
                       or 
                       ((start in r_vs) and IsThreePointsOnLine(poly[start],
                       poly[v], poly[(start+1)%psize])
                                    and v != (start+1) % psize)
                        )
               ]
        if requireContract:
            c_edges = [(i,j, angs) for (i,j,angs) in edges if angs != []]
            G.add_weighted_edges_from(c_edges)
        else:
            G.add_weighted_edges_from(edges)
    if DEBUG:
        print('Graph data:')
        #print(G.edge)
        plt.clf()
        nx.draw_circular(G, with_labels=True)
        plt.savefig(ops.join(image_save_folder, 'graph.png'))
    return G

# includes transient cycles
# complexity O((n+e)(c+1)) if there are c cycles
# takes forever on most polygons - can we do some kind of online filter?
def allCycles(G):
    return nx.simple_cycles(G)

# TODO - filter on previous function
# some limit cycles exist which are compositions of transient cycles.
# How to detect?
# Can we find where the transient cycles put the robot once it 'escapes' and
# then look for cycles in that graph?
# Maybe we can start by find all cycles of length up to some bound and
# exhaustively search.
# def allLimitCycles

# find all shortest paths (from start segment to end segment)
def findPaths(G, start, goal):
    return nx.all_shortest_paths(G, source=start, target=goal)

# return G given a range of bounce angles smaller than 0 to pi
def reduceGraphWrtAngle(G, theta_min, theta_max):
    epsilon = 0.0001
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes())
    new_edges = []
    for i in H.nodes():
        outgoing = G.edge[i]
        for e in outgoing:
            angle_intervals = outgoing[e]['weight']
            ang_info = []
            for a_range in angle_intervals:
                overlap = intersect_intervals(a_range, (theta_min, theta_max))
                if overlap[1] - overlap[0] > epsilon:
                    ang_info.append(overlap)
            if len(ang_info) > 0:
                new_edges.append((i,e,ang_info))
    H.add_weighted_edges_from(new_edges)
    if DEBUG:
        print('Reduced graph H for angle interval [',theta_min,',',theta_max,']')
        print(H.edge)
    return H

def mkSafeGraph(G, poly):
    psize = len(poly)
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes())
    new_edges = []
    viz_verts = mkVizSets(poly)
    for i in H.nodes():
        outgoing = G.edges([i])
        vset = viz_verts[i]+[i]
        for e in outgoing:
            e = e[1]
            e1 = (poly[i], poly[(i+1)%psize])
            e2 = (poly[e], poly[(e+1)%psize])
            e_viz = (e in vset) and ((e+1)%psize in vset)
            if SafeAngles(e1,e2) and e_viz:
                curr_weight = '{0:.2f}'.format(SafeAngles(e1,e2)[1])
                new_edges.append((i,e,curr_weight))
    H.add_weighted_edges_from(new_edges)
    if DEBUG:
        print('Safe graph data:')
        for i in range(psize):
            print('Node',i)
            print(H.edge[i])
    return H
