import re
import os

def step_file_name(img_path, desc):
	sample_regex = re.compile('.*/(\d+-.*-[LR]).*[.][jJ][pP][gG]', re.IGNORECASE)
	match = sample_regex.match(img_path)
	cwd = os.getcwd()

	if not os.path.exists("corrected"):
			os.makedirs("corrected")

	if match:
		return cwd + "/corrected/" + match.group(1) + "-" + str(desc) + ".jpg"
	else:
		raise Exception("Unable to parse image path: " + img_path)