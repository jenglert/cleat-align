from point_util import *
import numpy as np
from math import cos, sin

class EllipseBestFit:

	def __init__(self, centroid, contour_points):
		self.centroid = centroid
		self.contour_points = contour_points

	def area(self):
		(width, height, rotation) = self.estimated_dimensions()
		return math.pi * width * height

	# The match area difference will be 0 if it is a perfect ellipse.  The number
	# will never be one.  Realistically, pretty much any shape will not be 1.  For
	# example, a triangle will be about 0.11.  The formula here attempts to normalize
	# things well.
	def chance_is_elipse(self):
		area_diff = self.match_area_difference(10)
		if (area_diff < 0.1):
			return 0.9 + (0.1 - area_diff)
		if (area_diff < 0.2):
			return 0.8 + ((0.2 - area_diff) / 0.2) * 0.1
		if (area_diff < 0.3):
			return 0.7 + ((0.3 - area_diff) / 0.3) * 0.1
		else:
			return 0.

	# Computes the difference in area (per slice) between the actual
	# contour and the elipse formula we made to match the contour.
	def match_area_difference(self, angle_step):
		contour_points = self.consistent_contour(angle_step)
		ellipse_points = self.parametric_equation_points(angle_step)
		section_cnt = 360 / angle_step

		drop_distance = 0.

		for i in range(0, 36):
			# The effective area between the ellipse formula and the contour
			# We assume each section is a circle
			formula_radius = distance_between_points(ellipse_points[i], self.centroid)
			contour_radius = distance_between_points(contour_points[i], self.centroid)
			formula_area = (math.pi * math.pow(formula_radius, 2)) / section_cnt
			contour_area = (math.pi * math.pow(contour_radius, 2)) / section_cnt

			area_difference = abs(formula_area - contour_area)

			drop_distance = drop_distance + area_difference

		return drop_distance / self.area()

	def parametric_equation_points(self, angle_step):
		points = []

		(width, height, rotation) = self.estimated_dimensions()
		r_rad = math.radians(rotation)

		center = np.array([[self.centroid[0]], [self.centroid[1]]])
		rotation = np.array([                     \
			[cos(r_rad), -1 * sin(r_rad)],        \
			[sin(r_rad), cos(r_rad)]              \
		])

		for ang in range(0, 360, 10):
			dim = np.array([[width / 2 * cos(math.radians(ang))], [height / 2 * sin(math.radians(ang))]])

			point = np.add(center, np.dot(rotation, dim))

			points.append((point[0][0], point[1][0]))

		return points


	# Retrieves a tuple of (width, height, rotation CCW)
	def estimated_dimensions(self):
		# This should ensure that we have a number of points in the consistent
		# contour that is divisible by 4.
		angle_step = 10
		cc = self.consistent_contour(angle_step)

		biggest_contour_distance = -1
		biggest_contour_index = -1

		cc_len = len(cc)
		quarter_cc_len = len(cc) / 4
		half_cc_len = len(cc) / 2

		# Iterate over half the list of points and match points across from each other.
		for i in range(0, half_cc_len):
			dist = distance_between_points(cc[i], cc[i + half_cc_len])

			if (dist > biggest_contour_distance):
				biggest_contour_distance = dist
				biggest_contour_index = i


		angle = angle_step * biggest_contour_index
		width = biggest_contour_distance
		h_point_a, h_point_b = (cc[biggest_contour_index + quarter_cc_len], \
			                    cc[(biggest_contour_index + half_cc_len + quarter_cc_len) % cc_len])
		height = distance_between_points(h_point_a, h_point_b)

		return (width, height, angle)


	# Go around the centroid, in n degree increments, recording the
	# points a ray from the centroid at the degree increment intersects
	# the contour.
	#
	# In the event the ray intersects the contour multiple times, record
	# the average
	def consistent_contour(self, angle_step):
		consistent_contour = []
		for ang in range(0, 360, angle_step):
			intersections = map(lambda segment: intersection_of_ray_and_segment(self.centroid, ang, segment[0], segment[1]), \
				 self.segments())

			intersections = filter(lambda segment: segment != None, intersections)

			if (len(intersections) == 0):
				for segment in self.segments():
					print "S:" + str(segment)
				raise Exception("Unable to find intersection from " + str(self.centroid) + " at angle " + str(ang))

			consistent_contour.append(average_of_points(intersections))

		return consistent_contour

	# Iterate over every element in the contour as pairs of points.
	def segments(self):
		segments = []
		for idx, c in enumerate(self.contour_points):
			if (idx + 1 < len(self.contour_points)):
				segments.append((c, self.contour_points[idx + 1]))
			else:
				segments.append((c, self.contour_points[0]))

		return segments