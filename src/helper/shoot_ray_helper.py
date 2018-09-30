from src.helper.geometry_helper import *
from src.helper.visibility_helper import *
from src.helper.polygon_helper import *
from src.settings import *

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
    den = (a*np.cos(theta)+b*np.sin(theta))
    # case when lines are parallel
    if abs(den) < 0.000001:
        if DEBUG:
            print('divide by zero in ray shoot')
            print('shot from ',state,'to',v1,v2)
        raise ValueError
    else:
        t = (-c - b*y1 - a*x1)/den
        pint = (x1 + np.cos(theta)*t, y1 + np.sin(theta)*t)
    return t, pint

# shoot a ray starting at p1, along vector p1->p2
# find intersection with edge v1,v2
# will return first intersection *after* p2
def ShootRayFromVect(p1, p2, v1, v2):
    [x,y] = p2-p1# recenter points so p1 is at origin
    theta = FixAngle(np.arctan2(y,x))
    state = (p2[0], p2[1], theta)
    return ShootRay(state, v1, v2)

# shoot ray from p1 toward p2 in poly, return closest intersect point
# will not return point on 'last_bounce_edge'
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
            try:
                t,pt = ShootRayFromVect(p1, p2, v1, v2)
                
                # Find closest bounce for which t > 0
                pdist = la.norm(pt-p2)
                if ((t > 0) and (pdist < closest_bounce) and
                    BouncePointInEdge((x1,y1),pt,v1,v2)):
                    found_coll = True
                    bounce_point = pt
                    closest_bounce = pdist
                    bounce_edge = j
            # bounce was parallel to edge j
            # check if it's parallel and overlapping for degenerate polys
            except:
                pass
    if found_coll:
        return bounce_point, bounce_edge
    else:
        return False

def ShootRaysFromReflex(poly, j):
    ''' shoot two rays from each reflex vertex, along incident edges
        group by edge so we can insert them in correct order
    '''
    psize = len(poly)
    p2 = poly[j]
    p1_ccw = poly[(j+1) % psize]
    p1_cw = poly[(j-1) % psize]

    int_pts = []

    # ClosestPtAlongRay returns False if we shoot ray into existing vertex
    if ClosestPtAlongRay(p1_ccw,p2,poly,j):
        pt, k = ClosestPtAlongRay(p1_ccw,p2,poly,j)
        if not VertexExists(pt, poly):
            int_pts.append((pt,k, (j+1) % psize))

    if ClosestPtAlongRay(p1_cw,p2,poly,((j-1) % psize)):
        pt, k = ClosestPtAlongRay(p1_cw,p2,poly,((j-1) % psize))
        if not VertexExists(pt, poly):
            int_pts.append((pt,k, (j-1) % psize))

    return int_pts

def ShootRaysToReflexFromVerts(poly, j):
    ''' shoot ray from visible vertices through reflex verts
        Poly -> Int -> [(Point, Int)]
    '''
    psize = poly.shape[0]
    r_v = poly[j]
    pts = []
    visible_verts = get_visible_vertices(poly,j)

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
                    pts.append((pt,k, v))
    return pts
