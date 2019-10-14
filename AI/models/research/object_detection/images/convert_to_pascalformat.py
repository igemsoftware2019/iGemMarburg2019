#!/usr/bin/python -tt

# python code to convert coco val2014 JSON file to PASCAL XML.

import sys

def main():
	if len(sys.argv) != 2:
		print('usage: python convert_to_pascalformat.py coco_dataDir ')
		print('for example: python convert_to_pascalformat.py \'./\' ')
		sys.exit(1)

	dataDir = sys.argv[1]

	import os, glob, json

	#Find file with .json ending
	os.chdir("./{0}".format(dataDir))
	for file in glob.glob("*.json"):
		with open('{0}'.format(file), 'r') as ai:
			json_load = json.loads(ai.read())
			xml = "<?xml version=\"1.0\"?>\n"
			xml += "<annotation>\n"
			xml += "\t<folder>images</folder>\n"
			xml += "\t<filename>{0}.JPG</filename>\n".format(file.split('.json')[0])
			xml += "\t<path>images/{0}.JPG</path>\n".format(file.split('.json')[0])
			xml += "\t<source>\n"
			xml += "\t\t <database>Unknown</database>\n"
			xml += "\t</source>\n"
			xml += "\t<size>\n"
			xml += "\t\t <width>{0}</width>\n".format(json_load["images"][0]["width"])
			xml += "\t\t <height>{0}</height>\n".format(json_load["images"][0]["height"])
			xml += "\t\t <depth>3</depth>\n"
			xml += "\t</size>\n"
			xml += "\t<segmented>0</segmented>\n"
			for i in range(len(json_load['annotations'])):
				xml += "\t<object>\n"
				xml += "\t\t<name>colony</name>\n"
				xml += "\t\t<pose>Unspecified</pose>\n"
				xml += "\t\t<truncated>0</truncated>\n"
				xml += "\t\t<difficult>0</difficult>\n"
				xml += "\t\t<bndbox>\n"
				x_cord = []
				y_cord = []
				[x_cord.append(json_load['annotations'][i]['segmentation'][0][j*2]) for j in range(4)]
				[y_cord.append(json_load['annotations'][i]['segmentation'][0][j*2+1]) for j in range(4)]
				xml += "\t\t\t<xmin>{0}</xmin>\n".format(min(x_cord))
				xml += "\t\t\t<ymin>{0}</ymin>\n".format(min(y_cord))
				xml += "\t\t\t<xmax>{0}</xmax>\n".format(max(x_cord))
				xml += "\t\t\t<ymax>{0}</ymax>\n".format(max(x_cord))
				xml += "\t\t</bndbox>\n"
				xml += "\t</object>\n"
			xml += "</annotation>\n"
			f_xml = open(file.split('.json')[0] + '.xml', 'w+')
			f_xml.write(xml)
			f_xml.close()
			print("{0}.json converted into {0}.xml \n".format(file.split('.json')[0]))

if __name__ == '__main__':
  main()