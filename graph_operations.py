#!/usr/bin/env python

# graph_operations.py
# applications of the bounce visibility graph to robotic tasks

from graph_utils import *
from copy import copy

# a strategy should be an automata where inputs = sensor obs, and outputs = bounce angles

#def propagateInterval(G, startseg, startint, strategy):

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

def nodeInterval(poly, interval):
    (s1, s2) = interval
    s_verts = [s_inv(p, poly) for p in poly]
    i1 = 0
    i2 = 0
    FOUND_S1 = False
    FOUND_S2 = False
    for i,s in enumerate(s_verts):
        print(i,s)
        if s > s1 and not FOUND_S1:
            i1 = i-1
            FOUND_S1 = True
        if s > s2 and not FOUND_S2:
            i2 = i-1
            FOUND_S2 = True
    return i1, i2



def navigate(poly, S, G):
    P = InsertAllTransitionPts(poly)
    BVD = mkGraph(P)
    # find all paths with fewest bounces, choose the one with the widest ang
    # interval
    ps = findPaths(BVD, nodeContaining(BVD,G), nodeContaining(BVD,S))
    strats = map(getStrategies(BVG, S, "const"), ps)
    best = argmax(strats, getAngInt)

