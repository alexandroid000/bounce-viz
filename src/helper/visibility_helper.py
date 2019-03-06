#!/usr/bin/env python

import visilibity as vis
from copy import copy
from settings import *
from helper.shoot_ray_helper import *
# for polygons not in general position: returns all visible vertices along a ray

def visibleVertices(poly, j):
    #print('At vertex',j)
    vs = poly.complete_vertex_list

    # Outer boundary polygon must be COUNTER-CLOCK-WISE(ccw)
    # Create the outer boundary polygon
    # Define an epsilon value (should be != 0.0)
    vpoly = list(map(lambda x: vis.Point(x[0], x[1]), vs))
    walls = vis.Polygon(vpoly)
    walls.enforce_standard_form()

    # point from which to calculate visibility
    p1 = vs[j]
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
    for i in range(poly.size):
        p = vis.Point(*vs[i])
        vp = copy(p).projection_onto_boundary_of(isovist)
        if (vis.distance(vp, p) < EPSILON) and i != j:
            visibleVertexSet.append(i)
    if DEBUG:
        print('vertices',visibleVertexSet,'visible from',j)
    return visibleVertexSet

def get_all_edge_visible_vertices(poly):
    ''' make all sets of vertices visible from everywhere along edge
    '''
    all_viz_vxs = [visibleVertices(poly, i) for i in range(poly.size)]
    if DEBUG:
        print('All visible verts:\n{}\n'.format(all_viz_vxs))

    # each element in the map is indexed by its clockwise vertex (smaller index)
    vizSets = []

    # get vertices that are visible to the current vertex and the next vertex
    for i in range(poly.size):
        viz_vxs = list(set(all_viz_vxs[i]) & set(all_viz_vxs[(i+1)%poly.size]))
        # if the following line included, allows transition to next edge by wall
        # following, even if reflex angle
        # TODO: figure out if we want to allow this behavior
        viz_vxs.append((i+1)%poly.size) 
        # vizSets[i] = viz_vxs
        vizSets.append(viz_vxs)

    if DEBUG:
        print('viz sets\n--------\n{}\n'.format(vizSets))
    return vizSets 

def ShootRaysToReflexFromVerts(poly, j):
    ''' shoot ray from visible vertices through reflex verts
        Poly -> Int -> [(Point, Int)]
    '''
    psize = poly.size
    vs = poly.complete_vertex_list
    r_v = vs[j]
    pts = []
    visible_verts = visibleVertices(poly,j)

    # only ray shoot from non-adjacent vertices
    # previous and next neighbors always visible
    for v in visible_verts:
        if (v != (j-1)%psize) and (v != (j+1)%psize):
            #print('shooting ray from',v,'to',j)
            res = ClosestPtAlongRay(vs[v], r_v, poly)
            if res:
                pt, k = res
                if (IsInPoly((pt+r_v)/2, poly) and not VertexExists(pt, poly)):
                    #print('successful insert')
                    pts.append((pt, k, v))
    return pts

