#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime


def get(url, filename):

	# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
	cj = cookielib.CookieJar()
	# �Զ���opener,����opener��CookieJar�����
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
	urllib2.install_opener(opener)

	# Step1:��ȡtoken
	content = urllib2.urlopen(url).read()

	fw = open(filename,'w+')
	fw.write(content)
	fw.close()



if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	for i in range(10):
		filename = "../pics/gujinsuo/pics_orignal/" + str("%04d" % i) + ".jpg"
		get("https://www.gujinsuo.com.cn/auth/random?_=1445347060681", filename)
