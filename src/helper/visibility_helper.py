#!/usr/bin/env python

import visilibity as vis
from copy import copy
from settings import *
import numpy as np
# for polygons not in general position: returns all visible vertices along a ray

def visibleVertices(curr_poly_vx, vertex_list_per_poly, j):
    vs = [v for i,v in curr_poly_vx]

    # Outer boundary polygon must be COUNTER-CLOCK-WISE(ccw)
    # Create the outer boundary polygon
    # Define an epsilon value (should be != 0.0)
    def get_vis_form_from_vx_list(vs):
        poly = list(map(lambda x: vis.Point(x[1][0], x[1][1]), vs))
        walls = vis.Polygon(poly)
        walls.enforce_standard_form()
        return walls

    env_walls = [get_vis_form_from_vx_list(vs) for vs in vertex_list_per_poly]

    # point from which to calculate visibility
    p1 = vs[j]
    vp1 = vis.Point(p1[0],p1[1])

    # Create environment, wall will be the outer boundary because
    # is the first polygon in the list. The other polygons will be holes
    env = vis.Environment(env_walls)
    # Necesary to generate the visibility polygon
    vp1.snap_to_boundary_of(env, EPSILON)
    vp1.snap_to_vertices_of(env, EPSILON)
    isovist = vis.Visibility_Polygon(vp1, env, EPSILON)
    vvs = [(isovist[i].x(), isovist[i].y()) for i in range(isovist.n())]
    visibleVertexSet = []
    for poly_vx in vertex_list_per_poly:
        curr_vis_vx = []
        for i in range(len(poly_vx)):
            p = vis.Point(*poly_vx[i][1])
            vp = copy(p).projection_onto_boundary_of(isovist)
            if (vis.distance(vp, p) < EPSILON) and poly_vx[i][0] != curr_poly_vx[j][0]:
                curr_vis_vx.append(i)
        if DEBUG:
            print('vertices',curr_vis_vx,'visible from',j)
        visibleVertexSet.append(curr_vis_vx)
    return visibleVertexSet

def get_all_edge_visible_vertices(poly):
    ''' make all sets of vertices visible from everywhere along edge
    '''
    total_viz_sets = []
    for index, curr_poly_vx in enumerate(poly.vertex_list_per_poly):
        curr_viz_vxs = [visibleVertices(curr_poly_vx, poly.vertex_list_per_poly, i) for i in range(len(curr_poly_vx))]
        if DEBUG:
            print('All visible verts:\n{}\n'.format(curr_viz_vxs))

        # each element in the map is indexed by its clockwise vertex (smaller index)
        curr_viz_sets = []

        # get vertices that are visible to the current vertex and the next vertex
        for i in range(len(curr_poly_vx)):
            viz_vxs = get_common_list_of_list_visible_vertices(curr_viz_vxs[i], curr_viz_vxs[(i+1)%len(curr_poly_vx)], (curr_poly_vx[i][1], curr_poly_vx[(i+1)%len(curr_poly_vx)][1]), poly.complete_vertex_list)
            # if the following line included, allows transition to next edge by wall
            # following, even if reflex angle
            # TODO: figure out if we want to allow this behavior
            viz_vxs[index].append((i+1)%len(curr_poly_vx)) 
            # vizSets[i] = viz_vxs
            curr_viz_sets.append(viz_vxs)

        if DEBUG:
            print('viz sets\n--------\n{}\n'.format(curr_viz_sets))
        total_viz_sets.append(curr_viz_sets)
        
    return total_viz_sets 

def check_vertex_in_edge_half_plane(edge, vertex):
    ''' the vertex should be to the left of the edge
    '''
    v1 = edge[0]-vertex
    v2 = edge[1]-vertex 
    return np.cross(v1, v2) >= 0

def get_common_list_of_list_visible_vertices(ll_1, ll_2, edge, complete_vertex_list):
    # ll_1 and ll_2 should have the same size
    l_size = len(ll_1)
    common_list = []
    for i in range(l_size):
        common_visible_vertex = list(set(ll_1[i]) & set(ll_2[i]))
        filted_visible_vertex = []
        for vertex in common_visible_vertex:
            if check_vertex_in_edge_half_plane(edge, complete_vertex_list[vertex]):
                filted_visible_vertex.append(vertex)
        common_list.append(filted_visible_vertex)
    return common_list

