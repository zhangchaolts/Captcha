#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter  


BLACK_COLOR = 0
WHITE_COLOR = 255
THRESHOLD_COLOR = 140
THRESHOLD_CHARACTER_PIXEL_NUMBER = 5

def print_pic(pic):
	(width, height) = pic.size
	for i in xrange(width):
		for j in xrange(height):
			print pic.getpixel((i, j)),
		print
	print


def get_pic_black_pixel_number(pic):
	pixel_number = 0
	(width, height) = pic.size
	for i in xrange(width):
		for j in xrange(height):
			if pic.getpixel((i, j)) == BLACK_COLOR:
				pixel_number += 1
	return pixel_number


def compare_pics(pic0, pic1):
	(width0, height0) = pic0.size
	(width1, height1) = pic1.size
	if width0 != width1 or height0 != height1:
		return False
	for i in xrange(width0):
		for j in xrange(height0):
			if pic0.getpixel((i, j)) != pic1.getpixel((i, j)):
				return False
	return True


def binarized(pic):
	(width, height) = pic.size
	for i in xrange(width):
		for j in xrange(height):
			if pic.getpixel((i, j)) > THRESHOLD_COLOR:
				pic.putpixel((i, j), WHITE_COLOR)
			else:
				pic.putpixel((i, j), BLACK_COLOR)
	return pic


def remove_edge(pic):
	(width, height) = pic.size
	for i in xrange(width):
		for j in xrange(height):
			if i <= 0 or i >= width - 1:
				pic.putpixel((i, j), WHITE_COLOR)
			if j <= 0 or j >= height - 1:
				pic.putpixel((i, j), WHITE_COLOR)
	return pic


def smooth(pic):
	(width, height) = pic.size
	xx = [1, 0, -1, 0]
	yy = [0, 1, 0, -1]
	for i in xrange(width):
		for j in xrange(height):
			if pic.getpixel((i, j)) == BLACK_COLOR:
				cnt = 0
				for k in xrange(4):
					if 0 <= i + xx[k] < width and 0 <= j + yy[k] < height and pic.getpixel((i + xx[k], j + yy[k])) == WHITE_COLOR:
						cnt += 1
				if cnt > 3:
					pic.putpixel((i, j), WHITE_COLOR)
	return pic


def preprocess(pic):
	#转化到亮度
	im1 = pic.convert('L') 
	#二值化
	im2 = binarized(im1)
	#去除边框
	im3 = remove_edge(im2)
	#去除噪音点
	im4 = smooth(im3)
	return im4


if __name__ == '__main__':
	pic = Image.open('../../pics/yirendai/pics_orignal/0000.jpg')
	pic_preprocessed = preprocess(pic)
	pic_preprocessed.save('test_preprocessor.jpg')

