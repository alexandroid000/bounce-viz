import networkx as nx
from helper.bounce_graph_helper import *
from math import pi

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
    start_interval : (float, float)
        The range of starting interval in the unit interval mapping of the polygon
    end_interval : (float, float)
        The range of ending interval in the unit interval mapping of the polygon
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
        for g in get_vertices_in_interval(self.inserted_polygon.unit_interval_mapping,
        self.end_interval):
            for s in get_vertices_in_interval(self.inserted_polygon.unit_interval_mapping,
            self.start_interval):
                paths.append(self.bvg.get_shortest_path(s, g, 'safe'))
        return get_transition_over_path(paths[0], self.bvg.safe_action_graph)

    def __init__(self, start_interval, end_interval, bvg):
        self.start_interval = start_interval 
        self.end_interval = end_interval  
        self.bvg = bvg
        self.bvd = bvg.bounce_visibility_diagram
        self.pls = self.bvd.partial_local_sequence
        self.polygon = self.pls.polygon
        self.inserted_polygon = self.pls.inserted_polygon


# strategy is a function which performs BFS
class ConstantStrategy():
    ''' Navigation assuming our robot can only perform one type of bounce, with
    uncertainty. Searches safe bounce visibility graph.
    Attributes
    ----------
    start_interval : (float, float)
        The range of starting position in the unit interval mapping of the polygon
    end_interval : (float, float)
        The range of ending position in the unit interval mapping of the polygon
    bvg : :obj:`Bounce_Visibility_Graph`
    bvd: :obj:`Bounce_Visibility_Diagram`
    pls: :obj:`Partial_Local_Sequence`
    polygon: :obj:`Simple_Polygon`
    '''

    def __init__(self, start, end, bvg):
        self.start_interval = start 
        self.end_interval = end  
        self.sbvg = bvg.safe_action_graph
        self.bvd = bvg.bounce_visibility_diagram
        self.pls = self.bvd.partial_local_sequence
        self.polygon = self.pls.inserted_polygon


    def take_step(self, G, s, angranges):
        succs = nx.neighbors(G, s)
        valid_neighbors = []
        for n in succs:
            safe_bounce_interval = G[s][n]['weight']
            res_aranges = [intersect_intervals(i, safe_bounce_interval) for i in angranges]
            nonempty_ranges = [(n,i) for i in res_aranges if interval_len(i) > EPSILON]
            if nonempty_ranges != []:
                valid_neighbors.extend(nonempty_ranges)

        return valid_neighbors

