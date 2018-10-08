from helper.geometry_helper import *
from helper.general_position_helper import *
from settings import *

def IsInPoly(p, poly):
    ''' test if point p is in poly using crossing number
    '''
    intersects = 0
    theta = np.random.rand()*2*np.pi
    state=(p[0],p[1],theta)
    psize = len(poly)
    for j in range(psize):
        v1, v2 = poly[j], poly[(j+1) % psize]
        try:
            t, u, pt = ShootRay(state, v1, v2)
            if t>0 and (0 < u) and (u < 1):
                intersects += 1
        except:
            pass
    return not (intersects%2 == 0)

def VertexExists(v, poly):
    ''' Check whether a given vertex exists in the polygon
    '''
    for pt in poly:
        if la.norm(v-pt) < EPSILON:
            return True
    return False

def FindReflexVerts(poly):
    ''' return indices of all reflex vertices in poly
    '''
    psize = poly.shape[0]
    reflex_verts = []
    for j in range(psize):
        v1, v2, v3 = poly[(j-1) % psize], poly[j], poly[(j+1) % psize]
        if IsRightTurn(v1,v2,v3) and not IsThreePointsOnLine(v1,v2,v3):
            reflex_verts.append(j)

    return reflex_verts
