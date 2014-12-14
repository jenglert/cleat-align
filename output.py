from airspeed import CachingFileLoader

class ShoesReportViewModel:
	def __init__(self, pair_reports):
		self.pair_reports = pair_reports

	def write_file(self, file_name):
		loader = CachingFileLoader("html")
		template = loader.load_template("layout.html")
		html = template.merge({"vm": self }, loader=loader)
		f = open(file_name, "w")
		f.write(html)
		f.close()

class PairReport:
	def __init__(self, index, name, left, right, report):
		self.index = index
		self.name = name
		self.left = left
		self.right = right
		self.report = report

class ShoeReport:
	def __init__(self, images, area, shoe_angle, shoe_length, cleat_width):
		self.images = images
		self.area = area
		self.shoe_angle = shoe_angle
		self.shoe_length = shoe_length
		self.cleat_width = cleat_width

def make_shoe_report_view_model(index, name, left_images, right_images, left_sm, right_sm, report):
	left = ShoeReport(left_images, left_sm.area(), left_sm.toe_heel_angle(), left_sm.shoe_length(), left_sm.cleat_width())
	right = ShoeReport(right_images, right_sm.area(), right_sm.toe_heel_angle(), right_sm.shoe_length(), right_sm.cleat_width())
	pair = PairReport(index, name, left, right, report.pretty_html())
	return ShoesReportViewModel([pair])