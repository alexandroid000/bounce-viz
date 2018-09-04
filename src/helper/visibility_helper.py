import visilibity as vis
from settings import *
from copy import copy
# for polygons not in general position: returns all visible vertices along a ray

def GetVisibleVertices(poly, j):
    #print('At vertex',j)
    psize = len(poly)

    # Outer boundary polygon must be COUNTER-CLOCK-WISE(ccw)
    # Create the outer boundary polygon
    # Define an epsilon value (should be != 0.0)
    vpoly = [vis.Point(*pt) for pt in poly]
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
