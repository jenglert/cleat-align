import random
import unittest
from point_util import *
from ellipse_best_fit import *

class EllipseBestFitTest(unittest.TestCase):

	# def test_segments(self):
	# 	ebf = EllipseBestFit((5, 5), [(0, 0), (2, 2), (1, 3)])
	# 	self.assertEquals(ebf.segments, [((0, 0), (2, 2)), ((2, 2), (1, 3)), ((1, 3), (0, 0))])

	# def test_consistent_contour(self):
	# 	ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])
	# 	cc = ebf.consistent_contour(10)
	# 	self.assertEquals(len(cc), 36)
	# 	self.assertEquals(cc[0], (14,5))

	# def test_estimated_dimensions_EASY(self):
	# 	ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])
	# 	width, height, angle = ebf.estimated_dimensions()
	# 	self.assertEquals(width, 18)
	# 	self.assertEquals(height, 10)
	# 	self.assertEquals(angle, 0)

	# def test_estimated_dimensions_ROTATE(self):
	# 	# Not an actual elipse.  Bit messed up.  Centroid probably isn't actually 5, 5
	# 	ebf = EllipseBestFit((5, 5), [(-1, 5), (0, 10), (5, 13), (9, 9), (12, 5), (11, -2), (6, -2), (1, 1)])
	# 	width, height, angle = ebf.estimated_dimensions()
	# 	self.assertEquals(width, 16.084001805391374)
	# 	self.assertEquals(height, 11.125921694133767)
	# 	self.assertEquals(angle, 130)

	# def test_parametric_equation_points(self):
	# 	ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])

	# 	ellipse_points = ebf.parametric_equation_points(10)
	# 	self.assertEquals(len(ellipse_points), 36)

	# 	# Check some major points
	# 	self.assert_points_close(ellipse_points[0], (14., 5.))
	# 	self.assert_points_close(ellipse_points[18], (-4., 5.))
	# 	self.assert_points_close(ellipse_points[9], (5., 10.))
	# 	self.assert_points_close(ellipse_points[27], (5., 0.))

	# def test_match_area_difference(self):
	# 	ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])
	# 	diff = ebf.match_area_difference()
	# 	self.assertTrue(abs(diff - 0.077) < 0.001)

	# def test_match_area_difference_ROTATE(self):
	# 	# Not an actual elipse.  Bit messed up.  Centroid probably isn't actually 5, 5
	# 	ebf = EllipseBestFit((5, 5), [(-1, 5), (0, 10), (5, 13), (9, 9), (12, 5), (11, -2), (6, -2), (1, 1)])
	# 	diff = ebf.match_area_difference()
	# 	self.assertTrue(abs(diff - 0.097) < 0.001)

	# def test_match_area_difference_SQUARE(self):
	# 	ebf = EllipseBestFit((0, 0), [(-50, 0), (0, 50), (50, 0), (0, -50)])
	# 	diff = ebf.match_area_difference()
	# 	self.assertTrue(abs(diff - 0.089) < 0.001)

	# def test_match_area_difference_RANDOM(self):
	# 	ebf = EllipseBestFit((0, 0), [(-50, 0), (-20, 95), (0, 10), (20, 500), (50, 0), (20, -999), (0, 0)])
	# 	diff = ebf.match_area_difference()
	# 	self.assertTrue(abs(diff - 0.8367) < 0.001)

	# def test_match_area_difference_TRIANGLE(self):
	# 	ebf = EllipseBestFit((3, 2), [(3, 6), (6, 0), (0, 0)])
	# 	diff = ebf.match_area_difference()
	# 	self.assertTrue(abs(diff - 0.117) < 0.001)

	def test_match_area_difference_FROM_SHOE(self):
		ebf = EllipseBestFit((250.51300401466224, 202.31768196893), [(244, 175), (243, 176), (240, 176), (239, 177), (238, 177), (237, 178), (236, 178), (235, 179), (234, 179), (233, 180), (232, 180), (231, 181), (230, 181), (227, 184), (226, 184), (222, 188), (222, 189), (221, 190), (221, 191), (219, 193), (219, 196), (218, 197), (218, 199), (217, 200), (217, 208), (218, 209), (218, 211), (219, 212), (219, 213), (221, 215), (221, 216), (223, 218), (223, 219), (225, 221), (226, 221), (229, 224), (230, 224), (231, 225), (232, 225), (234, 227), (235, 227), (236, 228), (237, 228), (238, 229), (256, 229), (257, 228), (260, 228), (261, 227), (265, 227), (266, 226), (267, 226), (268, 225), (269, 225), (270, 224), (271, 224), (278, 217), (279, 217), (279, 216), (281, 214), (281, 213), (282, 212), (282, 211), (283, 210), (283, 208), (284, 207), (284, 206), (285, 205), (284, 204), (284, 195), (283, 194), (283, 193), (282, 192), (282, 191), (273, 182), (272, 182), (270, 180), (269, 180), (268, 179), (267, 179), (266, 178), (265, 178), (264, 177), (262, 177), (261, 176), (259, 176), (258, 175)])
		diff = ebf.match_area_difference()
		self.assertTrue(abs(diff - 0.117) < 0.001)

	def assert_points_close(self, a, b):
		if (a == b): # Capture None case.
			return True

		if ((a == None) or \
			(b == None) or \
			(abs(a[0] - b[0]) > 0.001) or \
			(abs(a[1] - b[1]) > 0.001)):
			raise AssertionError("Points are not close: " + str(a) + " and " + str(b))