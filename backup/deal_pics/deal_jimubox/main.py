#coding=utf-8
import Image
import ImageEnhance
import ImageFilter
import preprocessor
import spliter
import recognizer

if __name__ == '__main__':

	dir_path_base = '../../pics/jimubox/pics_orignal/'
	dir_path_step = '../../pics/jimubox/pics_step'

	deal_number = 50

	pic_step = 1
	for pic_ptr in xrange(deal_number):

		pic_ptr_str = str('%04d' % pic_ptr)
		image_path = dir_path_base + pic_ptr_str + '.jpg'

		pic = Image.open(image_path)
		pic_preprocessed = preprocessor.preprocess(pic)
		pic_preprocessed.save(dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg')
		print dir_path_step + str(pic_step) + '/' + pic_ptr_str + '_' + str(pic_step) + '.jpg'
	pic_step += 1
	
