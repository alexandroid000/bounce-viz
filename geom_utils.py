#!/usr/bin/env python

# geom_utils.py
# util functions for geometry in simple polygons

import random, math
from math import sqrt,cos,sin,atan2,pi
import numpy as np
import matplotlib.pyplot as plt

def PolyToWindowScale(poly, ydim):
    newpoly = []
    for p in poly:
        newpoly.append((p[0]/2.0, ydim - p[1]/2.0))
    return newpoly

def PointToWindowScale(p, ydim):
     return (p[0]/2.0, ydim - p[1]/2.0)

# Do we have theta1 <= theta <= theta2 (mod 2pi) ?
# It is just a particular cyclic permutation
def AngleBetween(theta,theta1,theta2):
    return (((theta1 <= theta) and (theta <= theta2)) or \
            ((theta2 <= theta1) and (theta1 <= theta)) or \
            ((theta <= theta2) and (theta2 <= theta1)))

def AngleDistance(theta1,theta2):
    d = abs(theta1-theta2)
    return min(d,2.0*pi-d)

def AngleDifference(theta1,theta2):
    d = theta2 - theta1
    if (d < pi):
        d += 2.0*pi;
    if (d > pi):
        d -= 2.0*pi;
    return d

def PointDistance(p,q):
    return sqrt((p[0]-q[0])*(p[0]-q[0])+(p[1]-q[1])*(p[1]-q[1]))

def GetVectorLen(v):
    return math.sqrt(sum((a*b) for a, b in zip(v, v)))

def GetVector2Angle(v1, v2):
    dot_prod = v1[0]*v2[0]+v1[1]*v2[1]
    ratio = max(min(dot_prod/(GetVectorLen(v1)*GetVectorLen(v2)), 1), -1)
    return np.arccos(ratio)

def FixAngle(theta):
    return theta % (2.0*pi)

# r is left of the vector formed by p->q
def IsLeftTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) > 0

# r is right of the vector formed by p->q
def IsRightTurn(p,q,r):
    return q[0]*r[1] + p[0]*q[1] + r[0]*p[1] - \
           (q[0]*p[1] + r[0]*q[1] + p[0]*r[1]) < 0

def IsIntersectSegments(p1, p2, q1, q2):
    return (IsLeftTurn(p1, p2, q1) != IsLeftTurn(p1, p2, q2)) and (IsLeftTurn(q1, q2, p1) != IsLeftTurn(q1, q2, p2))



# checks if vector sp->bp points within edge p1p2
# start point, boundary point, edge p1, edge p2
def BouncePointInEdge(sp,bp,ep1,ep2):
    return ((IsLeftTurn(sp,bp,ep2) and
             IsRightTurn(sp,bp,ep1)) or
            (IsRightTurn(sp,bp,ep2) and
             IsLeftTurn(sp,bp,ep1)))

# find line intersection parameter of edge (v1,v2)
# state :: (x,y,theta) initial point and angle of ray
def ShootRay(state, v1, v2):
    x1 = state[0]
    y1 = state[1]
    theta = state[2]
    x2 = v1[0]
    y2 = v1[1]
    x3 = v2[0]
    y3 = v2[1]
    a = y3 - y2
    b = x2 - x3
    c = y2*(x3-x2) - x2*(y3-y2)
    den = (a*cos(theta)+b*sin(theta))
    # case when lines are parallel
    # TODO: raise error
    if abs(den) < 0.000001:
        return -10000, (0,0)
    t = (-c - b*y1 - a*x1)/den
    pint = (x1 + cos(theta)*t, y1 + sin(theta)*t)
    return t, pint

# test if point p is in poly using crossing number
def IsInPoly(p, poly):
    intersects = 0
    theta = random.random()*2*pi
    state=(p[0],p[1],theta)
    psize = len(poly)
    for j in range(psize):
        v1, v2 = poly[j], poly[(j+1) % psize]
        t, pt = ShootRay(state, v1, v2)
        if t>0 and BouncePointInEdge(p, pt, v1, v2):
            intersects += 1
    return not (intersects%2 == 0)

# shoot a ray starting at p1, along vector p1->p2
# find intersection with edge v1,v2
# will return first intersection *after* p2
def ShootRayFromVect(p1, p2, v1, v2):
    (x1,y1), (x2,y2) = p1, p2
    (x,y) = (x2-x1, y2-y1) # recenter points so p1 is at origin
    theta = FixAngle(math.atan2(y,x))
    state = (p2[0], p2[1], theta)
    return ShootRay(state, v1, v2)


