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
        for g in get_vertices_in_interval(self.inserted_polygon.unit_interval_mapping, self.end_interval):
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
    sbvg : :obj:`Bounce_Visibility_Graph`
    polygon: :obj:`Simple_Polygon`
    '''

    def __init__(self, start, end, bvg):
        self.sbvg = bvg.safe_action_graph
        self.polygon = bvg.bounce_visibility_diagram.partial_local_sequence.inserted_polygon
        self.start = get_vertices_in_interval(self.polygon.unit_interval_mapping, start)
        self.end = get_vertices_in_interval(self.polygon.unit_interval_mapping, end)

    def navigate(self, depth = -1):
        if depth == -1:
            depth = self.sbvg.number_of_nodes()
        angrange = [(0.0, pi)]
        pathstates = [(s, angrange) for s in self.start]

        for i in range(depth):
            frontier = []
            for (v, angrange) in pathstates:
                # list of nodes reached and corresponding angranges for kth step
                # in BFS from one of the start nodes
                frontier.extend(self.take_step(self.sbvg, v, angrange))
            if self.atGoal(frontier):
                    return True, frontier

        return False, frontier

    # PathState is:
        # the current vertex, and
        # a list of angle intervals admitted by a path from a start node to that vertex
    # take a step from a single node s
    # Graph -> PathState -> [PathState]
    def take_step(self, G, s, angranges):

        valid_neighbors = []

        for n in nx.neighbors(G, s):
            safe_interval = G[s][n]['weight']
            print("safe interval", safe_interval)
            resulting_intervals = self.path_filter(angranges, safe_interval)
            if resulting_intervals != []:
                print("neighbor",n,"ranges", resulting_intervals)
                valid_neighbors.append( (n, resulting_intervals) )
        print("found all valid neighbors", valid_neighbors)
        return valid_neighbors


    # SafeState is the single safe bounce interval admitted by a single transition
    # State could also be a list of intervals: set of angles that admit a contraction mapping
    # intersect SafeState with old PathState
    # coming soon: union resulting projection of robot state, vizualize estimate
    # [(Angle, Angle)] -> (Angle, Angle) -> [(Angle, Angle)]
    def path_filter(self, old_aranges, safe_interval):
        print(old_aranges)
        iis = [intersect_intervals(angrange, safe_interval) for angrange in old_aranges]
        print("new intervals", iis)
        return [i for i in iis if interval_len(i) > EPSILON]


    # [[PathState]] -> Bool
    def atGoal(self, frontier):
        curr_nodes = [v for (v, angs) in frontier]
        goal = set(self.end)
        print("curr", curr_nodes)
        curr = set(curr_nodes)
        return goal.issubset(curr)


