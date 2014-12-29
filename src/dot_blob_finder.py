from filename_utils import *
from SimpleCV import Image
from SimpleCV import Color
from point_util import *
from shoe_measurements import ShoeMeasurements

class DotBlobFinder:

	def __init__(self, shoe, img_path):
		self.shoe = shoe
		self.img_path = img_path

	def find(self):
		new_file_path = self.nfn('dot-blobs')
		img = Image(self.img_path)
		new_img = img.colorDistance((160, 255, 160)).invert().binarize((200, 200, 200)).invert().erode(1)
		for blob in new_img.findBlobs():
			self.chance_blob_is_circular(blob)

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

	def chance_blob_is_circular(self, blob):
		mean = blob.radius()
		stddev = self.radius_diff_std_dev(blob)
		relt_std_dev = stddev / mean

		# print "mean: " + str(mean) + "\tstddev:" + str(stddev) + "\trltstddev:" + str(relt_std_dev) + "\tarea:" + str(blob.area()) + "\trect:" + str(rect.)

	# Finds points around a circle (every 10 degrees) that intersect the blob's contour.
	def points_around_elipse(self, blob):
		True


	# We know the average radius of each point in the blob.  This represents the standard deviation
	# of the actual points compared to the average radius.
	def radius_diff_std_dev(self, blob):
		centroid = blob.centroid()
		avg_radius = blob.radius()

		diffs = map(lambda cp: pow(distance_between_points(cp, centroid) - avg_radius, 2), blob.contour())

		return pow(sum(diffs) / len(diffs), 0.5)

	def avg(self, list):
		return sum(list) / float(len(list))

	def nfn(self, desc):
		return step_file_name(self.shoe.original_image_path, desc)

