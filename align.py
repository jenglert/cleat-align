import os
from os import listdir
from os.path import isfile, join
import re
from airspeed import CachingFileLoader
from SimpleCV import Image

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

def correct_alignment(si, step_number):
	cwd = os.getcwd()
	new_file_path = cwd + "/corrected/" + si.index + "-" + si.name + "-" + si.foot + "-Step" + str(step_number) + ".jpg"
	img = Image(si.original_file_name) 
	if (img.width > img.height):
		img.rotate(-90, fixed=False).save(new_file_path)
	else:
		img.save(new_file_path)
	return new_file_path

# Make the 'corrected' file path
if not os.path.exists("corrected"):
  os.makedirs("corrected")

sis = sample_images()

steps = [ correct_alignment ]

for si in sis:
	for counter, step in enumerate(steps):
		step_output = step(si, counter + 1)
		si.step_outputs.append(str(step_output))

write_file("output.html", load_cache({"rows": sorted(sis, key=lambda si: str(si.index) + si.foot)}) )

print "Done!"