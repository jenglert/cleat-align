from os import listdir
from os.path import isfile, join
import re
from airspeed import CachingFileLoader

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

for x in sample_images():
	print x

write_file("output.html", load_cache({"rows": sample_images()}) )

print "Done!"