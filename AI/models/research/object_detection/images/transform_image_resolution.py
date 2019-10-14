from PIL import Image
import os
import argparse
import glob

def rescale_images(directory, size):
	
	for img in os.listdir(directory):
		print(img)
		im = Image.open(directory+img)
		im_resized = im.resize(size, Image.ANTIALIAS)
		im_resized.save(directory+img)


if __name__ == '__main__':
	dir_path = os.path.dirname(os.path.realpath(__file__))
	parser = argparse.ArgumentParser(description="Rescale images")
	parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
	parser.add_argument('-s', '--size', type=int, nargs=2, required=True, metavar=('width', 'height'), help='Image size')
	args = parser.parse_args()
	print(dir_path)
	rescale_images(args.directory, args.size)