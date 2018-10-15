from helper.geometry_helper import *
from helper.general_position_helper import *
from settings import *

def VertexExists(v, all_poly_vxs):
    ''' Check whether a given vertex exists in the polygon
    '''
    for vs in all_poly_vxs:
      for pt in vs:
          if la.norm(v-pt[1]) < EPSILON:
              return True
    return False

