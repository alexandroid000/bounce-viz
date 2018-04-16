#! /usr/bin/env python

import unittest
from geom_utils import *
from maps import *

class TestGeomUtils(unittest.TestCase):

    def setUp(self):
        self.p1 = [ 10.0,   0.0]
        self.p2 = [-10.0,   0.0]
        self.p3 = [  0.0,  10.0]
        self.p4 = [  0.0, -10.0]

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

if __name__ == '__main__':
    unittest.main()
