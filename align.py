import os
from os import listdir
from os.path import isfile, join
import re
from SimpleCV import Image
import shutil
from SimpleCV import Color
from report import ShoeMeasurements, left_to_right_report, cleat_report
import itertools
from output import make_shoe_report_view_model

# Green pixel dot: RGB: 216, 255, 192 HSV: 95, 28, 100

class SampleImage:
	def __init__(self, original_file_name, index, name, foot):
		self.original_file_name = original_file_name
		self.index = index
		self.name = name
		self.foot = foot
		self.step_outputs = []

def convert_filename_to_sample_image(file_name):
	sample_regex = re.compile('(\d+)-(.*)-([LR]).[jJ][pP][gG]', re.IGNORECASE)

	match = sample_regex.match(file_name)

	if match:
		return SampleImage("sample-images/" + match.group(0), match.group(1), match.group(2), match.group(3))

def sample_images():
	sample_images = [ f for f in listdir('sample-images') if isfile(join('sample-images',f))]

	return filter(None, map(convert_filename_to_sample_image, sample_images))

def step_file_path(si, step):
	cwd = os.getcwd()
	return cwd + "/corrected/" + si.index + "-" + si.name + "-" + si.foot + "-" + str(step) + ".jpg"

def scale_down(si, image_path):
	new_file_path = step_file_path(si, 'scale-down')
	img = Image(image_path)
	img = img.resize(h=1024)
	img.save(new_file_path)
	return new_file_path

def correct_alignment(si, image_path):
	new_file_path = step_file_path(si, 'correct-alignment')
	img = Image(image_path)
	if (img.width > img.height):
		img.rotate(-90, fixed=False).save(new_file_path)
	else:
		img.save(new_file_path)
	si.step_outputs.append(new_file_path)
	return new_file_path

def dot_blobs(si, image_path):
	new_file_path = step_file_path(si, 'dot-blobs')
	img = Image(image_path)
	new_img = img.colorDistance((160, 255, 160)).invert().binarize((200, 200, 200)).invert().erode(1)
	dots = sorted(new_img.findBlobs()[-5:], key=lambda blob: blob.centroid()[1])
	for blob in dots:
		blob.draw()
		new_img.dl().circle(blob.centroid(), 5, Color.RED)

	centroids = map(lambda blob: blob.centroid(), dots)

	bottom_screws = sorted(centroids[2:4], key=lambda centroid: centroid[0])

	shoe_measurements = ShoeMeasurements(si.foot, centroids[0], centroids[1], bottom_screws[0], bottom_screws[1], centroids[4])
	new_img = shoe_measurements.draw_on_img(new_img)
	new_img.save(new_file_path)
	si.step_outputs.append(new_file_path)
	return (new_file_path, shoe_measurements)

def rotate_and_resize(si, left_sm, right_sm):
	new_file_path = step_file_path(si, 'rotate')
	img = Image(si.step_outputs[-1:][0])
	rot = right_sm.toe_heel_angle() + left_sm.toe_heel_angle()
	img = img.rotate(rot, fixed=True)
	si.step_outputs.append(new_file_path)
	img.save(new_file_path)

	scale = left_sm.shoe_length() / right_sm.shoe_length()

	new_file_path = step_file_path(si, 'scale-length')
	img = img.scale(scale)
	si.step_outputs.append(new_file_path)
	img.save(new_file_path)

	# We also resize the original file
	orig_img = Image(si.step_outputs[0])
	orig_img = orig_img.rotate(rot, fixed=True)
	orig_img = orig_img.scale(scale)

	new_file_path = step_file_path(si, 'transformed-original')
	si.step_outputs.append(new_file_path)
	orig_img.save(new_file_path)
	return new_file_path


# Make the 'corrected' file path
if os.path.isdir("corrected"):
  shutil.rmtree('corrected')
if not os.path.exists("corrected"):
  os.makedirs("corrected")

# Returns the shoe measurements for each image.
def process_image(si):
	scaled = scale_down(si, si.original_file_name)
	oriented = correct_alignment(si, scaled)
	dot_blobs_fp, sm = dot_blobs(si, oriented)
	return (si, sm)


sis = sample_images()

print "Loaded " + str(len(sis)) + " sample images"

for name, si_group in itertools.groupby(sis, key=lambda si: si.name):
	si_list = list(si_group)
	index = si_list[1].index
	print "Processing " + str(index) + "-" + name + " with items " + str(len(si_list))
	images = map(lambda si: process_image(si), si_list)
	left_si, left_sm = filter(lambda si: si[0].foot == 'L', images)[0]
	right_si, right_sm = filter(lambda si: si[0].foot == 'R', images)[0]

	# Rotate & resize
	transformed_fp = rotate_and_resize(right_si, left_sm, right_sm)

	right_blob_fp, right_sm = dot_blobs(right_si, transformed_fp)

	rimg = Image(transformed_fp)
	right_sm.draw_on_img(rimg)
	new_file_path = step_file_path(right_si, 'with-lines')
	right_si.step_outputs.append(new_file_path)
	rimg.save(new_file_path)

	limg = Image(left_si.step_outputs[0])
	left_sm.draw_on_img(limg)
	new_file_path = step_file_path(left_si, 'with-lines')
	left_si.step_outputs.append(new_file_path)
	limg.save(new_file_path)


	lr_report = left_to_right_report(cleat_report(left_sm), cleat_report(right_sm))

	vm = make_shoe_report_view_model(index, name, left_si.step_outputs, right_si.step_outputs, left_sm, right_sm, lr_report)
	vm.write_file("output.html")

print "Done!"




