#!/usr/bin/env python

# bounce.py
# This program simulates the bouncing of balls
# under various bouncing strategies
#
# Written by Steve LaValle
# November 2011

import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2,pi
from time import sleep
from geom_utils import *
from maps import *

#constants
XDIM = 500
YDIM = 500
WINSIZE = [XDIM, YDIM]
EPSILON = 1.0
NUMBOUNCES = 100000
MAXDIST = 10000000.0

# n is the inward edge normal (in radians 0 to pi)
def PerformRotation(incoming, n, strategy):
    # Random bounce
    if strategy == 0:
        dir = n + random.random()*pi - pi/2.0

    # Right angle bounce
    elif strategy == 1:
        dir = incoming + pi/2.0
        if AngleDistance(dir,n) > pi/2.0:
            dir += pi

    # Billiard bounce
    elif strategy == 2:
        rebound = FixAngle(incoming + pi)
#    print "ad:",AngleDifference(rebound,n),"rebound:",rebound,"n:",n
        dir = rebound + 2.0*AngleDifference(rebound,n)

    # Normal bounce
    elif strategy == 3:
        dir = n
    dir = FixAngle(dir)
    if AngleDistance(dir,n) > pi/2.0:
        print("Error: Illegal bounce.  n:",n,"dir:",dir)
        raise ValueError
    return dir

def PerformBounce(s,bp,n,strategy):
    dir = PerformRotation(s[2], n, strategy)
    return (bp[0], bp[1], dir)

def main():
    # Initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Bouncing Strategies    University of Illinois    2018')
    white = 255, 240, 200
    black = 20, 20, 40    
    green = 50, 130, 50
    screen.fill(black)
    pint = (0.0,0.0)

    # This sets the billiard boundary
    poly = bigpoly

    # Set the initial ball state (x,y,theta)
    state = (200.0, 200.0, 2.0)

    last_bounce_edge = -1

    for i in range(NUMBOUNCES):

        psize = len(poly)
        closest_bounce = MAXDIST
        bnormal = -1.0  # The inward edge normal of the bounce point

        pygame.draw.polygon(screen,white,PolyToWindowScale(poly, YDIM),5)
        # check each edge for collision
        for j in range(psize):
            if (j != last_bounce_edge):
                v1, v2 = poly[j], poly[(j+1) % psize]
                x1, y1 = state[0], state[1]
                # The line parameter t; needs divide by zero check!
                t,pt = ShootRay(state, v1, v2)
                
                # Find closest bounce for which t > 0
                pdist = PointDistance(pt,(x1,y1))
                if ((t > 0) and (pdist < closest_bounce) and
                    BouncePointInEdge((x1,y1),pt,v1,v2)):
                    bounce_point = pt
                    closest_bounce = pdist
                    b_edge = j
#                    print "bnormal:",bnormal
#                    print "pdist:",pdist,"closest_bounce:",closest_bounce,"pint:",pint

#            pygame.draw.circle(screen,green,PointToWindowScale(pint),5)
#        raw_input("Press Enter to continue...")

#        print "closest_bounce:",closest_bounce,"bounce_point:",bounce_point
        pygame.draw.line(screen,green,PointToWindowScale(bounce_point, YDIM),\
                         PointToWindowScale((state[0],state[1]), YDIM))
        pygame.display.update()
#        print "state:",state
        sleep(0.1)

# Set the last argument to PerformBounce:
# 0 = random, 1 = right angle, 2 = billiard, 3 = normal
        bnormal = FixAngle(pi/2.0 + 
                           atan2(poly[(b_edge+1)%psize][1]-poly[b_edge][1],\
                                 poly[(b_edge+1)%psize][0]-poly[b_edge][0]))
        state = PerformBounce(state,bounce_point,bnormal,3)
        last_bounce_edge = b_edge

        for e in pygame.event.get():
	        if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
	            sys.exit("Leaving because you requested it.")
    while (1):
        1 == 1

# if python says run, then we should run
if __name__ == '__main__':
    main()


