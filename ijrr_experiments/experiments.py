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
from matplotlib.ticker import StrMethodFormatter
from matplotlib.patches import ConnectionPatch
import matplotlib.patheffects as pe

# random tree of convex rooms

#num_rooms = 15
#corridors, rooms, T = random_tree(num_rooms)
#hobbit_hole = genTreeEnv(num_rooms, rooms, corridors)

# random star polygons (sweep queries over range of irregularity/spikiness)

# - generate initial state:
#     - monte carlo (uniform from boundary)
#     - iterate reachability query over all edges


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

N = 5
iterations = 10

fracs = np.zeros(N**2)
params = np.zeros((N**2,2))
s_cc = np.zeros((N,N))
w_cc = np.zeros((N,N))

extremum_examples = []

for iteration in range(iterations):
    print("Iteration",iteration)

    # generates 25 polygons
    polys = generatePolygonsGrid(N, 0.1, 0.4, 0.1, 0.5)

    for i, ((spike,irr), poly) in enumerate(polys):
        if iteration == 0:
            if i in [0, N-1, N*N-N, N*N-1]:
                extremum_examples.append(poly)

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

        num_c = nx.number_strongly_connected_components(bounce_graph.safe_action_graph)
        num_c_w = nx.number_weakly_connected_components(bounce_graph.safe_action_graph)
        s_cc[i // N][i % N] += num_c
        w_cc[i // N][i % N] += num_c_w
        print("strongly connected components in polygon", i // N, i % N,": ", num_c)
        print("weakly connected components in polygon", i // N, i % N,": ", num_c_w)
        #if unreach_segs != []:
        #    print("Visualizing Unreachable Set")
        #    visualize_subset_polygon(ins_vs, "reachable_boundary"+str(i), unreach_segs)

        frac = edgeFrac(pls.inserted_polygon, unreach_segs)
        fracs[i] += frac
        params[i][0] = spike
        params[i][1] = irr

        LOG = False
        if LOG:
            with open("single_poly_results.txt",'a+') as f:
                f.write("Polygon "+str(i)+'\n')
                f.write("spike: "+str(spike)+'\n')
                f.write("irr: "+str(irr)+'\n')
                f.write("fraction unreachable: "+str(frac)+'\n')
                f.write('\n')

avg_frac = fracs/iterations
avg_s_cc = s_cc/iterations
avg_w_cc = w_cc/iterations

data = avg_frac.reshape((N,N))

spike_vals = params[:N,0]
irr_vals = params[::N,1]
print("x axis:",spike_vals)
print("y axis:",irr_vals)

def plot_poly_example(poly, axA, axB, locationA):


    p1 = list(np.vstack((poly, poly[0])))
    xs, ys = zip(*p1)
    axB.plot(xs,ys, color='black')

    center = np.average(p1, axis=0)

    con = ConnectionPatch(
        xyA = locationA, coordsA = axA.transData,
        xyB = center, coordsB = axB.transData,
        arrowstyle="->", shrinkB=5, mutation_scale=20, lw=2,
        path_effects=[pe.Stroke(linewidth=5, foreground='w'), pe.Normal()])
    axA.add_artist(con)

def reachability_heatmap(data):

    fig1, ax1 = plt.subplots()

    # make reachability fraction heatmap
    heatmap = ax1.pcolor(data)
    plt.colorbar(heatmap)
    ax1.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
    ax1.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ax1.set_xticklabels(spike_vals.round(2), minor=False)
    ax1.set_yticklabels(irr_vals.round(2), minor=False)
    ax1.set_xlabel('Spikiness')
    ax1.set_ylabel('Irregularity')
    ax1.set_title('Average Fraction of Unreachable Polygon Boundary')

    # make inset (outset?) polygon examples
    left, right, bottom, top, width, height = [-0.1, 0.9, -0.1, 0.8, 0.2, 0.2]
    q11, q12, q21, q22 = [(0.5, 0.5), (N-0.5, 0.5), (0.5, N-0.5), (N-0.5, N-0.5)]
    low_s_low_i = fig1.add_axes([left, bottom, width, height])
    high_s_low_i = fig1.add_axes([right, bottom, width, height])
    low_s_high_i = fig1.add_axes([left, top, width, height])
    high_s_high_i = fig1.add_axes([right, top, width, height])
    low_s_low_i.axis('off')
    high_s_low_i.axis('off')
    low_s_high_i.axis('off')
    high_s_high_i.axis('off')

    plot_poly_example(extremum_examples[0], ax1, low_s_low_i, q11)
    plot_poly_example(extremum_examples[1], ax1, high_s_low_i, q12)
    plot_poly_example(extremum_examples[2], ax1, low_s_high_i, q21)
    plot_poly_example(extremum_examples[3], ax1, high_s_high_i, q22)


    plt.savefig('heatmap.png', dpi = 300, bbox_inches='tight')
    plt.clf()

def cc_heatmap(data, title, fname):

    fig2, ax2 = plt.subplots()

    # make connected component heatmap
    heatmap = ax2.pcolor(data)
    plt.colorbar(heatmap)
    ax2.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
    ax2.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
    ax2.set_xticklabels(spike_vals.round(2), minor=False)
    ax2.set_yticklabels(irr_vals.round(2), minor=False)
    ax2.set_xlabel('Spikiness')
    ax2.set_ylabel('Irregularity')
    ax2.set_title(title)

    plt.savefig(fname, dpi = 300, bbox_inches='tight')

cc_heatmap(avg_s_cc, 'Average Number of Strongly Connected Components in Polygons', 'scc_heatmap.png')
cc_heatmap(avg_w_cc, 'Average Number of Weakly Connected Components in Polygons', 'wcc_heatmap.png')


# - queries:
#     - what percentage of polygons contain parts that are not reachable using
#       safe actions from anywhere except themselves
#     - what is the expected percentage of a polygon (edge count / measure) that
#       is not reachable using safe actions from anywhere
#     - same queries but for "sinks" (edges of polygon with no outgoing safe
# actions)
#     - connected components?
