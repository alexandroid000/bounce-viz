def get_vertices_in_interval(poly_unit_map, interval):
    ''' Find vertices on the polygon that are in the range specified
    '''
    (s1, s2) = interval
    vxs = []
    for i in range(len(poly_unit_map)-1):
        if poly_unit_map[i]<s1*10:
            continue
        if poly_unit_map[i]>s2*10:
            break
        vxs.append(i)
    return vxs

def get_transition_over_path(path, safe_action_graph):
    ''' Get the transition with angle range information from a given path
    '''
    transitions = []
    path = list(path)[0]
    for (i,j) in zip(path, path[1:]):
        ang_range = safe_action_graph.get_edge_data(i,j)
        transitions.append((i,j,ang_range))
    return transitions

class Navigation(object):
    ''' Description of a navigation task for a given polygon
    Attributes
    ----------
    start_position : (float, float)
        The range of starting position in the unit interval mapping of the polygon
    end_position : (float, float)
        The range of ending position in the unit interval mapping of the polygon
    bvg : :obj:`Bounce_Visibility_Graph`
    bvd: :obj:`Bounce_Visibility_Diagram`
    pls: :obj:`Partial_Local_Sequence`
    polygon: :obj:`Simple_Polygon`
    inserted_polygon: :obj:`Simple_Polygon`
    '''
    def navigate(self):
        ''' Executing the navigation task with a given strategy
        '''
        paths = []
        for g in get_vertices_in_interval(self.inserted_polygon.unit_interval_mapping, self.end_position):
            for s in get_vertices_in_interval(self.inserted_polygon.unit_interval_mapping, self.start_position):
                paths.append(self.bvg.get_shortest_path(s, g, 'safe'))
        return get_transition_over_path(paths[0], self.bvg.safe_action_graph)

    def __init__(self, start_position, end_position, bvg):
        self.start_position = start_position 
        self.end_position = end_position  
        self.bvg = bvg
        self.bvd = bvg.bounce_visibility_diagram
        self.pls = self.bvd.partial_local_sequence
        self.polygon = self.pls.polygon
        self.inserted_polygon = self.pls.inserted_polygon