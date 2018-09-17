#! /usr/bin/env python3
import sys
sys.path.append('../src')
from helper.visualization_helper import *
from bounce_visibility_diagram import Bounce_Visibility_Diagram
from bounce_graph import Bounce_Graph

if __name__ == '__main__':
    poly_vx = simple_bit
    poly_name = 'simple_bit'
    pls = Partial_Local_Sequence(poly_vx)
    bvd = Bounce_Visibility_Diagram(pls)
    bounce_graph = Bounce_Graph(bvd)

    pls2 = Partial_Local_Sequence(poly2)
    origin = poly2[10]
    sequence = pls2.sequence_info[10]
    
    visualize_all_partial_order_sequence(pls.polygon.vertices, pls.inserted_polygon.vertices, pls.sequence_info)
    visualize_polygon(poly_vx, poly_name)
    visualize_bounce_visibility_diagram(bvd, hline = 1.4707)
    visualize_polygon(pls.inserted_polygon.vertices, 'inserted_'+poly_name)
    visualize_partial_local_sequence_for_one_vx(poly2, origin, sequence)
    visualize_graph(bounce_graph.visibility_graph, "bounce_visibility_graph")
    visualize_graph(bounce_graph.safe_action_graph, "bounce_safe_action_graph")
    # start = (0.1,0.15)
    # goal = (0.55, 0.56)
    # path = navigate(poly, start, goal)
    # print(path)
    #intervals = PropagatePath(p1, path, S)
    #VizPath(p1, intervals)
