import math
from SimpleCV import Image
from SimpleCV import Color

# Rotation is defined by
class IndividualSideReport:
	# Rotation angle represents angle from tip-heel line to cleat angle, measured in degrees.  Positive
	# angles indicate that the cleat is pointed towards in inside of the shoe
	def __init__(self, left_or_right, rotation, width_placement, length_placement):
		self.left_or_right = left_or_right
		self.rotation = rotation
		self.width_placement = width_placement
		self.length_placement = length_placement

	def pretty_print(self):
		print "Cleat alignment: " + self.left_or_right
		print "   rotation: " + str(self.rotation)
		print "   width_placement: " + str(self.width_placement)
		print "   length_placement: " + str(self.length_placement)

class LeftToRightReport:
	def __init__(self, rotation_difference, width_placement_difference, length_placement_difference):
		self.rotation_difference = rotation_difference
		self.width_placement_difference = width_placement_difference
		self.length_placement_difference = length_placement_difference

	def pretty_print(self):
		print "Cleat differences: "
		if (self.rotation_difference > 0):
			print "   - Left cleat points towards the inside of the shoe by an extra " + str(self.rotation_difference) + " degrees."
		else:
			print "   - Right cleat points towards the inside of the shoe by an extra " + str(self.rotation_difference) + " degrees."


		if (self.width_placement_difference > 0):
			print "   - The left cleat is further towards the inside of the shoe by " + str(self.width_placement_difference) + " pixels."
		else:
			print "   - The right cleat is further towards the inside of the shoe by " + str(self.width_placement_difference) + " pixels."

		if (self.length_placement_difference > 0):
			print "   - The left cleat is placed further back by " + str(self.length_placement_difference) + " pixels."
		else:
			print "   - The right cleat is placed further back by " + str(self.length_placement_difference) + " pixels."


class ShoeMeasurements:

	def __init__(self, left_or_right, tip, top_screw, left_screw, right_screw, heel):

		# Sanity checks - Make sure the cleat screws make sense.
		assert top_screw[1] < left_screw[1]
		assert top_screw[0] < right_screw[1]
		assert top_screw[0] < right_screw[0]
		assert top_screw[0] > left_screw[0]

		# Make sure the tip is above the heel
		assert tip[1] < heel[1]

		self.left_or_right = left_or_right
		self.tip = tip
		self.top_screw = top_screw
		self.left_screw = left_screw
		self.right_screw = right_screw
		self.heel = heel

	def draw_on_img(self, img):
		img.dl().line(self.tip, self.heel, Color.RED)
		img.dl().line(self.left_screw, self.right_screw, Color.RED)

		img.dl().line(self.left_screw, self.top_screw, Color.RED)
		ltmidpoint = middle_of_points(self.left_screw, self.top_screw)
		img.dl().text("{:.0f}".format(distance_between_points(self.left_screw, self.top_screw)), ltmidpoint)

		img.dl().line(self.left_screw, self.top_screw, Color.RED)
		rtmidpoint = middle_of_points(self.left_screw, self.top_screw)
		img.dl().text("{:.0f}".format(distance_between_points(self.right_screw, self.top_screw)), trmidpoint)

		img.dl().line(self.top_screw, middle_of_points(self.left_screw, self.right_screw), Color.RED)
		return img

	def cleat_area(self):
		return distance_between_points(self.top_screw, self.left_screw) * distance_between_points(self.top_screw, self.right_screw)

	def shoe_length(self):
		return distance_between_points(self.tip, self.heel)

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

# sm - ShoeMeasurements class
def cleat_report(sm):
	mid_point_of_bottom_screws = middle_of_points(sm.left_screw, sm.right_screw)

	# Angle represents angle from tip-heel line to cleat angle, measured in degrees.  Positive
	# angles indicate that the cleat is pointed towards in inside of the shoe
	if (sm.left_or_right == "R"):
		cleat_angle = angle_between_points(sm.top_screw, mid_point_of_bottom_screws, sm.tip, sm.heel)
	else:
		cleat_angle = angle_between_points(sm.tip, sm.heel, sm.top_screw, mid_point_of_bottom_screws)

	heel_cleat_intersection = intersection_of_lines(sm.tip, sm.heel, sm.left_screw, sm.right_screw)

	left_of_middle = distance_between_points(sm.left_screw, heel_cleat_intersection)
	right_of_middle = distance_between_points(sm.right_screw, heel_cleat_intersection)

	if sm.left_or_right == "R":
		lr_alignment = right_of_middle - left_of_middle
	else:
		lr_alignment = left_of_middle - right_of_middle

	fb_alignment = distance_between_points(sm.tip, heel_cleat_intersection) - distance_between_points(heel_cleat_intersection, sm.heel)

	return IndividualSideReport(sm.left_or_right, cleat_angle, lr_alignment, fb_alignment)

def left_to_right_report(left, right):
	assert left.left_or_right == "L"
	assert right.left_or_right == "R"

	# Return in pixels for now....
	return LeftToRightReport(left.rotation - right.rotation, left.width_placement - right.width_placement, left.length_placement - right.length_placement)

lsm = ShoeMeasurements("L", (263, 93), (273, 202), (201, 307), (344, 305), (261, 877))
rsm = ShoeMeasurements("R", (292, 103), (275, 241), (196, 346), (344, 355), (260, 907))

print "left cleat area: " + str(lsm.cleat_area())
print "right cleat area: " + str(rsm.cleat_area())
print "  diff: {:.2%}".format((lsm.cleat_area() - rsm.cleat_area()) / lsm.cleat_area())

print "left shoe length: " + str(lsm.shoe_length())
print "right shoe length: " + str(rsm.shoe_length())
print "  diff: {:.2%}".format((lsm.shoe_length() - rsm.shoe_length()) / lsm.shoe_length())

lcr = cleat_report(lsm)
lcr.pretty_print()
rcr = cleat_report(rsm)
rcr.pretty_print()

limg = Image("corrected/1-winter-sidi-L-Step2.jpg")
limg.drawText("Left")
rimg = Image("corrected/1-winter-sidi-R-Step2.jpg")
rimg.drawText("Right")

limg = lsm.draw_on_img(limg)
rimg = rsm.draw_on_img(rimg)

l = limg.applyLayers()
r = rimg.applyLayers()

r.sideBySide(l).save("sbys.jpg")

left_to_right_report(lcr, rcr).pretty_print()







