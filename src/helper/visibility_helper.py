#!/usr/bin/env python

import visilibity as vis
from copy import copy
from settings import *
# for polygons not in general position: returns all visible vertices along a ray

def get_visible_vertices(poly, j):
    #print('At vertex',j)
    psize = poly.shape[0]

    # Outer boundary polygon must be COUNTER-CLOCK-WISE(ccw)
    # Create the outer boundary polygon
    # Define an epsilon value (should be != 0.0)
    vpoly = list(map(lambda x: vis.Point(x[0], x[1]), poly))
    walls = vis.Polygon(vpoly)
    walls.enforce_standard_form()

    # point from which to calculate visibility
    p1 = poly[j]
    vp1 = vis.Point(*p1)

    # Create environment, wall will be the outer boundary because
    # is the first polygon in the list. The other polygons will be holes
    env = vis.Environment([walls])
    # Necesary to generate the visibility polygon
    vp1.snap_to_boundary_of(env, EPSILON)
    vp1.snap_to_vertices_of(env, EPSILON)
    isovist = vis.Visibility_Polygon(vp1, env, EPSILON)
    vvs = [(isovist[i].x(), isovist[i].y()) for i in range(isovist.n())]
    #print(vvs)
    visibleVertexSet = []
    for i in range(psize):
        p = vis.Point(*poly[i])
        vp = copy(p).projection_onto_boundary_of(isovist)
        if (vis.distance(vp, p) < EPSILON) and i != j:
            visibleVertexSet.append(i)
    if DEBUG:
        print('vertices',visibleVertexSet,'visible from',j)
    return visibleVertexSet

# make all sets of vertices visible from everywhere along edge
def get_all_edge_visible_vertices(poly):
    psize = poly.shape[0]
    all_viz_vxs = [get_visible_vertices(poly, i) for i in range(psize)]
    if DEBUG:
        print('All visible verts:\n{}\n'.format(all_viz_vxs))

    # each element in the map is indexed by its clockwise vertex (smaller index)
    vizSets = []

    # get vertices that are visible to the current vertex and the next vertex
    for i in range(psize):
        viz_vxs = list(set(all_viz_vxs[i]) & set(all_viz_vxs[(i+1)%psize]))
        # if the following line included, allows transition to next edge by wall
        # following, even if reflex angle
        # TODO: figure out if we want to allow this behavior
        viz_vxs.append((i+1)%psize) 
        # vizSets[i] = viz_vxs
        vizSets.append(viz_vxs)

    if DEBUG:
        print('viz sets\n--------\n{}\n'.format(vizSets))
    return vizSets 
