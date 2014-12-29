import random
import unittest
from point_util import *

class PointUtilTest(unittest.TestCase):

    def test_intersection_of_lines(self):
        cross_int = intersection_of_lines((2,0), (2, 20), (-10, 10), (10, 10))
        self.assertEqual(cross_int, (2, 10))

        x_int = intersection_of_lines((-3,-1), (1, 3), (-3, 3), (1, -1))
        self.assertEqual(x_int, (-1, 1))

        no_int = intersection_of_lines((1, 1), (5, 5), (-1, -1), (-1, 3))
        self.assertEqual(no_int, (-1, -1))

    def test_intersection_of_line_and_segment(self):
        cross_int = intersection_of_line_and_segment((2,0), (2, 20), (-10, 10), (10, 10))
        self.assertEqual(cross_int, (2, 10))

        x_int = intersection_of_line_and_segment((-3,-1), (1, 3), (-3, 3), (1, -1))
        self.assertEqual(x_int, (-1, 1))

        no_int = intersection_of_line_and_segment((-1, -1), (-1, 3), (1, 1), (5, 5))
        self.assertEqual(no_int, None)

        # Depending on which is the segment and which is the line, we will have success.
        no_int = intersection_of_line_and_segment((1, 1), (5, 5), (-1, -1), (-1, 3))
        self.assertEqual(no_int, (-1, -1))

    def test_slope_and_y_intercept(self):
		s, y = slope_and_y_intercept((0, 0), (1, 1))
		self.assertEqual(s, 1)
		self.assertEqual(y, 0)

		s, y = slope_and_y_intercept((1, 3), (2, 5))
		self.assertEquals(s, 2)
		self.assertEquals(y, 1)

		s, y = slope_and_y_intercept((1, 3), (1, 5))
		self.assertEquals(s, float("inf"))
		self.assertEquals(y, float("inf"))

		s, y = slope_and_y_intercept((1, 3), (3, 3))
		self.assertEquals(s, 0)
		self.assertEquals(y, 3)

    def test_point_lies_on_segment(self):
    	self.assertTrue(point_lies_on_segment((1, 1), (0, 0), (2, 2)))
    	self.assertFalse(point_lies_on_segment((1, 2), (0, 0), (2, 2)))
    	self.assertFalse(point_lies_on_segment((5, 5), (0, 0), (2, 2)))
    	self.assertTrue(point_lies_on_segment((1, 1), (2, 2), (-1, -1)))
    	self.assertTrue(point_lies_on_segment((5, 2), (2, 2), (6, 2)))
    	self.assertFalse(point_lies_on_segment((7, 2), (2, 2), (6, 2)))
    	self.assertTrue(point_lies_on_segment((2, 4), (2, 2), (2, 6)))
    	self.assertTrue(point_lies_on_segment((2, 2), (2, 2), (2, 6)))
    	self.assertFalse(point_lies_on_segment((2, 7), (2, 2), (2, 6)))

    	self.assertTrue(point_lies_on_segment((1.0000000000000002, 2.0), (0, 2), (2, 2)))
    	self.assertTrue(point_lies_on_segment((1.0000000000000002, 2.0), (1, 1), (1.0000000006123233, 10000001.0)))

        self.assertTrue(point_lies_on_segment((9.811858122146667, 9.037628375570668), (5, 10), (10, 9)))

    def test_intersection_of_ray_and_segment(self):
    	self.assert_points_close(intersection_of_ray_and_segment((0, 0), 45, (4, 3), (4, 5)), (4, 3.9999))
    	self.assert_points_close(intersection_of_ray_and_segment((0, 0), 45, (4, 0), (4, 3)), None)
    	self.assert_points_close(intersection_of_ray_and_segment((1, 1), 90, (0, 2), (2, 2)), (1, 2))
    	self.assertFalse(intersection_of_ray_and_segment((1, 3), 90, (0, 2), (2, 2)))

    	# Quadrant II
    	self.assertTrue(intersection_of_ray_and_segment((0, 0), 135, (-4, 3), (-4, 5)))
    	self.assertFalse(intersection_of_ray_and_segment((0, 0), 315, (-4, 3), (-4, 3.5)))

    	# Quadrant III
    	self.assertTrue(intersection_of_ray_and_segment((0, 0), 225, (-4, -3), (-4, -5)))
    	self.assertFalse(intersection_of_ray_and_segment((0, 0), 315, (-4, -3), (-4, -3.5)))

    	# Quadrant IV
    	self.assertTrue(intersection_of_ray_and_segment((0, 0), 315, (4, -3), (4, -5)))
    	self.assertFalse(intersection_of_ray_and_segment((0, 0), 315, (4, 3), (4, 5)))

        self.assertTrue(intersection_of_ray_and_segment((5, 5), 40, (5, 10), (10, 9)))

    def test_average_of_points(self):
        points = [(0, 0), (1.5, 1.5), (2.5, 5)]
        avg_pnt = average_of_points(points)
        self.assert_points_close(avg_pnt, ((4/3.0), (6.5/3)))


    def assert_points_close(self, a, b):
    	if (a == b): # Capture None case.
    		return True

    	if ((a == None) or \
    		(b == None) or \
    		(abs(a[0] - b[0]) > 0.001) or \
    		(abs(a[1] - b[1]) > 0.001)):
			raise AssertionError("Points are not close: " + str(a) + " and " + str(b))


