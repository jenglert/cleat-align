import re
import os
from shoe_measurements import ShoeMeasurements
from SimpleCV import Image
from SimpleCV import Color
from filename_utils import *

class Shoe:
	def __init__(self, original_image_path, left_or_right):
		self.original_image_path = original_image_path
		self.left_or_right = left_or_right

		self.transformations = []

		# Basic transformations
		corrected = self.correct_alignment(original_image_path)
		scaled_down = self.scale_down(corrected)
		blobs, shoe_measurements = self.dot_blobs(scaled_down)
		rotated = self.rotate(scaled_down, shoe_measurements)

		self.shoe_measurements = self.make_shoe_measurements(rotated)

	# Retrieves the last updated transformation without any circles or lines.
	def last_img_path(self):
		return self.transformations[-1:][0]

	def make_shoe_measurements(self, img_path):
		blobs, shoe_measurements = self.dot_blobs(img_path)

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

	def dot_blobs(self, img_path):
		new_file_path = self.nfn('dot-blobs')
		img = Image(img_path)
		new_img = img.colorDistance((160, 255, 160)).invert().binarize((200, 200, 200)).invert().erode(1)
		dots = sorted(new_img.findBlobs()[-5:], key=lambda blob: blob.centroid()[1])
		for blob in dots:
			blob.draw()
			new_img.dl().circle(blob.centroid(), 5, Color.RED)

		centroids = map(lambda blob: blob.centroid(), dots)

		bottom_screws = sorted(centroids[2:4], key=lambda centroid: centroid[0])

		shoe_measurements = ShoeMeasurements(self.left_or_right, centroids[0], centroids[1], bottom_screws[0], bottom_screws[1], centroids[4])
		new_img = shoe_measurements.draw_on_img(new_img)
		new_img.save(new_file_path)
		return (new_file_path, shoe_measurements)

	def nfn(self, desc):
		return step_file_name(self.original_image_path, desc)


shoel = Shoe("/web/cleat-align/sample-images/1-mavic-L.JPG", "L")
shoer = Shoe("/web/cleat-align/sample-images/1-mavic-R.JPG", "R")