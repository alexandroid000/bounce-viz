
class Simple_Polygon(object):
    ''' Partial local sequence is a sequence of points on ∂P associated with a vertex v0, and is constructed by shooting a ray through a reflex vertex v0 from every visible vertex and keeping the resulting sequence of intersections with ∂P. The partial local sequence for a convex vertex is empty.

    Attributes
    ----------
    vertices : numpy.array
        A list of coordinates of vertices in the polygon in counter clockwise order.
        
    '''
    def __init__(self, vertices):
        self.vertices = vertices
        self.size = vertices.shape[0]