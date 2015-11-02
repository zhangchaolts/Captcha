#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter
import Queue 
import preprocessor

def split(pic, block_array):
	pic1 = pic.copy()
	loop = 0 
	while loop < 10: 
		block = get_one_character(pic1)
		(block_width, block_height) = block.size
		if block_width > 1 and block_height > 1:
			block_array.append(block)
		pic1 = preprocessor.smooth(pic1)
		loop += 1

def get_one_character(pic):
	(width, height) = pic.size
	minX = width
	minY = height
	maxX = 0
	maxY = 0
	visited = {}
	flag_find = False
	for i in xrange(width):
		for j in xrange(height):
			if flag_find == True:
				continue
			if pic.getpixel((i, j)) == preprocessor.WHITE_COLOR:
				continue
			q = Queue.Queue()
			visited = {}
			q.put((i, j))
			visited[(i, j)] = True
			xx = [0, 1, 0, -1, 1, 1, -1, -1]
			yy = [1, 0, -1, 0, 1, -1, 1, -1]
			while q.empty() != True:
				(x, y) = q.get()
				for k in xrange(8):
					if 0 <= x + xx[k] < width and 0 <= y + yy[k] < height and visited.has_key((x + xx[k], y + yy[k])) == False and pic.getpixel((x + xx[k], y + yy[k])) == preprocessor.BLACK_COLOR:
						q.put((x + xx[k], y + yy[k]))
						visited[(x + xx[k], y + yy[k])] = True
						maxX = max(maxX, x + xx[k])
						minX = min(minX, x + xx[k])
						maxY = max(maxY, y + yy[k])
						minY = min(minY, y + yy[k])
				flag_find = True
	block = pic.crop((0, 0, 1, 1))
	if minX < maxX + 1 and minY < maxY + 1 and len(visited) > preprocessor.THRESHOLD_CHARACTER_PIXEL_NUMBER:
		block = pic.crop((minX, minY, maxX + 1, maxY + 1))
		(block_width, block_height) = block.size
		for i in xrange(block_width):
			for j in xrange(block_height):
				if visited.has_key((minX + i, minY + j)) == True:
					block.putpixel((i, j), preprocessor.BLACK_COLOR)
					pic.putpixel((minX + i, minY + j), preprocessor.WHITE_COLOR)
				else:
					block.putpixel((i, j), preprocessor.WHITE_COLOR)
	return block


if __name__ == '__main__':
	pic = Image.open('../../pics/yirendai/pics_orignal/0000.jpg')
	pic_preprocessed = preprocessor.preprocess(pic)
	block_array = []
	split(pic_preprocessed, block_array)
	for i in xrange(len(block_array)):
		block_array[i].save('test_spliter_block_' + str(i) + '.jpg')
	
