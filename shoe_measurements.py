from SimpleCV import Color
from point_util import *

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

	# The area logically included in the toe, left screw, right screw, heel object
	# I'm not sure if this area is valuable.
	def area(self):
		left_area = (distance_between_points(self.tip, self.left_screw) * distance_between_points(self.left_screw, self.heel)) / 2
		right_area = (distance_between_points(self.tip, self.right_screw) * distance_between_points(self.right_screw, self.heel)) / 2

		return left_area + right_area

	def toe_heel_angle(self):
		# Effectively the angle between the toe-heel and the horizon
		return angle_between_points(self.tip, self.heel, (0, 0), (0, 100))

	def cleat_length_intersection(self):
		return intersection_of_lines(self.tip, self.heel, self.left_screw, self.right_screw)

	def draw_on_img(self, img):
		img.dl().line(self.tip, self.heel, Color.RED, 2)
		img.dl().line(self.left_screw, self.right_screw, Color.RED, 2)

		img.dl().line(self.left_screw, self.top_screw, Color.RED, 2)
		ltmidpoint = middle_of_points(self.left_screw, self.top_screw)
		img.dl().text("{:.0f}".format(distance_between_points(self.left_screw, self.top_screw)), ltmidpoint, Color.WHITE)

		img.dl().line(self.right_screw, self.top_screw, Color.RED, 2)
		rtmidpoint = middle_of_points(self.right_screw, self.top_screw)
		img.dl().text("{:.0f}".format(distance_between_points(self.right_screw, self.top_screw)), rtmidpoint, Color.WHITE)

		cleatmidpoint = middle_of_points(self.right_screw, self.left_screw)
		img.dl().text("{:.0f}".format(distance_between_points(self.right_screw, self.left_screw)), cleatmidpoint, Color.WHITE)

		lengthmidpoint = middle_of_points(self.tip, self.heel)
		img.dl().text("{:.0f}".format(distance_between_points(self.tip, self.heel)), lengthmidpoint, Color.WHITE)

		img.dl().line(self.top_screw, middle_of_points(self.left_screw, self.right_screw), Color.RED, 2)
		return img

	def cleat_area(self):
		return distance_between_points(self.top_screw, self.left_screw) * distance_between_points(self.top_screw, self.right_screw)

	def shoe_length(self):
		return distance_between_points(self.tip, self.heel)

	def cleat_width(self):
		return distance_between_points(self.left_screw, self.right_screw)