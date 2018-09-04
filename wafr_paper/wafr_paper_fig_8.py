#! /usr/bin/env python3

from maps import *
from visualization_helper import *

if __name__ == '__main__':
    poly = simple_bit
    p1 = InsertAllTransitionPts(poly)
    VizPoly(p1)
    G = mkGraph(p1, requireContract = False)
    H = mkSafeGraph(G, p1)
    PlotGraph(H, "safe_graph")