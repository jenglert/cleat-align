from shoe import *
from filename_utils import *
from left_right_report import *

# A pair step represents a left and right shoe image.  Based on
# an original image, there may be multiple pair steps necessary
# to get to the final output.
class PairStep:
	def __init__(self, left_img_path, right_img_path):
		self.left_img_path = left_img_path
		self.right_img_path = right_img_path

		self.left_shoe = Shoe(left_img_path, "L")
		self.right_shoe = Shoe(right_img_path, "R")

		self.resize(self.left_shoe.shoe_measurements, self.right_shoe.shoe_measurements)

	def resize(self, left_sm, right_sm):
		if (left_sm.shoe_length() > right_sm.shoe_length()):
			scale = left_sm.shoe_length() / right_sm.shoe_length()
			self.right_shoe.scale(self.right_shoe.last_img_path(), scale)
		else:
			scale = right_sm.shoe_length() / left_sm.shoe_length()
			self.left_shoe.scale(self.left_shoe.last_img_path(), scale)

	def report(self):
		left_sm = self.left_shoe.make_shoe_measurements(self.left_shoe.last_img_path())
		right_sm = self.right_shoe.make_shoe_measurements(self.right_shoe.last_img_path())

		lr_report = LeftRightReport(left_sm, right_sm)
		lr_report.pretty_print()

		print ""

		left_img = Image(self.left_shoe.last_img_path())
		left_img = left_sm.draw_on_img(left_img)
		left_img.drawText("Left", 50, 50, Color.WHITE, 30)
		left_img = left_img.applyLayers()

		right_img = Image(self.right_shoe.last_img_path())
		right_img = right_sm.draw_on_img(right_img)
		right_img.drawText("Right", 50, 50, Color.WHITE, 30)
		right_img = right_img.applyLayers()

		max_width = max(left_img.width, right_img.width)
		max_height = max(left_img.height, right_img.height)

		left_img = left_img.embiggen((max_width, max_height))
		right_img = right_img.embiggen((max_width, max_height))

		side_by_side = left_img.sideBySide(right_img, scale=True)
		side_by_side.save("side_by_side.jpg")

		print "Final comparison available at " + side_by_side.filename

ps = PairStep("/web/cleat-align/sample-images/1-mavic-L.JPG", "/web/cleat-align/sample-images/1-mavic-R.JPG")
ps.report()


