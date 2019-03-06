from helper.geometry_helper import *
from helper.general_position_helper import *
from settings import *

def VertexExists(v, poly):
    ''' Check whether a given vertex exists in the polygon
    '''
    vs = poly.complete_vertex_list
    for pt in vs:
        if la.norm(v-pt) < EPSILON:
            return True
    return False

