#! /usr/bin/env python

from geom_utils import *
from maps import *
import numpy as np

# Used to plot the example
import matplotlib.pyplot as plt

def VizRay(poly):
    # Set the title
    wall_x = [x for (x,y) in poly]
    wall_x.append(wall_x[0])
    wall_y = [y for (x,y) in poly]
    wall_y.append(wall_y[0])
    
    # Plot the outer boundary with black color
    plt.figure()
    plt.plot(wall_x, wall_y, 'black')

    # mark reflex vertices
    rvs = FindReflexVerts(poly)
    for p in rvs:
        plt.plot([poly[p][0]], [poly[p][1]], 'bo')
        r1, r2 = ShootRaysFromReflex(poly, p)
        transition_pts = ShootRaysToReflexFromVerts(poly,p)
        transition_pts.extend([r1,r2])
        for (pt,k) in transition_pts:
            plt.plot([poly[p][0], pt[0]], [poly[p][1], pt[1]], 'green')

    t_pts = InsertAllTransitionPts(poly)
    t_x = [x for (x,y) in t_pts]
    t_y = [y for (x,y) in t_pts]
    plt.plot(t_x, t_y, 'ro')
    plt.show()

    #plt.savefig('test.pdf')

def VizInsertedPoly(poly):
    t_pts = InsertAllTransitionPts(poly)
    psize = len(t_pts)
    jet = plt.cm.jet
    colors = jet(np.linspace(0, 1, psize))
    plt.figure()
    wall_x = [x for (x,y) in t_pts]
    wall_x.append(wall_x[0])
    wall_y = [y for (x,y) in t_pts]
    wall_y.append(wall_y[0])
    plt.plot(wall_x, wall_y, 'black')
    for i in range(psize):
        point = t_pts[i]
        plt.scatter(point[0], point[1], color=colors[i])
        plt.annotate(str(i), (point[0]+10, point[1]+10))
    plt.axis('equal')
    plt.savefig('inserted_poly.png', dpi = 300)
    plt.show()

if __name__ == '__main__':
    # VizRay(simple_bit)
    link_diagram = GetLinkDiagram(concave_pent)
    PlotLinkDiagram(link_diagram, hline = 1.4707)
    VizInsertedPoly(concave_pent)
