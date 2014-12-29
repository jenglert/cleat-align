from point_util import *

# Rotation is defined by
class CleatReport:

	def __init__(self, sm):
		self.left_or_right = sm.left_or_right
		mid_point_of_bottom_screws = middle_of_points(sm.left_screw, sm.right_screw)

		# Angle represents angle from tip-heel line to cleat angle, measured in degrees.  Positive
		# angles indicate that the cleat is pointed towards in inside of the shoe
		if (sm.left_or_right == "R"):
			self.rotation = angle_between_points(sm.top_screw, mid_point_of_bottom_screws, sm.tip, sm.heel)
		else:
			self.rotation = angle_between_points(sm.tip, sm.heel, sm.top_screw, mid_point_of_bottom_screws)

		heel_cleat_intersection = intersection_of_lines(sm.tip, sm.heel, sm.left_screw, sm.right_screw)

		left_of_middle = distance_between_points(sm.left_screw, heel_cleat_intersection)
		right_of_middle = distance_between_points(sm.right_screw, heel_cleat_intersection)

		if sm.left_or_right == "R":
			self.width_placement = right_of_middle - left_of_middle
		else:
			self.width_placement = left_of_middle - right_of_middle

		self.length_placement = distance_between_points(sm.tip, heel_cleat_intersection) - distance_between_points(heel_cleat_intersection, sm.heel)

	def pretty_print(self):
		print "Cleat alignment: " + self.left_or_right
		print "   rotation: " + str(self.rotation)
		print "   width_placement: " + str(self.width_placement)
		print "   length_placement: " + str(self.length_placement)