# shoot ray from p1 toward p2 in poly, return closest intersect point
# will not return point on "last_bounce_edge"
def ClosestPtAlongRay(p1,p2,poly,last_bounce_edge=-1):
    psize = len(poly)
    closest_bounce = 100000000000
    bounce_point = (0.0, 0.0)
    found_coll = False
    bounce_edge = last_bounce_edge

    # check each edge for collision
    for j in range(psize):
        if (j != last_bounce_edge):
            v1, v2 = poly[j], poly[(j+1) % psize]
            x1, y1 = p2[0], p2[1]
            # The line parameter t; needs divide by zero check!
            t,pt = ShootRayFromVect(p1, p2, v1, v2)
            
            # Find closest bounce for which t > 0
            pdist = PointDistance(pt,p2)
            if ((t > 0) and (pdist < closest_bounce) and
                BouncePointInEdge((x1,y1),pt,v1,v2)):
                found_coll = True
                bounce_point = pt
                closest_bounce = pdist
                bounce_edge = j
                #bounce_param = t
                #b_edge = j
    if found_coll:
        return bounce_point, bounce_edge
    else:
        return False

def FindReflexVerts(poly):
    psize = len(poly)
    reflex_verts = []

    for j in range(psize):
        v1, v2, v3 = poly[(j-1) % psize], poly[j], poly[(j+1) % psize]
        if IsRightTurn(v1,v2,v3):
            reflex_verts.append(j)

    return reflex_verts

# shoot two rays from each reflex vertex, along incident edges
# group by edge so we can insert them in correct order
def ShootRaysFromReflex(poly, j):
    psize = len(poly)
    p2 = poly[j]
    p1_ccw = poly[(j+1) % psize]
    p1_cw = poly[(j-1) % psize]

    # do not check False return case - should always succeed lol
    int_1, k = ClosestPtAlongRay(p1_ccw,p2,poly,j)
    int_2, l = ClosestPtAlongRay(p1_cw,p2,poly,((j-1) % psize))

    return (int_1, k), (int_2, l)

# shoot ray from visible vertices through reflex verts
# Poly -> Int -> [(Point, Int)]
def ShootRaysToReflexFromVerts(poly, j):
    psize = len(poly)
    r_v = poly[j]
    pts = []
    visible_verts = GetVisibleVertices(poly,j)

    for v in visible_verts[1:-1]:
        res = ClosestPtAlongRay(poly[v], r_v, poly)
        if res:
            pt, k = res
            if IsInPoly(((pt[0]+r_v[0])/2, (pt[1]+r_v[1])/2), poly):
                pts.append((pt,k))
    return pts

def IsThreePointsOnLine(p1, p2, p3):
    degeneracy_error = 0.00001
    cross_prod = (p1[1] - p2[1]) * (p3[0] - p2[0]) - (p1[0] - p2[0]) * (p3[1] - p2[1])
    return abs(cross_prod)<degeneracy_error

def IsThreePointsOnLineSeg(p1, p2, p3):
    if IsThreePointsOnLine(p1, p2, p3):
        v1 = (p1[0]-p3[0], p1[1]-p3[1])
        v2 = (p2[0]-p3[0], p2[1]-p3[1])
        return (v1[0]*v2[0]+v1[1]*v2[1])<0
    return False

def IsBoundaryIntersect(p1, p2, q1, q2):
    return (IsThreePointsOnLine(p1, p2, q1) or
           IsThreePointsOnLine(p1, p2, q2) or
           IsThreePointsOnLine(q1, q2, p1) or
           IsThreePointsOnLine(q1, q2, p2))

def GetVisibleVertices(poly, j):
    psize = len(poly)
    p1 = poly[j]
    visibleVertexSet = [(j+1)%psize]
    for i in range(psize):
        is_visible = True
        if i == j or i == (j-1)%psize or i == (j+1)%psize:
            continue
        p2 = poly[i]
        for k in range(psize-1):
            if k == i or k == (i-1)%psize or k == j or k == (j-1)%psize:
                continue
            q1, q2 = poly[k], poly[k+1]
            if IsIntersectSegments(p1, p2, q1, q2):
                if IsBoundaryIntersect(p1, p2, q1, q2):
                    continue
                else:
                    is_visible = False
                    break
        # add the check for degeneracy
        other_vxs = list(range(psize))
        other_vxs.remove(i)
        other_vxs.remove(j)
        if is_visible and (IsInPoly(((p1[0]+p2[0])/2, (p1[1]+p2[1])/2), poly) or any([IsThreePointsOnLine(p1, p2, poly[l]) for l in other_vxs])):
            visibleVertexSet.append(i)
    visibleVertexSet.append((j-1)%psize)
    return visibleVertexSet

def SortByDistance(p1, unsorted_vs):
    return sorted(unsorted_vs, key = lambda v: PointDistance(v,p1))

