#! /usr/bin/env python

from geom_utils import *
from maps import *

# Used to plot the example
import matplotlib.pyplot as plt


def VizRay():
    poly = poly1
    poly.append(poly[0])
    # Set the title
    wall_x = [x for (x,y) in poly]
    wall_y = [y for (x,y) in poly]
    
    # Plot the outer boundary with black color
    plt.plot(wall_x, wall_y, 'black')

    plt.savefig('test.pdf')

if __name__ == '__main__':
    VizRay()
