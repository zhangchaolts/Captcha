#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter  
import Queue
import os
import string
import preprocessor
import spliter

THRESHOLD_BLOCK_NUMBER = 3

def recognize(pic, dir_train_pics):
	pic = Image.open(pic)
	#print 'preprocessor.preprocess'
	pic_preprocessed = preprocessor.preprocess(pic)
	block_array = []
	#print 'spliter.split'
	spliter.split(pic_preprocessed, block_array)
	captcha = ""
	if len(block_array) >= THRESHOLD_BLOCK_NUMBER:
		#print 'recognize_block_array'
		captcha = recognize_block_array(block_array, dir_train_pics)
	return captcha


def recognize_block_array(block_array, dir_train_pics):
	train_pic_dict = {}
	read_tran_pics(dir_train_pics, train_pic_dict)
	recognized_str = ''
	digit0_str = ''
	digit1_str = ''
	notation_str = ''
	for i in xrange(THRESHOLD_BLOCK_NUMBER):
		recognized_character = recognize_one_character(block_array[i], train_pic_dict)
		#print recognized_character
		if i == 0:
			digit0_str = recognized_character
		if i == 1:
			notation_str = recognized_character
		if i == 2:
			digit1_str = recognized_character
	if digit0_str != '' and digit1_str != '' and notation_str != '' and digit0_str != 'A' and digit0_str != 'M' and digit1_str != 'A' and digit1_str != 'M':
		if notation_str == 'J':
			recognized_str = str(string.atoi(digit0_str) + string.atoi(digit1_str))
		if notation_str == 'M':
			recognized_str = str(string.atoi(digit0_str) * string.atoi(digit1_str))
	return recognized_str


def read_tran_pics(dir_train_pics, train_pic_dict):
	file_list = os.listdir(dir_train_pics)
	for file in file_list:
		#print file
		character = file[0:1]
		im0 = Image.open(dir_train_pics + '/' + file)
		train_pic_dict[im0] = character


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
	block_resize_binarized = preprocessor.binarized(block_resize)
	block_strlist = get_strlist_from_pic(block_resize_binarized)
	character_pic_resize = character_pic.resize((12, 18), Image.ANTIALIAS)
	character_pic_resize_binarized = preprocessor.binarized(character_pic_resize)
	character_pic_strlist = get_strlist_from_pic(character_pic_resize_binarized)
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
	file_pic = '../../pics/dangtianjinrong/pics_orignal/0003.jpg'
	dir_train_pics = '../../pics/dangtianjinrong/pics_train/'
	captcha = recognize(file_pic, dir_train_pics)
	print captcha

