import networkx as nx

from helper.visibility_helper import visibleVertices
from helper.bounce_graph_helper import check_valid_transit, validAnglesForContract, SafeAngles

class Bounce_Graph(object):
    ''' Bounce visibility diagram is the directed edge visibility graph a partitioned polygon
    Attributes
    ----------
    bounce_visibility_diagram
    visibility_graph
    safe_action_graph
    '''
    def create_bounce_visibility_graph(self, poly, inserted_poly, requireContract = False):
        ''' creates directed edge-to-edge visibility graph; edge information is angle ranges which create contraction mapping
        '''
        bvg = nx.DiGraph()

        for component in inserted_poly.vertex_list_per_poly:
            for start_i, start in component:
                m = len(component)
                viz_verts = visibleVertices(component, inserted_poly.vertex_list_per_poly,
                poly, start_i % m)
                if start_i == 21:
                    print("visible from 21:", viz_verts)
                if start_i == 22:
                    print("visible from 22:", viz_verts)
                vvs = [inserted_poly.vertex_list_per_poly[c][j][0]
                       for c, vv in enumerate(viz_verts)
                       for j in vv]
                edges = [(start_i,v,validAnglesForContract(inserted_poly, start_i, v))
                         for v in vvs if
                         check_valid_transit(v, start_i, inserted_poly)]
                if requireContract:
                    c_edges = [(i,j, angs) for (i,j,angs) in edges if angs != []]
                    bvg.add_weighted_edges_from(c_edges)
                else:
                    bvg.add_weighted_edges_from(edges)
        return bvg

    def create_safe_action_graph(self, bvg, poly, visible_vx_set_for_edges):
        ''' Remove edges with an empty angle range from the bounce visibility graph to create the safe action graph
        ''' 
        psize = poly.size
        safe_action_graph = nx.DiGraph()
        safe_action_graph.add_nodes_from(bvg.nodes())
        new_edges = []
        vs = poly.complete_vertex_list
        for i in safe_action_graph.nodes():
            outgoing = bvg.edges([i])
            vset = visible_vx_set_for_edges[i]+[i]
            for e in outgoing:
                e = e[1]
                e1 = (vs[i], vs[(i+1)%psize])
                e2 = (vs[e], vs[(e+1)%psize])
                e_viz = (e in vset) and ((e+1)%psize in vset)
                if SafeAngles(e1,e2) and e_viz:
                    curr_weight = '{0:.2f}'.format(SafeAngles(e1,e2)[1])
                    new_edges.append((i,e,curr_weight))
        safe_action_graph.add_weighted_edges_from(new_edges)
        return safe_action_graph

    def get_shortest_path(self, start_set, goal_set, graph_type = 'safe'):
        ''' Get shortest paths set from a start set to the goal set in a given graph
        '''
        if graph_type == 'safe':
            graph = self.safe_action_graph
        else:
            graph = self.visibility_graph
        return nx.all_shortest_paths(graph, start_set, goal_set)

    def __init__(self, bvd):
        self.bounce_visibility_diagram = bvd
        self.visibility_graph = self.create_bounce_visibility_graph(bvd.partial_local_sequence.polygon,
        bvd.partial_local_sequence.inserted_polygon)
        #self.safe_action_graph = self.create_safe_action_graph(self.visibility_graph, bvd.partial_local_sequence.inserted_polygon, bvd.visible_vx_set_for_edges)
