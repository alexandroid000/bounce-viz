#! /usr/bin/env python3
import sys
sys.path.append('../src')
from helper.visualization_helper import *

if __name__ == '__main__':
    poly = simple_bit
    VizRay(poly)
    VizPoly(poly)
    p1 = InsertAllTransitionPts(poly)
    link_diagram = GetLinkDiagram(p1)
    PlotLinkDiagram(p1, link_diagram, hline = 1.4707)
    print("inserted all transition pts")
    VizPoly(p1)
    
    # G = mkGraph(p1, requireContract = False)
    # print("made graph")
    # PlotGraph(G)
    # H = mkSafeGraph(G, p1)
    # PlotGraph(H, "safe_graph")
    # start = (0.1,0.15)
    # goal = (0.55, 0.56)
    # path = navigate(poly, start, goal)
    # print(path)
    #intervals = PropagatePath(p1, path, S)
    #VizPath(p1, intervals)
