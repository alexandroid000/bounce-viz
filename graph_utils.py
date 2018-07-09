#!/usr/bin/env python

# graph_utils.py
# functions for constructing and querying the bounce visibility graph

from geom_utils import *

# the coefficent of "contraction" for the mapping from edge i to edge j
# |f(x) - f(y)| = |x - y| * sin(theta) / sin (theta-phi)
# -1 < |f(x) - f(y)| < 1 leads to
# theta > phi/2
# theta < -phi/2
# for contraction mapping
def angleBound(poly, i, j):
    n = len(poly)
    v1 = Points2Vect(poly[i], poly[(i+1) % n])
    v2 = Points2Vect(poly[j], poly[(j+1) % n])
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
    overlap_2 = intersect_intervals((pi-phi,pi),(min_a, max_a))

    intervals = []

    if interval_len(overlap_1) > epsilon:
        intervals.append(overlap_1)
    if interval_len(overlap_2) > epsilon:
        intervals.append(overlap_2)

    return intervals

# creates directed edge-to-edge visibility graph
# edge information is angle ranges which create contraction mapping
def mkGraph(poly):
    G = nx.DiGraph()
    r_vs = FindReflexVerts(poly)
    psize = len(poly)

    for start in range(psize):
        edges = [(start,v,validAnglesForContract(poly, start, v))
                for v in GetVisibleVertices(poly, start)
                # don't allow transition to edge "around corner"
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
        if DEBUG:
            print("Raw edges")
            for i,v,a in edges:
                print("Can see ", v, " from ", i, " with angle bound ", a)
        G.add_weighted_edges_from(edges)
    if DEBUG:
        print("Graph data:")
        print(G.edge)
        plt.clf()
        nx.draw_circular(G, with_labels=True)
        plt.savefig("graph.png")
    return G

# includes transient cycles
# complexity O((n+e)(c+1)) if there are c cycles
# takes forever on most polygons - can we do some kind of online filter?
def allCycles(G):
    return nx.simple_cycles(G)

# TODO - filter on previous function
# some limit cycles exist which are compositions of transient cycles.
# How to detect?
# Can we find where the transient cycles put the robot once it "escapes" and
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
        print("Reduced graph H for angle interval [",theta_min,",",theta_max,"]")
        print(H.edge)
    return H

def mkSafeGraph(G, poly):
    psize = len(poly)
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes())
    new_edges = []
    viz_verts = mkVizSets(poly)
    for i in H.nodes():
        outgoing = G.edge[i]
        for e in outgoing:
            e1 = (poly[i], poly[(i+1)%psize])
            e2 = (poly[e], poly[(e+1)%psize])
            e_viz = (e in viz_verts[i]) and ((e+1)%psize in viz_verts[i])
            if SafeAngles(e1,e2) and e_viz:
                new_edges.append((i,e,SafeAngles(e1,e2)))
    H.add_weighted_edges_from(new_edges)
    return H
