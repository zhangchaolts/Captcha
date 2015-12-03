#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime


def get(url, filename):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	url = "http://www.gujinsuo.com.cn/login.html"
	html = urllib2.urlopen(url).read()

	print 'ok1'
	content = urllib2.urlopen(url).read()
	print 'ok2'
	fw = open(filename,'wb+')
	fw.write(content)
	fw.close()



if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	for i in range(10):
		filename = "../pics/gujinsuo/pics_orignal/" + str("%04d" % i) + ".jpg"
		filename = '0000.jpg'
		print filename
		get("http://www.gujinsuo.com.cn/auth/random?_=1445347060681", filename)
