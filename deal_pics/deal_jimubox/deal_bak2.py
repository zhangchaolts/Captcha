#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter  
import sys 
import Queue
import os


BLACK_COLOR = 0
WHITE_COLOR = 255
THRESHOLD_COLOR = 140

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


def get_one_character(pic, avg_pixel_number):
	#print_pic(pic)
	(width, height) = pic.size
	minX = width
	minY = height
	maxX = 0
	maxY = 0
	#print minX,minY,maxX,maxY
	visited = {}
	#print_pic(pic)
	flag_find = False
	for i in xrange(width):
		for j in xrange(height):
			if flag_find == True:
				continue
			if pic.getpixel((i, j)) == WHITE_COLOR:
				continue
			q = Queue.Queue()
			visited = {}
			q.put((i, j))
			visited[(i, j)] = True
			xx = [0, 1, 0, -1, 1, 1, -1, -1]
			yy = [1, 0, -1, 0, 1, -1, 1, -1]
			while q.empty() != True:
				(x, y) = q.get()
				#print pic.getpixel((x, y))
				for k in xrange(8):
					if 0 <= x + xx[k] < width and 0 <= y + yy[k] < height and visited.has_key((x + xx[k], y + yy[k])) == False and pic.getpixel((x + xx[k], y + yy[k])) == BLACK_COLOR:
						#print x + xx[k] , y + yy[k] 
						q.put((x + xx[k], y + yy[k]))
						visited[(x + xx[k], y + yy[k])] = True
						maxX = max(maxX, x + xx[k])
						minX = min(minX, x + xx[k])
						maxY = max(maxY, y + yy[k])
						minY = min(minY, y + yy[k])
				flag_find = True
	block = pic.crop((0, 0, 1, 1))
	#print minX,minY,maxX,maxY
	#print avg_pixel_number
	#print len(visited)
	if minX < maxX + 1 and minY < maxY + 1 and len(visited) > avg_pixel_number / 5:
		block = pic.crop((minX, minY, maxX + 1, maxY + 1))
		(block_width, block_height) = block.size
		#print (width, height)
		#print (block_width, block_height)
		#print (minX + block_width, minY + block_height)
		for i in xrange(block_width):
			for j in xrange(block_height):
				if visited.has_key((minX + i, minY + j)) == True:
					block.putpixel((i, j), BLACK_COLOR)
					pic.putpixel((minX + i, minY + j), WHITE_COLOR)
				else:
					block.putpixel((i, j), WHITE_COLOR)
	return block


def split(pic, avg_pixel_number, dir_path_step, pic_step, pic_ptr_str):
	pic1 = pic.copy()
	block_array = []
	loop = 0
	while loop < 10:
		#print get_pic_black_pixel_number(pic1)
		block = get_one_character(pic1, avg_pixel_number)
		(block_width, block_height) = block.size
		#print (block_width, block_height) 
		if block_width > 1 and block_height > 1:
			block_array.append(block)
		pic1 = smooth(pic1)
		loop += 1
	if len(block_array) == 4:
		for i in xrange(len(block_array)):
			block_array[i].save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '_' + str(i) + '.jpg')


def recognize(pic, train_pic_dict, dir_path_step, pic_step, pic_ptr_str):
	pic1 = pic.copy()
	block_array = []
	loop = 0
	while loop < 10:
		block = get_one_character(pic1, avg_pixel_number)
		(block_width, block_height) = block.size
		if block_width > 1 and block_height > 1:
			block_array.append(block)
		pic1 = smooth(pic1)
		loop += 1
	if len(block_array) == 4:
		recognized_characte_array = []
		recognized_str = ''
		for i in xrange(len(block_array)):
			recognized_characte = recognize_one_character(block_array[i], train_pic_dict)
			print recognized_characte
			recognized_characte_array.append(recognized_characte)
			recognized_str += recognized_characte
		print recognized_str
		#print_pic(pic)
		pic.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '_' + recognized_str + '.jpg')
			


