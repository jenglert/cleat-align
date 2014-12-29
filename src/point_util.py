import math

def subtract(a, b):
	return (a[0] - b[0], a[1] - b[1])

def middle_of_points(point_a, point_b):
	return (((point_a[0] + point_b[0]) / 2), ((point_a[1] + point_b[1]) / 2))

# Retrieves the angle between two lines (as defined by 4 total points)
def angle_between_points(point_a1, point_a2, point_b1, point_b2):
	a_tan2 = math.degrees(math.atan2(point_a2[1] - point_a1[1], point_a2[0] - point_a1[0]))
	b_tan2 = math.degrees(math.atan2(point_b2[1] - point_b1[1], point_b2[0] - point_b1[0]))

	return a_tan2 - b_tan2

def intersection_of_lines(point_a1, point_a2, point_b1, point_b2):
	# (x1-x2)(y3-y4) - (y1-y2)(x3-x4)
	d = (point_a1[0] - point_a2[0]) * (point_b1[1] - point_b2[1]) - \
	    (point_a1[1] - point_a2[1]) * (point_b1[0] - point_b2[0])

	if (d == 0.0):
		return None

	# int xi = ((x3-x4)*(x1*y2-y1*x2)-(x1-x2)*(x3*y4-y3*x4))/d;
	xi = ((point_b1[0] - point_b2[0]) * (point_a1[0] * point_a2[1] - point_a1[1] * point_a2[0]) - \
				(point_a1[0] - point_a2[0]) * (point_b1[0] * point_b2[1] - point_b1[1] * point_b2[0])) / d

    # int yi = ((y3-y4)*(x1*y2-y1*x2)-(y1-y2)*(x3*y4-y3*x4))/d;
	yi = ((point_b1[1] - point_b2[1]) * (point_a1[0] * point_a2[1] - point_a1[1] * point_a2[0]) - \
    			(point_a1[1] - point_a2[1]) * (point_b1[0] * point_b2[1] - point_b1[1] * point_b2[0])) / d

	return (xi, yi)

def intersection_of_line_and_segment(line1, line2, segment1, segment2):
	int_of_lines = intersection_of_lines(line1, line2, segment1, segment2)

	# Check whether the intersection is included in the segment
	xok = int_of_lines[0] >= min(segment1[0], segment2[0]) and \
	      int_of_lines[0] <= max(segment1[0], segment2[0])

	yok = int_of_lines[1] >= min(segment1[1], segment2[1]) and \
	      int_of_lines[1] <= max(segment1[1], segment2[1])

	if (not xok or not yok):
		return None
	return int_of_lines

# The ray goes from ray_start forever at ray_angle
def intersection_of_ray_and_segment(ray_start, ray_angle, segment1, segment2):
	# Move the point 10000000 units from ray_start, along the angle.  The #1000000 is just
	# an approximation of how long a ray is.
	second_ray_point = (ray_start[0] + math.cos(math.radians(ray_angle)) * 10000000, ray_start[1] + math.sin(math.radians(ray_angle)) * 10000000)

	int_of_lines = intersection_of_lines(ray_start, second_ray_point, segment1, segment2)
	if (int_of_lines == None):
		return None

	if (not point_lies_on_segment(int_of_lines, segment1, segment2)):
		return None

	if (not point_lies_on_segment(int_of_lines, ray_start, second_ray_point)):
		return None

	return int_of_lines


def distance_between_points(point_a, point_b):
 	return math.sqrt(math.pow((point_b[1] - point_a[1]), 2) + math.pow((point_b[0] - point_a[0]), 2))

def point_lies_on_segment(point, segmenta, segmentb):
 	# Check formula (y = mx + b)
 	slope, y_intercept = slope_and_y_intercept(segmenta, segmentb)

	# Vertical line segment check
	if (slope > 1e8):
		if (not is_close(point[0], segmenta[0])):  # X needs to equal x of segment
			return False
	else:
		if (not is_close(point[1], slope * point[0] + y_intercept)):
 			return False

 	minx, maxx = (min(segmenta[0], segmentb[0]), max(segmenta[0], segmentb[0]))
 	miny, maxy = (min(segmenta[1], segmentb[1]), max(segmenta[1], segmentb[1]))

 	xok = point[0] >= minx and point[0] <= maxx
 	yok = point[1] >= miny and point[1] <= maxy

 	return xok and yok

def slope_and_y_intercept(pointa, pointb):
	if (pointa == pointb):
		raise Exception("Unable to determine slope_and_y_intercept.  Points are equal.")

	if (pointa[0] == pointb[0]):
		# I'm not sure if this is really right... Vertical line => slope/Y is inf/inf
		return (float("inf"), float("inf"))

	if (pointa[1] == pointb[1]):
		return (0.0, pointa[1])

	# y = mx + b
	slope = (float(pointb[1]) - pointa[1]) / (pointb[0] - pointa[0])
 	y_intercept = float(pointa[1]) - (slope * pointa[0])

 	return (slope, y_intercept)

def is_close(a, b):
	return abs(a - b) < 0.0001

def average_of_points(arr):
	sumx = 0.0
	sumy = 0.0

	for a in arr:
		sumx = sumx + a[0]
		sumy = sumy + a[1]

	return (sumx / len(arr), sumy / len(arr))




