from html_helper import *
from cleat_report import *

class LeftRightReport:

	def __init__(self, left_sm, right_sm):
		assert left_sm.left_or_right == "L"
		assert right_sm.left_or_right == "R"

		left_cr = CleatReport(left_sm)
		right_cr = CleatReport(right_sm)

		self.rotation_difference = left_cr.rotation - right_cr.rotation
		self.width_placement_difference = left_cr.width_placement - right_cr.width_placement
		self.length_placement_difference = left_cr.length_placement - right_cr.length_placement

	def pretty_text(self):
		result = ""
		result = result + "Cleat differences: \n"
		if (self.rotation_difference > 0):
			result = result + "   - Left cleat points towards the inside of the shoe by an extra " + str(self.rotation_difference) + " degrees.\n"
		else:
			result = result + "   - Right cleat points towards the inside of the shoe by an extra " + str(self.rotation_difference) + " degrees.\n"


		if (self.width_placement_difference > 0):
			result = result + "   - The left cleat is further towards the inside of the shoe by " + str(abs(self.width_placement_difference)) + " pixels.\n"
		else:
			result = result + "   - The right cleat is further towards the inside of the shoe by " + str(abs(self.width_placement_difference)) + " pixels.\n"

		if (self.length_placement_difference > 0):
			result = result + "   - The left cleat is placed further back by " + str(abs(self.length_placement_difference)) + " pixels.\n"
		else:
			result = result + "   - The right cleat is placed further back by " + str(abs(self.length_placement_difference)) + " pixels.\n"

		return result

	def pretty_print(self):
		print(self.pretty_text())

	def pretty_html(self):
		return make_text_html(self.pretty_text())