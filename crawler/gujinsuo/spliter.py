#coding=utf-8
import Image  
import ImageEnhance  
import ImageFilter
import Queue 
import preprocessor

def split(pic, block_array):
	pic_deal = pic.copy()
	pic_visited_dict = {}
	loop = 0 
	while loop < 10: 
		block = preprocessor.get_block(pic_deal, pic_visited_dict)
		block_array.append(block)
		if len(pic_visited_dict) == preprocessor.get_pic_black_pixel_number(pic):
			break
		loop += 1


if __name__ == '__main__':
	pic = Image.open('../../pics/gujinsuo/pics_orignal/0001.jpg')
	pic_preprocessed = preprocessor.preprocess(pic)
	block_array = []
	split(pic_preprocessed, block_array)
	for i in xrange(len(block_array)):
		block_array[i].save('test_spliter_block_' + str(i) + '.jpg')
	
