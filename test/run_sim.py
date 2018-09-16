#! /usr/bin/env python3
import sys
sys.path.append('../src')
from helper.visualization_helper import *
from link_diagram import Link_Diagram

if __name__ == '__main__':
    poly_vx = simple_bit
    poly_name = 'simple_bit'
    pls = Partial_Local_Sequence(poly_vx)
    visualize_all_partial_order_sequence(pls.polygon.vertices, pls.inserted_polygon.vertices, pls.sequence_info)
    visualize_polygon(poly_vx, poly_name)
    link_diagram = Link_Diagram(pls)
    visualize_link_diagram(link_diagram, hline = 1.4707)
    visualize_polygon(pls.inserted_polygon.vertices, 'inserted_'+poly_name)
    pls2 = Partial_Local_Sequence(poly2)
    origin = poly2[10]
    sequence = pls2.sequence_info[10]
    visualize_partial_local_sequence_for_one_vx(poly2, origin, sequence)

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
