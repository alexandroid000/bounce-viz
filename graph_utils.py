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

def coeff(poly, i, j, theta):
    phi = 2*angleBound(poly, i, j)
    return sin(theta) / sin (theta-phi)

def mkGraph(poly):
    G = nx.DiGraph()

    t_pts = InsertAllTransitionPts(poly)
    r_vs = FindReflexVerts(poly)
    psize = len(t_pts)

    for start in range(psize):
        edges = [(start,v,angleBound(t_pts, start, v))
                for v in GetVisibleVertices(t_pts, start)
                # don't allow transition to edge "around corner"
                # don't allow zero-measure transition from one endpoint
                # TODO: clean up logic
                if not (
                       ((v in r_vs) and (v == (start+1) % psize))
                       or
                       ((start in r_vs) and (start == (v+1) % psize))
                       or
                       ((v in r_vs) and IsThreePointsOnLine(t_pts[start], t_pts[v],
                                                            t_pts[(v+1)%psize])
                                    and start != ((v+1) % psize))
                       or 
                       ((start in r_vs) and IsThreePointsOnLine(t_pts[start], t_pts[v],
                                                            t_pts[(start+1)%psize])
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
        print(G.nodes())
        print(G.edges())
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
    H = nx.DiGraph()
    H.add_nodes_from(G.nodes())
    for i in H.nodes():
        outgoing = G.edge[i]
        for e in outgoing:
            phi = outgoing[e]['weight']
            if (theta_min < phi) or (theta_max > pi-phi):
                H.add_edge(i,e)
    return H



