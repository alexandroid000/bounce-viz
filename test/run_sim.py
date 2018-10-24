#! /usr/bin/env python3
import sys
sys.path.append('../src')
from helper.visualization_helper import *
from bounce_visibility_diagram import Bounce_Visibility_Diagram
from bounce_graph import Bounce_Graph
from navigation import FewestBouncesStrategy, ConstantStrategy

if __name__ == '__main__':
    poly = simple_bit
    poly_vx = poly.vertices
    poly_name = 'simple_bit'
    pls = Partial_Local_Sequence(poly)
    bvd = Bounce_Visibility_Diagram(pls)
    bounce_graph = Bounce_Graph(bvd)

    pls2 = Partial_Local_Sequence(poly2)
    origin = poly2.vertices[10]
    sequence = pls2.sequence_info[10]


    start = (0.51, 0.66)
    goal = (0.85, 0.9)
    nav_task = FewestBouncesStrategy(start, goal, bounce_graph)
    path = nav_task.navigate()

    strat = ConstantStrategy(start, goal, bounce_graph)
    print("Reachable states with constant strat from",strat.start)
    r = strat.reachable_with_constant_strat()
    print(r)
    all_nodes = set(range(strat.sbvg.number_of_nodes()))
    print("Unreachable from",strat.start,"with constant strategy:")
    print(all_nodes.difference(r))
    print("Navigating from",start,"to",goal)
    status, frontier = strat.navigate()
    print("Searching SBVG from",strat.start,"to",strat.end)

    if status:
        print("Found constant strategy!")
        for (s,f) in zip(strat.start, frontier):
            print("bounce at",f,"from",s)
    else:
       print("Could not find constant strategy")
       print("Final frontier:")
       for f in frontier:
           print(f)


    visualize_all_partial_order_sequence(pls.polygon.vertices, pls.inserted_polygon.vertices, pls.sequence_info)
    visualize_polygon(poly_vx, poly_name)
    visualize_bounce_visibility_diagram(bvd, hline = 1.4707)
    visualize_polygon(pls.inserted_polygon.vertices, 'inserted_'+poly_name)
    visualize_partial_local_sequence_for_one_vx(poly2.vertices, origin, sequence)
    visualize_graph(bounce_graph.visibility_graph, "bounce_visibility_graph")
    visualize_graph(bounce_graph.safe_action_graph, "bounce_safe_action_graph")
    # intervals = PropagatePath(pls.inserted_polygon.vertices, path, start)
    # VizPath(p1, intervals)
