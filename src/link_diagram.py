from partial_local_sequence import *
import numpy as np
import numpy.linalg as la

def GetAngleFromThreePoint(p1, p2, origin):
    return GetVector2Angle(p1-origin, p2-origin)

def SortByDistance(p1, unsorted_vs):
    ''' sort the input vertices by distance and remove duplicates

    '''
    if unsorted_vs.shape[0] == 0:
        unsorted_vs = p1
    else:
        unsorted_vs = np.vstack((unsorted_vs, p1))
    verts = list(np.unique(np.reshape(unsorted_vs, (-1, 2)), axis = 0))
    return sorted(verts, key = lambda v: la.norm(v-p1))

# find all induced transition points, sort and insert into polygon
# probably the most naive way to do this
# return a list of edge indicators for each vertex
def InsertAllTransitionPts(poly):
    t_pts_grouped = {i:[] for i in range(poly.shape[0])}
    rvs = FindReflexVerts(poly)
    # find all transition points, group by edge
    for p in rvs:
        t_pts = []
        t_pts.extend(ShootRaysFromReflex(poly, p))
        t_pts.extend(ShootRaysToReflexFromVerts(poly,p))
        for (pt,edge_i) in t_pts:
            t_pts_grouped[edge_i].append(pt)

    # sort transition points along edge
    new_poly_grouped = {}
    for i in range(poly.shape[0]):
        new_poly_grouped[i] = SortByDistance(poly[i], np.array(t_pts_grouped[i]))
        if DEBUG:
            print('Inserted verts', new_poly_grouped[i], 'on edge',i)

    # insert into polygon
    new_poly = []
    for i in range(poly.shape[0]):
        new_poly.extend(new_poly_grouped[i])
    return np.array(new_poly)

# make all sets of vertices visible from everywhere along edge
def mkVizSets(poly):
    psize = poly.shape[0]
    all_viz_vxs = [GetVisibleVertices(poly, i) for i in range(psize)]
    if DEBUG:
        print('All visible verts:')
        print(all_viz_vxs)
        print('\n')

    # each element in the map is indexed by its clockwise vertex (smaller index)
    vizSets = {i:[] for i in range(psize)}

    # get vertices that are visible to the current vertex and the next vertex
    for i in range(psize):
        viz_vxs = list(set(all_viz_vxs[i]) & set(all_viz_vxs[(i+1)%psize]))
        # if the following line included, allows transition to next edge by wall
        # following, even if reflex angle
        # TODO: figure out if we want to allow this behavior
        viz_vxs.append((i+1)%psize) 
        vizSets[i] = viz_vxs

    if DEBUG:
        print('viz sets')
        print('--------')
        print(vizSets)
        print('')
    return vizSets 

def GetLinkDiagram(poly, resolution = 15):
    ''' Compute the link diagram for the input polygon
        For each visible vertex, we need to calculate:
         (1) the view angle at the current vertex w.r.t the current edge and
         (2) the view angle at the sample points on the edge and the next vertex w.r.t the current edge
         (3) insert a np.nan for discontinuity otherwise matplotlib will try to connect them together

    Parameters
    ----------
    poly:np.array
        The input polygon represented by its vertex coordinates
    resolution:int
        the number of sample points on each edge

    Returns
    -------
    np.array
        The link diagram for the input polygon
    '''
    psize = poly.shape[0]
    link_diagram = np.nan*np.ones((psize, resolution*psize))
    vizSets = mkVizSets(poly)
    for i in range(psize):
        for vx in vizSets[i]:
            curr_p = poly[i]
            next_p = poly[(i+1)%psize]
            interest_p = poly[vx]

            link_diagram[vx][resolution*i] = GetAngleFromThreePoint(next_p, interest_p, curr_p)
            # the if case is for when we are considering the 'next vertex'
            if (interest_p == next_p).all():
                for stride in range(resolution)[1:-1]:
                    link_diagram[vx][resolution*i+stride] = link_diagram[vx][resolution*i]
            else:
                for stride in range(resolution)[1:-1]:
                    # this is the point on the same line of the current edge but in front of the next vertex.
                    # Use this so that we don't get zero length vector from the next vertex perspective
                    extended_point = curr_p+2*(next_p-curr_p)
                    ratio = 1./(resolution-2)*stride
                    origin = ratio*next_p+(1-ratio)*curr_p
                    link_diagram[vx][resolution*i+stride] = GetAngleFromThreePoint(interest_p, extended_point, origin)
            link_diagram[vx][resolution*i+resolution-1] = np.nan
    return link_diagram
