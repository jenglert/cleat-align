import random
import unittest
from point_util import *
from ellipse_best_fit import *

class EllipseBestFitTest(unittest.TestCase):

	def test_segments(self):
		ebf = EllipseBestFit((5, 5), [(0, 0), (2, 2), (1, 3)])
		self.assertEquals(ebf.segments(), [((0, 0), (2, 2)), ((2, 2), (1, 3)), ((1, 3), (0, 0))])

	def test_consistent_contour(self):
		ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])
		cc = ebf.consistent_contour(10)
		self.assertEquals(len(cc), 36)
		self.assertEquals(cc[0], (14,5))

	def test_estimated_dimensions_EASY(self):
		ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])
		width, height, angle = ebf.estimated_dimensions()
		self.assertEquals(width, 18)
		self.assertEquals(height, 10)
		self.assertEquals(angle, 0)

	def test_estimated_dimensions_ROTATE(self):
		# Not an actual elipse.  Bit messed up.  Centroid probably isn't actually 5, 5
		ebf = EllipseBestFit((5, 5), [(-1, 5), (0, 10), (5, 13), (9, 9), (12, 5), (11, -2), (6, -2), (1, 1)])
		width, height, angle = ebf.estimated_dimensions()
		self.assertEquals(width, 16.084001805391374)
		self.assertEquals(height, 11.125921694133767)
		self.assertEquals(angle, 130)

	def test_parametric_equation_points(self):
		ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])

		ellipse_points = ebf.parametric_equation_points(10)
		self.assertEquals(len(ellipse_points), 36)

		# Check some major points
		self.assert_points_close(ellipse_points[0], (14., 5.))
		self.assert_points_close(ellipse_points[18], (-4., 5.))
		self.assert_points_close(ellipse_points[9], (5., 10.))
		self.assert_points_close(ellipse_points[27], (5., 0.))

	def test_match_area_difference(self):
		ebf = EllipseBestFit((5, 5), [(-4, 5), (0, 9), (5,10), (10, 9), (14, 5), (10, 1), (5, 0), (0, 1)])
		diff = ebf.match_area_difference(10)
		self.assertTrue(abs(diff - 0.077) < 0.001)

	def test_match_area_difference_ROTATE(self):
		# Not an actual elipse.  Bit messed up.  Centroid probably isn't actually 5, 5
		ebf = EllipseBestFit((5, 5), [(-1, 5), (0, 10), (5, 13), (9, 9), (12, 5), (11, -2), (6, -2), (1, 1)])
		diff = ebf.match_area_difference(10)
		self.assertTrue(abs(diff - 0.097) < 0.001)

	def test_match_area_difference_SQUARE(self):
		ebf = EllipseBestFit((0, 0), [(-50, 0), (0, 50), (50, 0), (0, -50)])
		diff = ebf.match_area_difference(10)
		self.assertTrue(abs(diff - 0.089) < 0.001)

	def test_match_area_difference_RANDOM(self):
		ebf = EllipseBestFit((0, 0), [(-50, 0), (-20, 95), (0, 10), (20, 500), (50, 0), (20, -999), (0, 0)])
		diff = ebf.match_area_difference(10)
		self.assertTrue(abs(diff - 0.8367) < 0.001)

	def test_match_area_difference_TRIANGLE(self):
		ebf = EllipseBestFit((3, 2), [(3, 6), (6, 0), (0, 0)])
		diff = ebf.match_area_difference(10)
		self.assertTrue(abs(diff - 0.117) < 0.001)

	def assert_points_close(self, a, b):
		if (a == b): # Capture None case.
			return True

		if ((a == None) or \
			(b == None) or \
			(abs(a[0] - b[0]) > 0.001) or \
			(abs(a[1] - b[1]) > 0.001)):
			raise AssertionError("Points are not close: " + str(a) + " and " + str(b))