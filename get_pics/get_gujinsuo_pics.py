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

	# Step1:获取token
	content = urllib2.urlopen(url).read()

	fw = open(filename,'w+')
	fw.write(content)
	fw.close()



if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	for i in range(1000):
		filename = "../pics/gujinsuo/pics_orignal/" + str("%04d" % i) + ".jpg"
		get("https://www.gujinsuo.com.cn/auth/random?_=1445347060681", filename)
