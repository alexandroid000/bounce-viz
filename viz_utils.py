#! /usr/bin/env python

from geom_utils import *
from maps import *

# Used to plot the example
import matplotlib.pyplot as plt


def VizRay():
    poly = poly1
    # Set the title
    wall_x = [x for (x,y) in poly]
    wall_x.append(wall_x[0])
    wall_y = [y for (x,y) in poly]
    wall_y.append(wall_y[0])
    
    # Plot the outer boundary with black color
    plt.plot(wall_x, wall_y, 'black')

    pt1 = (0.0, 0.0)
    pt2 = (150.0, 50.0)

    plt.plot([pt1[0]], [pt1[1]], 'go')
    plt.plot([pt2[0]], [pt2[1]], 'go')

    # mark reflex vertices
    rvs = FindReflexAngles(poly)
    for p in rvs:
        plt.plot([poly[p][0]], [poly[p][1]], 'bo')

    print(rvs)

    int_pt = ClosestPtAlongRay(pt1,pt2,-1,poly)
    print(int_pt)
    plt.plot([pt1[0], int_pt[0]], [pt1[1], int_pt[1]], 'red')
    
    plt.savefig('test.pdf')

if __name__ == '__main__':
    VizRay()