# find all induced transition points, sort and insert into polygon
# probably the most naive way to do this
# return a list of edge indicators for each vertex
def InsertAllTransitionPts(poly):
    t_pts_grouped = {i:[] for i in range(len(poly))}
    rvs = FindReflexVerts(poly)
    # find all transition points, group by edge
    for p in rvs:
        t_pts = []
        r1, r2 = ShootRaysFromReflex(poly, p)
        t_pts.extend([r1,r2])
        t_pts.extend(ShootRaysToReflexFromVerts(poly,p))
        for (pt,i) in t_pts:
            t_pts_grouped[i].append(pt)

    # sort transition points along edge
    for i in range(len(poly)):
        t_pts_grouped[i] = SortByDistance(poly[i], t_pts_grouped[i])

    # insert into polygon
    new_poly = []
    degeneracy_indicator = []
    for i in range(len(poly)):
        new_poly.append(poly[i])
        new_poly.extend(t_pts_grouped[i])
        degeneracy_indicator.append(-1)
        degeneracy_indicator.extend([i for x in range(len(t_pts_grouped[i]))])

    return new_poly, degeneracy_indicator

def getAngleFromThreePoint(p1, p2, origin):
    v1 = (p1[0]-origin[0], p1[1]-origin[1])
    v2 = (p2[0]-origin[0], p2[1]-origin[1])
    return GetVector2Angle(v1, v2)

def getLinkDiagram(poly):
    t_pts, degeneracy_indicator = InsertAllTransitionPts(poly)
    psize = len(t_pts)
    # store the seperating line segments in the link diagram into this array. The 3*psize is for ploting discontinuous lines.
    link_diagram = np.nan*np.ones((psize, 3*psize))
    all_viz_vxs = [GetVisibleVertices(t_pts, i) for i in range(psize)]
    for i in range(psize):
        # filter out the vertices on the next adjacent edge of this vertex since they will all have angle zero
        viz_vxs = []
        for index in all_viz_vxs[i]:
            if degeneracy_indicator[index] != i and index in all_viz_vxs[(i+1)%psize]:
                viz_vxs.append(index)
        viz_vxs.append((i+1)%psize)
        # for each visible vertex, we need to calculate (1) the view angle at the current vertex w.r.t the current edge and (2) the view angle at the next vertex w.r.t the current edge. we also need to (3) insert a np.nan for discontinuity otherwise matplotlib will try to connect them together
        for vx in viz_vxs:
            curr_p = t_pts[i]
            next_p = t_pts[(i+1)%psize]
            # this is the point on the same line of the current edge but in front of the next vertex. Use this so that we don't get zero length vector from the next vertex perspective
            extended_point = (curr_p[0]+2*(next_p[0]-curr_p[0]), curr_p[1]+2*(next_p[1]-curr_p[1]))
            interest_p = t_pts[vx]
            # (1)
            link_diagram[vx][3*i] = getAngleFromThreePoint(next_p, interest_p, curr_p)
            # (2)
            # the if case is for when we are considering the "next vertex"
            if interest_p == next_p:
                link_diagram[vx][3*i+1] = link_diagram[vx][3*i]
            else:
                link_diagram[vx][3*i+1] = getAngleFromThreePoint(interest_p, extended_point, next_p)
            # (3)
            link_diagram[vx][3*i+2] = np.nan
    # plotting the link diagram
    plt.figure()
    for i in range(psize):
        cut_range = link_diagram[i]
        for j in range(psize):
            if cut_range[j] == -1:
                cut_range[j] = np.nan
        x = []
        for j in range(psize):
            x.extend([j, j+1, j+1])
        plt.plot(x, cut_range, label= '{}'.format(i))
        plt.axvline(x=i, linestyle='--')
    leg = plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
    vxs_color = list(range(psize))
    for line in leg.get_lines():
        vxs_color[int(line.get_label())] = '{}'.format(line.get_color())
    plt.savefig('link_diagram.png', bbox_inches="tight")
    plt.show()
    # Color the vertex of the new poly with the colors selected by matplotlib for the lines 
    plt.figure()
    wall_x = [x for (x,y) in t_pts]
    wall_x.append(wall_x[0])
    wall_y = [y for (x,y) in t_pts]
    wall_y.append(wall_y[0])
    plt.plot(wall_x, wall_y, 'black')
    for i in range(psize):
        point = t_pts[i]
        color = vxs_color[i]
        plt.scatter(point[0], point[1], color=color)
        plt.annotate(str(i), (point[0]+10, point[1]+10))
    plt.axis('equal')
    plt.savefig('inserted_poly.png')
    plt.show()

