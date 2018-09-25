# #! /usr/bin/env python

# import unittest
# from src.bounce import *
# from src.geom_utils import *
# from src.graph_utils import *
# from src.graph_operations import *
# from src.maps import *

# class TestGeomUtils(unittest.TestCase):

#     def setUp(self):
#         self.origin = [0.0, 0.0]

#         # square on xy axis
#         self.p1 = [ 10.0,   0.0]
#         self.p2 = [-10.0,   0.0]
#         self.p3 = [  0.0,  10.0]
#         self.p4 = [  0.0, -10.0]

#         # right triangle
#         self.t1 = [6.0, 0.0]
#         self.t2 = [3.0, 4.0]
#         self.x3 = [[0.0, 0.0],[3.0,0.0]]
#         self.y4 = [[3.0, 0.0],[3.0,4.0]]

#         # edges
#         self.e1 = [self.origin, [1.0, 0.0]]
#         self.e2 = [[2.0,1.0], [2.0, 2.0]]

#         self.maxDiff = None

#     def test_left(self):
#         v1 = IsLeftTurn(self.p1, self.p2, self.p4)
#         v2 = IsLeftTurn(self.p2, self.p1, self.p3)
#         self.assertTrue(v1 and v2)

#     def test_right(self):
#         v1 = IsRightTurn(self.p1, self.p2, self.p3)
#         v2 = IsRightTurn(self.p2, self.p1, self.p4)
#         self.assertTrue(v1 and v2)

#     def test_contains(self):
#         self.assertTrue(IsInPoly((0.0,0.0), poly1))

#     def test_notIn(self):
#         self.assertFalse(IsInPoly((500.0,0.0), poly1))

#     def test_shootRayFromVect(self):
#         t, (x,y) = ShootRayFromVect(self.t1, self.t2, self.origin, self.p3)
#         self.assertAlmostEqual(x, 0.0)
#         self.assertAlmostEqual(y, 8.0)

#     def test_intersect_interior(self):
#         (x,y), _ = ClosestPtAlongRay(self.origin, self.p1, poly1)
#         self.assertAlmostEqual(x, 139.1304347826087)
#         self.assertAlmostEqual(y, 0.0)

#     def test_intersect_thru_vertex(self):
#         (x,y), _ = ClosestPtAlongRay(self.origin, (150,50), poly1)
#         self.assertAlmostEqual(x, 198.21428571428572)
#         self.assertAlmostEqual(y, 66.07142857142857)

#     def test_reflex(self):
#         rfverts = FindReflexVerts(poly1)
#         self.assertEqual([3,7,10], rfverts)

#     def test_transition_pts(self):
#         t3 = ShootRaysToReflexFromVerts(poly1, 3)
#         t7 = ShootRaysToReflexFromVerts(poly1, 7)
#         t9 = ShootRaysToReflexFromVerts(poly1, 9)
#         t10 = ShootRaysToReflexFromVerts(poly1, 10)
#         ts3 = [((-67.74193548387098, 182.25806451612902), 4), ((109.82142857142857, 186.60714285714286), 1), ((-60.0, 190.0), 4)]
#         ts7 = [((-206.18384401114204, -199.13649025069637), 8), ((-127.36842105263163, -194.21052631578948), 8)]
#         ts10 = [((-177.77777777777777, 50.00000000000004), 5), ((207.44680851063828, 11.70212765957443), 0), ((209.34065934065933, 40.10989010989009), 0), ((205.3602811950791, 56.32688927943761), 1), ((199.90439770554494, 63.76673040152964), 1), ((190.12048192771084, 77.10843373493977), 1)]
#         self.assertEqual(ts3, t3)
#         self.assertEqual(ts7, t7)
#         self.assertEqual([], t9)
#         self.assertEqual(ts10, t10)

#     def test_viz_verts(self):
#         p = InsertAllTransitionPts(simple_bit)
#         self.assertEqual([2, 4, 5, 6, 7], GetVisibleVertices(p,3))
#         self.assertEqual([0, 1, 3, 4, 5, 6, 7, 8, 10, 11], GetVisibleVertices(p,2))

#     def test_viz_gp(self):
#         p = InsertAllTransitionPts(tworooms)
#         self.assertEqual([1, 2, 11, 12, 13, 14, 15], GetVisibleVertices(p, 0))

#     def test_angle_parallel(self):
#         a = angleBound(square, 1, 3)
#         self.assertAlmostEqual(a, 1.57079632679)

#     def test_angle_collinear(self):
#         p = [(0,0),(0,10),(0,20)]
#         a = angleBound(p, 0, 1)
#         self.assertAlmostEqual(a, 0.0)

#     # use triangle properties to check that angles are calculated properly
#     def test_maxmin_angles(self):
#         max_a = 63.4349488*(pi/180)
#         min_a = 26.5650511*(pi/180)
#         min_c, max_c = AnglesBetweenSegs(self.e1, self.e2)
#         self.assertAlmostEqual(min_c, min_a)
#         self.assertAlmostEqual(max_c, max_a)

#     def test_maxmin_adjacent(self):
#         min_a = 0.0
#         max_a = pi/2
#         min_c, max_c = AnglesBetweenSegs(self.x3, self.y4)
#         self.assertAlmostEqual(min_c, min_a)
#         self.assertAlmostEqual(max_c, max_a)


#     def test_graph_reduce(self):
#         G = mkGraph(square)
#         H = reduceGraphWrtAngle(G, 0.0, 0.2)
#         self.assertEqual(H.edge,
#             {0: {1: {'weight': [(0, 0.2)]}}, 1: {2: {'weight': [(0, 0.2)]}}, 2: {3: {'weight': [(0, 0.2)]}}, 3: {0: {'weight': [(0, 0.2)]}}}
#             )

#     def test_general_pos(self):
#         self.assertFalse(PolyInGeneralPos(tworooms2))
#         self.assertTrue(poly1)

#     def test_shootInterval(self):
#         # land inside interval
#         pt1, pt2 = ShootInterval(square, 3, 0, (-10,-250), (10,-250), pi/2, pi/2)
#         self.assertAlmostEqual(pt1[0], 10)
#         self.assertAlmostEqual(pt1[1], 250)
#         self.assertAlmostEqual(pt2[0], -10)
#         self.assertAlmostEqual(pt2[1], 250)

#         # land outside interval, clip to endpoints
#         pt3, pt4 = ShootInterval(square, 3, 0, (-10,-250), (10,-250), 0.1, pi-0.1)
#         self.assertAlmostEqual(pt3[0], 250)
#         self.assertAlmostEqual(pt3[1], 250)
#         self.assertAlmostEqual(pt4[0], -250)
#         self.assertAlmostEqual(pt4[1], 250)

#     def test_nodeParam(self):
#         self.assertEqual(nodesCovered(square,(0.1,0.6)),[0,1,2])
#         self.assertEqual(nodesCovered(square,(0.9,0.1)),[3,0])
#         self.assertEqual(nodesCovered(square,(0.1,0.2)),[0])

# if __name__ == '__main__':
#     unittest.main()