from settings import *
from simple_polygon import Simple_Polygon
from helper.shoot_ray_helper import *

class Partial_Local_Sequence(object):
    ''' Partial local sequence is a sequence of points on the boundary of P associated with a vertex v0, and is constructed by shooting a ray through a reflex vertex v0 from every visible vertex and keeping the resulting sequence of intersections with the boundary of P. The partial local sequence for a convex vertex is empty.

    Attributes
    ----------
    polygon : numpy.array
        The polygon that the partial local sequence is built upon
    inserted_polygon : numpy.array
        The polygon with all new vertices inserted 
    sequence_info : list
        A 2D array stores the partial local sequence for each vertex in polygon in rows
    '''
    def compute_sequence(self, input_polygon):
        ''' Compute the partial local sequence for all vertices of the polygon
        '''
        rvs = FindReflexVerts(input_polygon.vertices)
        sequence_info = []
        for i in range(input_polygon.size):
            if not i in rvs:
                sequence_info.append([])
                continue
            r_children = ShootRaysFromReflex(input_polygon.vertices, i)
            transition_pts = ShootRaysToReflexFromVerts(input_polygon.vertices, i)
            transition_pts.extend(r_children)
            sequence_info.append(transition_pts)
        return sequence_info

    def compute_inserted_polygon(self, polygon, sequence_info):
        ''' Compute the polygon with all new vertices from the partial local sequence inserted
        '''
        t_pts_grouped = {i:[] for i in range(polygon.size)}
        for i in range(len(sequence_info)):
            for (pt, edge, _) in sequence_info[i]:
                t_pts_grouped[edge].append(pt)
        
        # sort transition points along edge
        new_poly_grouped = {}
        for i in range(polygon.size):
            new_poly_grouped[i] = sort_by_distance(polygon.vertices[i], np.array(t_pts_grouped[i]))
            if DEBUG:
                print('Inserted verts', new_poly_grouped[i], 'on edge',i)

        inserted_polygon = []
        new_vertices = []
        for i in range(polygon.size):
            new_vertices.extend(new_poly_grouped[i])
        inserted_polygon = Simple_Polygon(np.array(new_vertices))
        return inserted_polygon

    def __init__(self, polygon_vx):
        self.polygon = Simple_Polygon(polygon_vx)
        self.sequence_info = self.compute_sequence(self.polygon)
        self.inserted_polygon = self.compute_inserted_polygon(self.polygon, self.sequence_info) 