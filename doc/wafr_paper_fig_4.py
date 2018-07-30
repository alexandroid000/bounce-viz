#! /usr/bin/env python3

from maps import *
from viz_utils import *

if __name__ == '__main__':
    poly = l_poly
    p1 = InsertAllTransitionPts(poly)
    VizPoly(p1)
    link_diagram = GetLinkDiagram(p1)
    PlotLinkDiagram(p1, link_diagram)