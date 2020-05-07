#!/usr/bin/env python
# coding: utf-8

# polygon generation processes
# ----------------------------

import sys
sys.path.append('../src')
from environments.generate_random_polygon import *
from helper.visualization_helper import *
from simple_polygon import Simple_Polygon
from partial_local_sequence import Partial_Local_Sequence
from bounce_visibility_diagram import Bounce_Visibility_Diagram
from bounce_graph import Bounce_Graph
from navigation import Navigation

# random tree of convex rooms

def containsUnreachableSegs(poly, safe_bg):

    segs = []

    for seg in safe_bg.nodes():
        in_edges = safe_bg.in_edges(seg)
        if len(in_edges) == 0:
            segs.append(seg)

    return segs


def edgeFrac(poly, edges):
    ''' fraction of the polygon perimeter composed of edges in list
    '''
    map = poly.unit_interval_mapping[0]

    frac = 0.
    for i in edges:
        s = map[i+1] - map[i]
        frac += s
    return frac

fracs = np.zeros(len(range(2, 6)) * len(range(5, 20, 3)))
params = np.zeros((len(range(2, 6)) * len(range(5, 20, 3)),2))

for iteration in range(10):
    print("Iteration",iteration)

    polys = []

    for num_rooms in range(2, 6):
        for rvx in range(5, 20, 3):
            corridors, rooms, tree_map = random_tree(num_rooms)
            hobbit_hole = genTreeEnv(num_rooms, rvx, rooms, corridors, tree_map, Hallway_Type.RANDOM_DIRECTION)
            polys.append((num_rooms, rvx, hobbit_hole))

    for i, (num_rooms, rvx, poly) in enumerate(polys):
        print("polygon",i)
        p = Simple_Polygon("sp",poly)
        poly_vx = p.complete_vertex_list

        # generate visibility discretization and visualize
        pls = Partial_Local_Sequence(p)
        ins_vs = np.array(pls.inserted_polygon.complete_vertex_list)
        #visualize_polygon(ins_vs, "poly"+str(i))
        bvd = Bounce_Visibility_Diagram(pls)

        # compute transition graphs between segments on boundary
        bounce_graph = Bounce_Graph(bvd)
        #visualize_graph(bounce_graph.visibility_graph, "bg"+str(i))
        #visualize_graph(bounce_graph.safe_action_graph, "safe_bg"+str(i))
        unreach_segs = containsUnreachableSegs(p, bounce_graph.safe_action_graph)
        #if unreach_segs != []:
        #    print("Visualizing Unreachable Set")
        #    visualize_subset_polygon(ins_vs, "reachable_boundary"+str(i), unreach_segs)

        frac = edgeFrac(pls.inserted_polygon, unreach_segs)
        fracs[i] += frac
        params[i][0] = num_rooms
        params[i][1] = rvx

        LOG = True
        if LOG:
            with open("hobbit_hole_results.txt",'a+') as f:
                f.write("Polygon "+str(i)+'\n')
                f.write("num_rooms: "+str(num_rooms)+'\n')
                f.write("num vxs per room: "+str(rvx)+'\n')
                f.write("fraction unreachable: "+str(frac)+'\n')
                f.write('\n')

fracs = fracs/24.
print(fracs)
print(params)

data = fracs.reshape((len(range(2, 6)), len(range(5, 20, 3))))

plt.imshow(data, cmap='hot', interpolation='nearest')
plt.savefig('hobbit_heatmap.png', dpi = 300, bbox_inches='tight')


# - queries:
#     - what percentage of polygons contain parts that are not reachable using
#       safe actions from anywhere except themselves
#     - what is the expected percentage of a polygon (edge count / measure) that
#       is not reachable using safe actions from anywhere
#     - same queries but for "sinks" (edges of polygon with no outgoing safe
# actions)
#     - what percentage of the polygon can reach the sink under safe actions?
