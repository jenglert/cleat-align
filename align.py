import os
from os import listdir
from os.path import isfile, join
import re
from airspeed import CachingFileLoader
from SimpleCV import Image
import shutil

def load_cache(contents):
	loader = CachingFileLoader("html")
	template = loader.load_template("layout.html")
	return template.merge(contents, loader=loader)

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

def write_file(file_path, contents):
	f = open(file_path, "w")
	f.write(contents)
	f.close()

def step_file_path(si, step_number):
	cwd = os.getcwd()
	return cwd + "/corrected/" + si.index + "-" + si.name + "-" + si.foot + "-Step" + str(step_number) + ".jpg"

def scale_down(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.step_outputs[len(si.step_outputs) - 1])
	img = img.resize(h=1024)
	img.save(new_file_path)
	return new_file_path

def correct_alignment(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.original_file_name) 	
	if (img.width > img.height):
		img.rotate(-90, fixed=False).save(new_file_path)
	else:
		img.save(new_file_path)
	return new_file_path

def find_corners(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.step_outputs[len(si.step_outputs) - 1])
	fs = img.findCorners()
	if (fs != None):
		fs.draw()
	img.save(new_file_path)
	return new_file_path

def find_circles(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.step_outputs[len(si.step_outputs) - 1])
	fs = img.findCircle()
	if (fs != None):
		fs.draw()
	img.save(new_file_path)
	return new_file_path	

def find_blobs(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.step_outputs[len(si.step_outputs) - 1])
	fs = img.findBlobs()
	if (fs != None):
		fs.draw()
	img.save(new_file_path)
	return new_file_path

# Strategy is to find blobs that have an edge on the perimeter of the image.  Remove 
# these blobs from the image.  The blobs also need to be at least 2% of the image.
def find_and_remove_bottom_blobs(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.step_outputs[len(si.step_outputs) - 1])
	for blob in img.findBlobs():
		if (blob.area() / img.area() > 0.02):
			edge_rect = [ point for point in blob.minRect() if point[0] < 10 or point[0] > img.width - 10 or point[1] < 10 or point[1] > img.height - 10]
			if (len(edge_rect) >= 2):
				blob.draw()
	img.save(new_file_path)
	return new_file_path

def dilate_and_erode(si, step_number):
	new_file_path = step_file_path(si, step_number)
	img = Image(si.step_outputs[len(si.step_outputs) - 1])
	img.erode(1).save(new_file_path)
	return new_file_path	

# Make the 'corrected' file path
shutil.rmtree('corrected')
if not os.path.exists("corrected"):
  os.makedirs("corrected")

sis = sample_images()

steps = [ correct_alignment, scale_down, dilate_and_erode, find_and_remove_bottom_blobs, find_corners ]

for si in sis:
	for counter, step in enumerate(steps):
		step_output = step(si, counter + 1)
		si.step_outputs.append(str(step_output))

write_file("output.html", load_cache({"rows": sorted(sis, key=lambda si: str(si.index) + si.foot)}) )

print "Done!"