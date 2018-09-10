#! /usr/bin/env python3

from geom_utils import *
from graph_utils import *
from graph_operations import *
from maps import *
from link_diagram import *
from partial_local_sequence import FindReflexVerts, ShootRaysFromReflex, ShootRaysToReflexFromVerts
from settings import *
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import os.path as osp

def VizRay(poly):
    ''' Draws all transition points in poly and saves to viz_test.pdf
    '''
    # Plot the outer boundary with black color
    plt.figure()
    plt.plot(np.vstack((poly, poly[0])), 'black')

    # mark reflex vertices
    rvs = FindReflexVerts(poly)
    for p in rvs:
        plt.plot(poly, 'bo')
        r_children = ShootRaysFromReflex(poly, p)
        transition_pts = ShootRaysToReflexFromVerts(poly,p)
        transition_pts.extend(r_children)
        for (pt,k) in transition_pts:
            plt.plot(poly, 'green')

    t_pts = InsertAllTransitionPts(poly)
    plt.plot(t_pts, 'ro')
    plt.savefig(osp.join(image_save_folder,'viz_test.pdf'))
    if DEBUG:
        plt.show()

def VizPoly(poly, fname='inserted_poly'):
    ''' Draws polygon with numbered vertices
    '''
    psize = len(poly)
    jet = plt.cm.jet
    colors = jet(np.linspace(0, 1, psize))

    # plot only polygon, no axis or frame
    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    plt.plot(np.vstack((poly, poly[0])), 'black')
    for i in range(psize):
        point = poly[i]
        plt.scatter(point[0], point[1], color=colors[i], s=100)
        plt.annotate(str(i), (point[0]+5, point[1]+20), size = 20)
    plt.axis('equal')

    plt.savefig(osp.join(image_save_folder,fname+'.png'), dpi = 300, bbox_inches='tight')
    if DEBUG:
        plt.show()

# Resolution is the number of sample points on each edge
# hline is for showing fix theta bouncing
# fname is the output file name for the link diagram
def PlotLinkDiagram(poly, link_diagram, resolution = 15, hline = None, fname = 'link_diagram.png'):
    ''' Save the link diagram for a given polygon to image

    Parameters
    ----------
    poly:np.array
        The input polygon represented by its vertex coordinates
    link_diagram:np.array
        The link diagram computed for the given polygon
    Resolution:int
        The number of sample points on each edge
    hline:float
        The angle of fix theta bouncing
    fname:string
        The output file name for the link diagram
    '''
    poly = np.array([list(x) for x in poly])
    edge_len = [norm(poly[i]-poly[(i+1)%len(poly)]) for i in range(len(poly))]
    acc_edge_len = [sum(edge_len[:i]) for i in range(len(edge_len)+1)]
    psize = link_diagram.shape[0]
    jet = plt.cm.jet
    colors = jet(np.linspace(0, 1, psize))
    fig, ax = plt.subplots()
    x = []
    for i in range(psize):
        x.extend(list(np.linspace(acc_edge_len[i], acc_edge_len[i+1], resolution-1)))
        x.extend([acc_edge_len[i+1]])
    for i in range(psize):
        plt.plot(x, link_diagram[i], label= '{}'.format(i), alpha=0.7, color = colors[i])
        plt.axvline(x=acc_edge_len[i], linestyle='--')
    plt.axvline(x = acc_edge_len[-1], linestyle='--')
    if hline != None:
        plt.plot(range(psize+1), hline*np.ones(psize+1))

    leg = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol=5)
    ax.set_xticks(acc_edge_len)
    x_labels = list(range(psize))
    x_labels.append(0)
    ax.set_xticklabels(x_labels)
    ax.set_yticks([0., np.pi/6., np.pi/3., np.pi/2., 2*np.pi/3., 5*np.pi/6., np.pi])
    ax.set_yticklabels(["$0$", r"$\frac{1}{6}\pi$", r"$\frac{1}{3}\pi$", r"$\frac{1}{2}\pi$", r"$\frac{2}{3}\pi$", r"$\frac{5}{6}\pi$", r"$\pi$"])
    plt.xlabel(r"vertices on $\partial P'$", fontsize=15)
    plt.ylabel(r"bounce angle $\theta$", fontsize=15)
    plt.savefig(osp.join(image_save_folder,fname), bbox_inches='tight', dpi = 300)
    if DEBUG:
        plt.show()

def PlotGraph(G, fname = 'graph'):
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
    # nx.draw_networkx_edge_labels(G,new_pos,edge_labels=labels)
    plt.axis('off')
    ax = plt.gca()
    ax.collections[0].set_edgecolor('black') 
    plt.savefig(osp.join(image_save_folder,fname+'.png'), bbox_inches='tight', dpi = 300)

def VizPath(poly, intervals):
    psize = len(poly)
    jet = plt.cm.jet
    colors = jet(np.linspace(0, 1, psize))

    # plot only polygon, no axis or frame
    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    wall_x = [x for (x,y) in poly]
    wall_x.append(wall_x[0])
    wall_y = [y for (x,y) in poly]
    wall_y.append(wall_y[0])
    plt.plot(wall_x, wall_y, 'black')
    for i in range(psize):
        point = poly[i]
        plt.scatter(point[0], point[1], color=colors[i])
        plt.annotate(str(i), (point[0]+10, point[1]+10), size = 'small')
    plt.axis('equal')

    print(intervals)

    interval_ts = list(zip(intervals, intervals[1:]))
    for i in interval_ts:
        print(i)
    p1, p2 = list(interval_ts)[0][0]
    plt.plot([p1[0],p2[0]], [p1[1], p2[1]], 'red',linewidth=5)

    for ((pt1, pt2), (new_pt1, new_pt2)) in interval_ts:
        print('plotting', ((pt1, pt2), (new_pt2, new_pt1)))
        plt.plot([new_pt1[0],new_pt2[0]], [new_pt1[1], new_pt2[1]], 'red',linewidth=5)
        plt.plot([pt1[0],new_pt2[0]], [pt1[1], new_pt2[1]], 'green')
        plt.plot([pt2[0],new_pt1[0]], [pt2[1], new_pt1[1]], 'green')

    plt.savefig(osp.join(image_save_folder,'path.png'), dpi = 300)
    if DEBUG:
        plt.show()