def recognize_one_character(block, train_pic_dict):
	most_match_character = '#'
	least_distance = 10000	
	for character_pic,character in train_pic_dict.items():
		distance = get_distance(block, character_pic)
		if distance < least_distance:
			most_match_character = character
			least_distance = distance
	return most_match_character


def get_distance(block, character_pic):
	block_resize = block.resize((12, 18), Image.ANTIALIAS)
	block_resize_binarized = binarized(block_resize)
	block_strlist = get_strlist_from_pic(block_resize_binarized)
	character_pic_strlist = get_strlist_from_pic(character_pic)
	#print_pic(block_resize_binarized)
	#print block_strlist
	#print character_pic_strlist
	return levenshtein(block_strlist, character_pic_strlist)


def get_strlist_from_pic(pic):
	list = []
	(width, height) = pic.size
	for i in xrange(width):
		for j in xrange(height):
			list.append(pic.getpixel((i, j)))
	return list


def levenshtein(first, second):
	if len(first) > len(second):  
		first,second = second,first  
	if len(first) == 0:  
		return len(second)  
	if len(second) == 0:  
		return len(first)  
	first_length = len(first) + 1  
	second_length = len(second) + 1  
	distance_matrix = [range(second_length) for x in range(first_length)]   
	#print distance_matrix  
	for i in range(1,first_length):  
		for j in range(1,second_length):  
			deletion = distance_matrix[i-1][j] + 1  
			insertion = distance_matrix[i][j-1] + 1  
			substitution = distance_matrix[i-1][j-1]  
			if first[i-1] != second[j-1]:  
				substitution += 1  
			distance_matrix[i][j] = min(insertion,deletion,substitution)  
	#print distance_matrix  
	return distance_matrix[first_length-1][second_length-1]  


if __name__ == '__main__':

	dir_path_base = '../get_pics/yirendai_pics/'
	dir_path_step = '../get_pics/yirendai_pics_step'
	dir_train_pics = '../get_pics/train_pics'

	deal_number = 100
	
	total_pixel_number = 0
	im_array = []

	for pic_ptr in xrange(deal_number):

		pic_ptr_str = str('%04d' % pic_ptr)
		image_path = dir_path_base + pic_ptr_str + '.jpg'

		#打开图片
		pic_step = 1
		im1 = Image.open(image_path)
		im1.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg')
		pic_step += 1
	
		#转化到亮度
		pic_step = 2
		im2 = im1.convert('L')  
		im2.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg')
   
		#二值化
		pic_step = 3
		im3 = binarized(im2)
		im3.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg')

		#去除边框
		pic_step = 4
		im4 = remove_edge(im3)
		im4.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg')
		
		#降噪
		pic_step = 5
		im5 = smooth(im4)
		im5.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg')

		(width, height) = im5.size
		for i in xrange(width):
			for j in xrange(height):
				if im5.getpixel((i, j)) == BLACK_COLOR:
					total_pixel_number += 1
		
		im_array.append(im5)

	# 统计每个字符的像素点的平均值
	avg_pixel_number = total_pixel_number / (deal_number * 4)
	#print avg_pixel_number

	#分割字符
	pic_step = 6
	for pic_ptr in xrange(len(im_array)):
		pic_ptr_str = str('%04d' % pic_ptr)
		im6 = im_array[pic_ptr]
		#split(im6, avg_pixel_number, dir_path_step, pic_step, pic_ptr_str)

	#训练
	pic_step = 7
	train_pic_dict = {}
	file_list = os.listdir(dir_train_pics)
	for file in file_list:
		character = file[0:1]
		im7_0 = Image.open(dir_train_pics + '/' + file)
		im7_1 = im7_0.resize((12, 18), Image.ANTIALIAS)
		im7_2 = binarized(im7_1)
		#print_pic(im7_2)
		train_pic_dict[im7_2] = character
		im7_2.save(dir_path_step + str(pic_step) + '/' + file)

	#识别
	pic_step = 8
	for pic_ptr in xrange(len(im_array)):
		pic_ptr_str = str('%04d' % pic_ptr)
		im8 = im_array[pic_ptr]
		recognize(im8, train_pic_dict, dir_path_step, pic_step, pic_ptr_str)
