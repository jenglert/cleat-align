
from SimpleCV import Image
from SimpleCV import Color
from HtmlHelper import make_text_html

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



# lsm = ShoeMeasurements("L", (263, 93), (273, 202), (201, 307), (344, 305), (261, 877))
# rsm = ShoeMeasurements("R", (292, 103), (275, 241), (196, 346), (344, 355), (260, 907))

# print "left cleat area: " + str(lsm.cleat_area())
# print "right cleat area: " + str(rsm.cleat_area())
# print "  diff: {:.2%}".format((lsm.cleat_area() - rsm.cleat_area()) / lsm.cleat_area())

# print "left shoe length: " + str(lsm.shoe_length())
# print "right shoe length: " + str(rsm.shoe_length())
# print "  diff: {:.2%}".format((lsm.shoe_length() - rsm.shoe_length()) / lsm.shoe_length())

# lcr = cleat_report(lsm)
# lcr.pretty_print()
# rcr = cleat_report(rsm)
# rcr.pretty_print()

# limg = Image("corrected/1-winter-sidi-L-Step2.jpg")
# limg.drawText("Left")
# rimg = Image("corrected/1-winter-sidi-R-Step2.jpg")
# rimg.drawText("Right")

# limg = lsm.draw_on_img(limg)
# rimg = rsm.draw_on_img(rimg)

# l = limg.applyLayers()
# r = rimg.applyLayers()

# r.sideBySide(l).save("sbys.jpg")

# left_to_right_report(lcr, rcr).pretty_print()







