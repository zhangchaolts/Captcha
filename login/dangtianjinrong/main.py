#coding=utf-8
import Image
import ImageEnhance
import ImageFilter
import preprocessor
import spliter
import recognizer

if __name__ == '__main__':

	dir_path_base = '../../pics/dangtianjinrong/pics_orignal/'
	dir_path_step = '../../pics/dangtianjinrong/pics_step'
	dir_path_train = '../../pics/dangtianjinrong/pics_train/'

	deal_number = 20

	pic_step1 = 1
	pic_step2 = 2
	pic_step3 = 3

	for pic_ptr in xrange(deal_number):

		pic_ptr_str = str('%04d' % pic_ptr)
		image_path = dir_path_base + pic_ptr_str + '.jpg'

		pic = Image.open(image_path)
		pic_preprocessed = preprocessor.preprocess(pic)

		output_path = dir_path_step + str(pic_step1) + '/' + pic_ptr_str + '_' + str(pic_step1) + '.jpg'
		print output_path
		pic_preprocessed.save(output_path)

		block_array = []
		spliter.split(pic_preprocessed, block_array)
		for i in xrange(len(block_array)):
			output_path = dir_path_step + str(pic_step2) + '/' + pic_ptr_str + '_' + str(pic_step2) + '_' + str(i) + '.jpg'
			print output_path
			block_array[i].save(output_path)

	for pic_ptr in xrange(deal_number):

		pic_ptr_str = str('%04d' % pic_ptr)
		image_path = dir_path_base + pic_ptr_str + '.jpg'

		captcha = recognizer.recognize(image_path, dir_path_train)
		if captcha != "":
			pic = Image.open(image_path)
			output_path = dir_path_step + str(pic_step3) + '/' + pic_ptr_str + '_' + str(pic_step3) + '_' + captcha + '.jpg'
			print output_path
			pic.convert('RGB').save(output_path)

