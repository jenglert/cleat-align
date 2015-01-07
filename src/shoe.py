import re
import os
from shoe_measurements import ShoeMeasurements
from SimpleCV import Image
from SimpleCV import Color
from filename_utils import *
from dot_blob_finder import *

class Shoe:
	def __init__(self, original_image_path, left_or_right):
		self.original_image_path = original_image_path
		self.left_or_right = left_or_right

		self.transformations = []

		# Basic transformations
		corrected = self.correct_alignment(original_image_path)
		scaled_down = self.scale_down(corrected)
		blobs, shoe_measurements = DotBlobFinder(self, scaled_down).find()
		rotated = self.rotate(scaled_down, shoe_measurements)

		self.shoe_measurements = self.make_shoe_measurements(rotated)

	# Retrieves the last updated transformation without any circles or lines.
	def last_img_path(self):
		return self.transformations[-1:][0]

	def make_shoe_measurements(self, img_path):
		blobs, shoe_measurements = DotBlobFinder(self, img_path).find()

		return shoe_measurements

	def scale(self, img_path, scale):
		new_file_path = self.nfn('resized')
		img = Image(img_path)
		img = img.scale(scale)
		img.save(new_file_path)
		self.transformations.append(new_file_path)
		return new_file_path

	def rotate(self, img_path, shoe_measurements):
		img = Image(img_path)
		new_file_path = self.nfn('rotated')
		img = img.rotate(shoe_measurements.toe_heel_angle(), point=shoe_measurements.cleat_length_intersection())
		self.transformations.append(new_file_path)
		img.save(new_file_path)
		return new_file_path

	def scale_down(self, img_path):
		new_file_path = self.nfn('scale-down')
		img = Image(img_path)
		img = img.resize(h=1024)
		img.save(new_file_path)
		return new_file_path

	def correct_alignment(self, img_path):
		new_file_path = self.nfn('correct-alignment')
		img = Image(img_path)
		if (img.width > img.height):
			img.rotate(-90, fixed=False).save(new_file_path)
		else:
			img.save(new_file_path)
		self.transformations.append(new_file_path)
		return new_file_path

	def nfn(self, desc):
		return step_file_name(self.original_image_path, desc)

print "Right"
shoel = Shoe("/web/cleat-align/corrected/1-mavic-L-rotated.jpg", "L")
print shoel.shoe_measurements.centered_coordinates().pretty_print()
print "Left"
shoer = Shoe("/web/cleat-align/corrected/1-mavic-R-resized.jpg", "R")
print shoer.shoe_measurements.centered_coordinates().pretty_print()