from partial_local_sequence import *
def GetAngleFromThreePoint(p1, p2, origin):
    v1 = (p1[0]-origin[0], p1[1]-origin[1])
    v2 = (p2[0]-origin[0], p2[1]-origin[1])
    return GetVector2Angle(v1, v2)

# sort by distance and remove duplicates
def SortByDistance(p1, unsorted_vs):
    unsorted_vs.append(p1)
    verts = list(set(unsorted_vs))
    return sorted(verts, key = lambda v: PointDistance(v,p1))

# find all induced transition points, sort and insert into polygon
# probably the most naive way to do this
# return a list of edge indicators for each vertex
def InsertAllTransitionPts(poly):
    t_pts_grouped = {i:[] for i in range(len(poly))}
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
    for i in range(len(poly)):
        new_poly_grouped[i] = SortByDistance(poly[i], t_pts_grouped[i])
        if DEBUG:
            print('Inserted verts', new_poly_grouped[i], 'on edge',i)

    # insert into polygon
    new_poly = []
    for i in range(len(poly)):
        new_poly.extend(new_poly_grouped[i])
    return new_poly

# make all sets of vertices visible from everywhere along edge
def mkVizSets(poly):
    psize = len(poly)
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

# Resolution is the number of sample points on each edge
def GetLinkDiagram(poly, resolution = 15):
    psize = len(poly)
    link_diagram = np.nan*np.ones((psize, resolution*psize))
    vizSets = mkVizSets(poly)
    for i in range(psize):
        # for each visible vertex, we need to calculate:
        #  (1) the view angle at the current vertex w.r.t the current edge and
        #  (2) the view angle at the sample points on the edge and the next vertex w.r.t the current edge
        #  (3) insert a np.nan for discontinuity otherwise matplotlib will try to connect them together
        for vx in vizSets[i]:
            curr_p = poly[i]
            next_p = poly[(i+1)%psize]
            interest_p = poly[vx]

            link_diagram[vx][resolution*i] = GetAngleFromThreePoint(next_p, interest_p, curr_p)
            # the if case is for when we are considering the 'next vertex'
            if interest_p == next_p:
                for stride in range(resolution)[1:-1]:
                    link_diagram[vx][resolution*i+stride] = link_diagram[vx][resolution*i]
            else:
                for stride in range(resolution)[1:-1]:
                    # this is the point on the same line of the current edge but in front of the next vertex.
                    # Use this so that we don't get zero length vector from the next vertex perspective
                    extended_point = (curr_p[0]+2*(next_p[0]-curr_p[0]), curr_p[1]+2*(next_p[1]-curr_p[1]))
                    ratio = 1./(resolution-2)*stride
                    origin = (ratio*next_p[0]+(1-ratio)*curr_p[0], ratio*next_p[1]+(1-ratio)*curr_p[1])
                    link_diagram[vx][resolution*i+stride] = GetAngleFromThreePoint(interest_p, extended_point, origin)
            link_diagram[vx][resolution*i+resolution-1] = np.nan
    return link_diagram
