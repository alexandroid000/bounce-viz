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

if __name__ == '__main__':
    unittest.main()
