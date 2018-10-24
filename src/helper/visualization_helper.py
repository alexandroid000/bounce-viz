from helper.geometry_helper import *
from maps import *
from partial_local_sequence import ShootRaysFromReflex, ShootRaysToReflexFromVerts
from settings import *
from partial_local_sequence import Partial_Local_Sequence


import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os.path as osp
import networkx as nx

def visualize_all_partial_order_sequence(poly_vx, inserted_poly_vx, sequence_info):
    ''' Draws all transition points in poly and saves to viz_test.pdf
    '''
    # Plot the outer boundary with black color
    plt.figure()
    wall = np.vstack((poly_vx, poly_vx[0]))
    ax = plt.gca()
    ax.axis('off')
    plt.plot(wall[:, 0], wall[:, 1], 'black')
    plt.plot(inserted_poly_vx[:, 0], inserted_poly_vx[:, 1], 'ro')
    for index, seq in enumerate(sequence_info):
        for (pt,k, _) in seq:
            plt.plot([poly_vx[index][0], pt[0]], [poly_vx[index][1], pt[1]], 'green')
    plt.savefig(osp.join(image_save_folder,'viz_test.pdf'))
    if DEBUG:
        plt.show()

def visualize_partial_local_sequence_for_one_vx(poly_vx, origin, sequence, fname = 'partial_local_sequence'):
    ''' Draw the partial local sequence for a given vertex
    '''
    plt.figure()
    ax = plt.gca()
    ax.axis('off')
    wall = np.vstack((poly_vx, poly_vx[0]))
    plt.plot(wall[:, 0], wall[:, 1], 'black')
    psize = poly_vx.shape[0]
    for i, pt in enumerate(poly_vx):
        plt.plot(pt[0], pt[1], 'ko', markersize = 5)
        plt.annotate("{}".format(i), xy = (pt[0], pt[1]+7), size =8, color = 'red')

    for (pt,k, v) in sequence:
        plt.plot([origin[0], pt[0]], [origin[1], pt[1]], 'b--',  markersize = 4)
        plt.plot(pt[0], pt[1], 'bo', markersize = 5)
        plt.annotate("{}'".format(v), xy = (pt[0]-8, pt[1]-20),  size =8, color = 'red')

    plt.plot(origin[0], origin[1], 'bo', markersize = 5)
    plt.savefig(osp.join(image_save_folder, fname+'.png'), dpi = 300)
    if DEBUG:
        plt.show()

def visualize_graph(G, fname = 'graph'):
    ''' Draw graph in circular shape
    '''
    plt.clf()
    pos = nx.circular_layout(G)
    labels = nx.get_edge_attributes(G,'weight')
    new_pos = dict()
    count = 0
    for i in pos:
        new_pos[count] = pos[i]
        count += 1
    nx.draw_networkx(G, with_labels=True,
        pos = new_pos,
        node_color='white',
        width=1.2,
        node_size = 600, 
        font_size=14)
    plt.axis('off')
    ax = plt.gca()
    ax.collections[0].set_edgecolor('black') 
    plt.savefig(osp.join(image_save_folder,fname+'.png'), bbox_inches='tight', dpi = 300)

# def VizPath(poly, intervals):
#     psize = len(poly)
#     jet = plt.cm.jet
#     colors = jet(np.linspace(0, 1, psize))

#     # plot only polygon, no axis or frame
#     fig = plt.figure(frameon=False)
#     ax = fig.add_axes([0, 0, 1, 1])
#     ax.axis('off')

#     wall_x = [x for (x,y) in poly]
#     wall_x.append(wall_x[0])
#     wall_y = [y for (x,y) in poly]
#     wall_y.append(wall_y[0])
#     plt.plot(wall_x, wall_y, 'black')
#     for i in range(psize):
#         point = poly[i]
#         plt.scatter(point[0], point[1], color=colors[i])
#         plt.annotate(str(i), (point[0]+10, point[1]+10), size = 'small')
#     plt.axis('equal')

#     print(intervals)

#     interval_ts = list(zip(intervals, intervals[1:]))
#     for i in interval_ts:
#         print(i)
#     p1, p2 = list(interval_ts)[0][0]
#     plt.plot([p1[0],p2[0]], [p1[1], p2[1]], 'red',linewidth=5)

#     for ((pt1, pt2), (new_pt1, new_pt2)) in interval_ts:
#         print('plotting', ((pt1, pt2), (new_pt2, new_pt1)))
#         plt.plot([new_pt1[0],new_pt2[0]], [new_pt1[1], new_pt2[1]], 'red',linewidth=5)
#         plt.plot([pt1[0],new_pt2[0]], [pt1[1], new_pt2[1]], 'green')
#         plt.plot([pt2[0],new_pt1[0]], [pt2[1], new_pt1[1]], 'green')

#     plt.savefig(osp.join(image_save_folder,'path.png'), dpi = 300)
#     if DEBUG:
#         plt.show()
