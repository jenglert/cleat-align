import math

def middle_of_points(point_a, point_b):
	return (((point_a[0] + point_b[0]) / 2), ((point_a[1] + point_b[1]) / 2))

# Retrieves the angle between two lines (as defined by 4 total points)
def angle_between_points(point_a1, point_a2, point_b1, point_b2):
	a_tan2 = math.degrees(math.atan2(point_a2[1] - point_a1[1], point_a2[0] - point_a1[0]))
	b_tan2 = math.degrees(math.atan2(point_b2[1] - point_b1[1], point_b2[0] - point_b1[0]))

	return a_tan2 - b_tan2

def intersection_of_lines(point_a1, point_a2, point_b1, point_b2):
	slope_of_a = float(point_a2[1] - point_a1[1])/float(point_a2[0] - point_a1[0])
	slope_of_b = float(point_b2[1] - point_b1[1])/float(point_b2[0] - point_b1[0])
	intercept_of_a = point_a1[1] - slope_of_a * point_a1[0]
	intercept_of_b = point_b1[1] - slope_of_b * point_b1[0]

	# m1x + b1 = m2x + b2
	# (m1 - m2)x = b2 - b1
	intersection_x = (intercept_of_b - intercept_of_a) / (slope_of_a - slope_of_b)
	intersection_y = slope_of_a * intersection_x + intercept_of_a
	return (intersection_x, intersection_y)

def distance_between_points(point_a, point_b):
 	return math.sqrt(math.pow((point_b[1] - point_a[1]), 2) + math.pow((point_b[0] - point_a[0]), 2))