from geom_utils import *
from helper.visibility_helper import *
from helper.polygon_helper import *
from settings import *

# shoot two rays from each reflex vertex, along incident edges
# group by edge so we can insert them in correct order
def ShootRaysFromReflex(poly, j):
    psize = len(poly)
    p2 = poly[j]
    p1_ccw = poly[(j+1) % psize]
    p1_cw = poly[(j-1) % psize]

    int_pts = []

    # ClosestPtAlongRay returns False if we shoot ray into existing vertex
    if ClosestPtAlongRay(p1_ccw,p2,poly,j):
        pt, k = ClosestPtAlongRay(p1_ccw,p2,poly,j)
        if not VertexExists(pt, poly):
            int_pts.append((pt,k))

    if ClosestPtAlongRay(p1_cw,p2,poly,((j-1) % psize)):
        pt, k = ClosestPtAlongRay(p1_cw,p2,poly,((j-1) % psize))
        if not VertexExists(pt, poly):
            int_pts.append((pt,k))

    return int_pts

# shoot ray from visible vertices through reflex verts
# Poly -> Int -> [(Point, Int)]
def ShootRaysToReflexFromVerts(poly, j):
    psize = poly.shape[0]
    r_v = poly[j]
    pts = []
    visible_verts = GetVisibleVertices(poly,j)

    # only ray shoot from non-adjacent vertices
    # previous and next neighbors always visible
    for v in visible_verts:
        if (v != (j-1)%psize) and (v != (j+1)%psize):
            #print('shooting ray from',v,'to',j)
            res = ClosestPtAlongRay(poly[v], r_v, poly)
            if res:
                pt, k = res
                if (IsInPoly((pt+r_v)/2, poly) and
                    not VertexExists(pt, poly)):
                    #print('successful insert')
                    pts.append((pt,k))
    return pts
