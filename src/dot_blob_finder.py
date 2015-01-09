from filename_utils import *
from SimpleCV import Image
from SimpleCV import Color
from point_util import *
from shoe_measurements import ShoeMeasurements
from ellipse_best_fit import *

class DotBlobFinder:

	def __init__(self, shoe, img_path):
		self.shoe = shoe
		self.img_path = img_path

	def find(self):
		new_file_path = self.nfn('dot-blobs')
		img = Image(self.img_path)
		new_img = img.colorDistance((160, 255, 160)).invert().binarize((200, 200, 200)).invert().erode(1)
		for blob in new_img.findBlobs():
			print str(blob) + " --> " + str(self.chance_blob_is_an_ellipse(blob))

		dots = sorted(new_img.findBlobs()[-5:], key=lambda blob: blob.centroid()[1])
		for blob in dots:
			blob.draw()
			new_img.dl().circle(blob.centroid(), 5, Color.RED)

		centroids = map(lambda blob: blob.centroid(), dots)

		bottom_screws = sorted(centroids[2:4], key=lambda centroid: centroid[0])

		shoe_measurements = ShoeMeasurements(self.shoe.left_or_right, centroids[0], centroids[1], bottom_screws[0], bottom_screws[1], centroids[4])
		new_img = shoe_measurements.draw_on_img(new_img)
		new_img.save(new_file_path)
		return (new_file_path, shoe_measurements)

	def chance_blob_is_an_ellipse(self, blob):
		# Skip blobs that do not have their centroid within the blob.
		if (blob.distanceFrom(blob.centroid()) > blob.radius()):
			return 0.

		ebf = EllipseBestFit(blob.centroid(), blob.contour())
		img = Image(self.img_path)
		ebf.show_best_fit_model(img)
		return ebf.chance_is_elipse()


	def nfn(self, desc):
		return step_file_name(self.shoe.original_image_path, desc)

