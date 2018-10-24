from helper.geometry_helper import *
from helper.general_position_helper import *
from settings import *

def VertexExists(v, vertex_list_per_poly):
    ''' Check whether a given vertex exists in the polygon
    '''
    for vs in vertex_list_per_poly:
      for pt in vs:
          if la.norm(v-pt[1]) < EPSILON:
              return True
    return False

