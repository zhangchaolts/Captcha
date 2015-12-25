#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter  
import Queue

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


def denoising_remove_line(pic):
	(width, height) = pic.size
	for i in xrange(width):
		for j in xrange(height):
			if pic.getpixel((i, j)) == BLACK_COLOR:
				cnt = 0
				for x_bias in xrange(-1, 2):
					for y_bias in xrange(-1, 2):
						if 0 <= i + x_bias < width and 0 <= j + y_bias < height and pic.getpixel((i + x_bias, j + y_bias)) == BLACK_COLOR:
							cnt += 1
				if cnt <= 3:
					pic.putpixel((i, j), WHITE_COLOR)
	return pic


def denoising_remove_little_block(pic):
	pic_deal = pic.copy()
	pic_visited_dict = {}
	loop = 0
	#print get_pic_black_pixel_number(pic)
	while loop < 20:
		block = get_block(pic_deal, pic_visited_dict)
		#block.save('test_preprocessor_' + str(loop) + '.jpg')
		#print len(pic_visited_dict)
		if len(pic_visited_dict) == get_pic_black_pixel_number(pic):
			break
		loop += 1
		#print loop
	return pic_deal


def get_block(pic, pic_visited_dict):
	block = pic.crop((0, 0, 1, 1))
	(width, height) = pic.size
	is_find = False
	for i in xrange(width):
		for j in xrange(height):
			if pic.getpixel((i, j)) == WHITE_COLOR:
				continue
			if pic_visited_dict.has_key((i, j)) == True:
				continue
			q = Queue.Queue()
			block_visited_dict = {}
			q.put((i, j)) 
			block_visited_dict[(i, j)] = True
			pic_visited_dict[(i, j)] = True
			minX = i
			minY = j
			maxX = i
			maxY = j
			xx = [0, 1, 0, -1, 1, 1, -1, -1] 
			yy = [1, 0, -1, 0, 1, -1, 1, -1] 
			while q.empty() != True:
				(x, y) = q.get()
				for k in xrange(8):
					if 0 <= x + xx[k] < width and 0 <= y + yy[k] < height and block_visited_dict.has_key((x + xx[k], y + yy[k])) == False and pic.getpixel((x + xx[k], y + yy[k])) == BLACK_COLOR:
						q.put((x + xx[k], y + yy[k]))
						block_visited_dict[(x + xx[k], y + yy[k])] = True
						pic_visited_dict[(x + xx[k], y + yy[k])] = True
						minX = min(minX, x + xx[k])
						minY = min(minY, y + yy[k])
						maxX = max(maxX, x + xx[k])
						maxY = max(maxY, y + yy[k])
			if minX < maxX + 1 and minY < maxY + 1:
				block = pic.crop((minX, minY, maxX + 1, maxY + 1)) #前两个参数是闭，后两个参数是开 
				(block_width, block_height) = block.size
				#print 'len(block_visited_dict):' + str(len(block_visited_dict))
				for i in xrange(block_width):
					for j in xrange(block_height):
						if block_visited_dict.has_key((minX + i, minY + j)) == True:
							if len(block_visited_dict) < THRESHOLD_CHARACTER_PIXEL_NUMBER:
								pic.putpixel((minX + i, minY + j), WHITE_COLOR)
						else:
							block.putpixel((i, j), WHITE_COLOR)
			is_find = True
			break
		if is_find == True:
			break
	return block


def preprocess(pic):
	#转化到亮度
	im1 = pic.convert('L') 
	#二值化
	im2 = binarized(im1)
	#去除干扰线
	im3 = im2
	#times = 0
	#while times < 5:
	#	im3 = denoising_remove_line(im3)
	#	times += 1
	#去除小block
	im4 = denoising_remove_little_block(im3)
	return im4


if __name__ == '__main__':
	pic = Image.open('../../pics/dangtianjinrong/pics_orignal/0003.jpg')
	pic_preprocessed = preprocess(pic)
	pic_preprocessed.save('test_preprocessor.jpg')

