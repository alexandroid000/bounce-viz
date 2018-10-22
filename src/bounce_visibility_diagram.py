import numpy as np

from helper.visibility_helper import *
from helper.geometry_helper import *


class Bounce_Visibility_Diagram(object):
    ''' Bounce visibility diagram is a representation of the vertex-edge visibility structure of a partitioned polygon
    
    Attributes
    ----------
    resolution : int
        the discretization constant for the angle function
    partial_local_sequence : :obj:`Partial_Local_Sequence`
        The partial local sequence for the polygon
    visible_angle_info : numpy.array
        The angle functions for each edge
    '''
    def compute_visible_angle_info(self, pls, visible_vx_set_for_edges, resolution):
        ''' Compute the visible angle info for the input polygon
            For each visible vertex, we need to calculate:
             (1) the view angle at the current vertex w.r.t the current edge and
             (2) the view angle at the sample points on the edge and the next vertex w.r.t the current edge
             (3) insert a np.nan for discontinuity otherwise matplotlib will try to connect them together

        Parameters
        ----------
        pls: :obj:`Partial_Local_Sequence`
        resolution:int
            the number of sample points on each edge

        Returns
        -------
        np.array
            The visible angle info for the input polygon
        '''
        i_poly_vx = pls.inserted_polygon.outer_boundary_vertices
        psize =  len(i_poly_vx)
        visible_angle_info = np.nan*np.ones((psize, resolution*psize))
        for i, visible_vxs in enumerate(visible_vx_set_for_edges):
            for vx_index in visible_vxs:
                curr_p = i_poly_vx[i]
                next_p = i_poly_vx[(i+1)%psize]
                interest_p = i_poly_vx[vx_index]
                visible_angle_info[vx_index][resolution*i] = get_angle_from_three_pts(next_p, interest_p, curr_p)
                visible_angle_info[vx_index][resolution*i+resolution-1] = np.nan
                # the if case is for when we are considering the 'next vertex'
                if (interest_p == next_p).all():
                    for stride in range(resolution)[1:-1]:
                        visible_angle_info[vx_index][resolution*i+stride] = visible_angle_info[vx_index][resolution*i]
                    continue
                for stride in range(resolution)[1:-1]:
                    # this is the point on the same line of the current edge but in front of the next vertex.
                    # Use this so that we don't get zero length vector from the next vertex perspective
                    extended_point = curr_p+2*(next_p-curr_p)
                    ratio = 1./(resolution-2)*stride
                    origin = ratio*next_p+(1-ratio)*curr_p
                    visible_angle_info[vx_index][resolution*i+stride] = get_angle_from_three_pts(interest_p, extended_point, origin)
        return visible_angle_info

    def __init__(self, pls):
        self.resolution = 15
        self.partial_local_sequence = pls
        self.visible_vx_set_for_edges = get_all_edge_visible_vertices(pls.inserted_polygon)
        self.visible_angle_info = self.compute_visible_angle_info(pls, self.visible_vx_set_for_edges, self.resolution)
