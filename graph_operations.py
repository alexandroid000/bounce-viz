#!/usr/bin/env python

# graph_operations.py
# applications of the bounce visibility graph to robotic tasks

from graph_utils import *
from copy import copy
from maps import *

# a strategy should be an automata where inputs = sensor obs, and outputs = bounce angles

def interp(p1, p2, s):
    (x1,y1) = p1
    (x2,y2) = p2
    x_new = (1-s)*x1 + s*x2
    y_new = (1-s)*y1 + s*y2
    return (x_new, y_new)

def polyLens(poly):
    p = copy(poly)
    p.append(poly[0])
    edge_lens = [PointDistance(p1,p2) for (p1, p2) in zip(p, p[1:])]
    perim_len = sum(edge_lens)
    return edge_lens, perim_len

# [0,1) -> dP
def s(s_param, poly):
    psize = len(poly)
    edge_lens, perim_len = polyLens(poly)
    s_len = s_param*perim_len

    for i in range(psize):
        if s_len - edge_lens[i] < 0.0:
            s_edge = s_len/edge_lens[i]
            if DEBUG:
                print("param", s_edge, "on edge", poly[i], poly[(i+1)%psize])
            return interp(poly[i],poly[(i+1)%psize],s_edge)
        else:
            s_len = s_len - edge_lens[i]

# dp -> [0,1)
# assumes point is on boundary
def s_inv(pt, poly):
    psize = len(poly)
    edge_lens, perim_len = polyLens(poly)
    edge = 0
    s_edge = 0.0
    for i in range(psize):
        p1,p2 = poly[i], poly[(i+1)%psize]
        if IsThreePointsOnLineSeg(p1,p2,pt) or p1==pt:
            edge = i
            s = sum(edge_lens[:i])/perim_len
            s += PointDistance(p1, pt)/perim_len
            return s

# this needs an algebra
def nodesCovered(poly, interval):
    psize = len(poly)
    (s1, s2) = interval
    s_dist = (s2-s1)%1
    s_verts = [s_inv(p, poly) for p in poly]
    s_verts.extend([s+1.0 for s in s_verts])
    nodes = []
    for i,s in enumerate(s_verts[:-1]):
        if s_verts[i+1] > s1 and (s1+s_dist) > s:
            nodes.append(i%psize)
    return nodes

def navigate(poly, S, G):
    P = InsertAllTransitionPts(poly)
    BVD = mkGraph(P)
    # find all paths with fewest bounces
    # choose the one with the widest ang interval
    paths = []
    for g in nodesCovered(poly, G):
        for s in nodesCovered(poly, S):
            print(g,s)
            paths.append(findPaths(BVD, g, s))
    #strategy = getStrategies(BVG, S, "const", path)

if __name__ == '__main__':
    navigate(square, (0.1,0.2), (0.8,0.9))
