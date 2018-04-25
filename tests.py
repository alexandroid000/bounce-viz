#! /usr/bin/env python

import unittest
from geom_utils import *
from maps import *

class TestGeomUtils(unittest.TestCase):

    def setUp(self):
        self.origin = [0.0, 0.0]

        # square on xy axis
        self.p1 = [ 10.0,   0.0]
        self.p2 = [-10.0,   0.0]
        self.p3 = [  0.0,  10.0]
        self.p4 = [  0.0, -10.0]

        # right triangle
        self.t1 = [6.0, 0.0]
        self.t2 = [3.0, 4.0]

    def test_left(self):
        v1 = IsLeftTurn(self.p1, self.p2, self.p4)
        v2 = IsLeftTurn(self.p2, self.p1, self.p3)
        self.assertTrue(v1 and v2)

    def test_right(self):
        v1 = IsRightTurn(self.p1, self.p2, self.p3)
        v2 = IsRightTurn(self.p2, self.p1, self.p4)
        self.assertTrue(v1 and v2)

    def test_contains(self):
        self.assertTrue(IsInPoly((0.0,0.0), poly1))

    def test_notIn(self):
        self.assertFalse(IsInPoly((500.0,0.0), poly1))

    def test_shootRayFromVect(self):
        t, (x,y) = ShootRayFromVect(self.t1, self.t2, self.origin, self.p3)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 8.0)

    def test_intersect_interior(self):
        (x,y), _ = ClosestPtAlongRay(self.origin, self.p1, poly1)
        self.assertAlmostEqual(x, 139.1304347826087)
        self.assertAlmostEqual(y, 0.0)

    def test_intersect_thru_vertex(self):
        (x,y), _ = ClosestPtAlongRay(self.origin, (150,50), poly1)
        self.assertAlmostEqual(x, 198.21428571428572)
        self.assertAlmostEqual(y, 66.07142857142857)

    def test_reflex(self):
        rfverts = FindReflexVerts(poly1)
        self.assertEqual([3,7,10], rfverts)

    def test_transition_pts(self):
        t3 = ShootRaysToReflexFromVerts(poly1, 3)
        t7 = ShootRaysToReflexFromVerts(poly1, 7)
        t10 = ShootRaysToReflexFromVerts(poly1, 10)
        ts3 = [((-67.74193548387098, 182.25806451612902), 4), ((-60.0, 190.0), 4)]
        ts7 = [((-206.18384401114204, -199.13649025069637),
        8), ((-127.36842105263163, -194.21052631578948), 8)]
        ts10 = [((207.44680851063828, 11.70212765957443), 0),
        ((209.34065934065933, 40.10989010989009), 0), ((205.3602811950791,
        56.32688927943761), 1), ((199.90439770554494, 63.76673040152964), 1),
        ((190.12048192771084, 77.10843373493977), 1)]
        self.assertEqual(ts3, t3)
        self.assertEqual(ts7, t7)
        self.assertEqual(ts10, t10)




if __name__ == '__main__':
    unittest.main()
