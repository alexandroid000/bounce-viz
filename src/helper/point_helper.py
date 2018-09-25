import numpy as np
import numpy.linalg as la
from helper.geometry_helper import *
def sort_by_distance(p1, unsorted_vs):
    ''' sort the input vertices by distance and remove duplicates

    '''
    if unsorted_vs.shape[0] == 0:
        unsorted_vs = p1
    else:
        unsorted_vs = np.vstack((unsorted_vs, p1))
    verts = list(np.unique(np.reshape(unsorted_vs, (-1, 2)), axis = 0))
    return sorted(verts, key = lambda v: la.norm(v-p1))

def get_angle_from_three_pts(p1, p2, origin):
    return GetVector2Angle(p1-origin, p2-origin)