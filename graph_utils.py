#!/usr/bin/env python

# graph_utils.py
# functions for constructing and querying the bounce visibility graph

# the coefficent of "contraction" for the mapping from edge i to edge j
# |f(x) - f(y)| = |x - y| * sin(theta) / sin (theta-phi)
# -1 < |f(x) - f(y)| < 1 leads to
# theta > phi/2
# theta < -phi/2
# for contraction mapping
def angleBound(poly, i, j):
    n = len(poly)
    v1 = Points2Vect(poly[i], poly[(i+1) % n])
    v2 = Points2Vect(poly[j], poly[(j+1) % n])
    phi = GetVector2Angle(v1, v2)
    return phi/2

def coeff(poly, i, j, theta):
    phi = 2*angleBound(poly, i, j)
    return sin(theta) / sin (theta-phi)

def mkGraph(poly):
    G = nx.DiGraph()

    t_pts = InsertAllTransitionPts(poly)
    r_vs = FindReflexVerts(poly)
    psize = len(t_pts)

    for i in range(psize):
        edges = [(i,v,angleBound(t_pts, i, v)) for v in GetVisibleVertices(t_pts, i)]
        if DEBUG:
            print("Raw edges")
            for i,v,a in edges:
                print("Can see ", v, " from ", i, " with angle bound ", a)
        G.add_weighted_edges_from(edges)
    if DEBUG:
        print("Graph data:")
        print(G.nodes())
        print(G.edges())
    plt.clf()
    nx.draw_circular(G, with_labels=True)
    plt.savefig("graph.png")
    return G


