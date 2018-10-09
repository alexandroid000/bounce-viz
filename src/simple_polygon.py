from numpy.linalg import norm
import numpy as np
import settings as settings
from helper.geometry_helper import IsRightTurn
from helper.general_position_helper import IsThreePointsOnLine

class Simple_Polygon(object):
    ''' Partial local sequence is a sequence of points on the boundary of P associated with a vertex v0, and is constructed by shooting a ray through a reflex vertex v0 from every visible vertex and keeping the resulting sequence of intersections with the boundary of P. The partial local sequence for a convex vertex is empty.

    Attributes
    ----------
    vertices : numpy.array
        A list of coordinates of vertices in the polygon in counter clockwise order.
        
    '''
    def compute_unit_interval_mapping(self):
        ''' Map the vertices of the polygon on to a given interval (length specified in settings) where both the start and the end of the interval identify with the first vertex in the polygon
        '''
        edge_len = [norm(self.vertices[i]-self.vertices[(i+1)%self.size]) for i in range(self.size)]
        acc_edge_len = np.array([sum(edge_len[:i]) for i in range(len(edge_len)+1)])
        acc_edge_len /= acc_edge_len[-1]/settings.unit_interval_len
        return acc_edge_len

    def reflex_verts(self, vs):
        ''' return indices of all reflex vertices in poly
        '''
        reflex_verts = []
        for j in range(self.size):
            v1, v2, v3 = vs[(j-1) % self.size], vs[j], vs[(j+1) % self.size]
            if IsRightTurn(v1,v2,v3) and not IsThreePointsOnLine(v1,v2,v3):
                reflex_verts.append(j)

        return reflex_verts

    def __init__(self, vertices):
        self.vertices = vertices
        self.size = vertices.shape[0]
        self.rverts = self.reflex_verts(self.vertices)
        self.unit_interval_mapping = self.compute_unit_interval_mapping()
