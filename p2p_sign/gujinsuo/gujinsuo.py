#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import recognizer_gjs.recognizer
import string

def sign(username, password):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	print username + " start ..."

	is_logined = False
	try_times = 0

	while try_times < 20:

		try_times += 1

		# Step1:识别验证码
		first_headers = {	"Accept" : "*/*", \
							"Cache-Control" :"max-age=0", \
							"Connection" : "keep-alive", \
							"Host" : "www.gujinsuo.com.cn", \
							"Upgrade-Insecure-Requests" : "1", \
							"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
						} 

		first_url = "https://www.gujinsuo.com.cn/login.html"
		first_request = urllib2.Request(first_url, headers=first_headers)
		first_response = opener.open(first_request).read().decode('utf8').encode('gb18030')
		#print first_response

		fw = open('pics_captcha_gjs/0.jpg', 'wb+')

		captcha_url = 'https://www.gujinsuo.com.cn/auth/random?_=' + str(int(time.mktime(datetime.datetime.now().timetuple()))) + '000'
		captcha_request = urllib2.Request(captcha_url, headers=first_headers)
		captcha_response = opener.open(captcha_request).read()
		fw.write(captcha_response)
		fw.close()

		randcode = recognizer_gjs.recognizer.recognize('pics_captcha_gjs/0.jpg', 'pics_train_gjs')
		print "(" + str(try_times) + ") " + "randcode:" + randcode

		# Step2:登录
		login_url = "https://www.gujinsuo.com.cn/login"

		login_data = {	"username": username, \
						"password": password, \
						"randcode": randcode \
					}
		print login_data

		login_post_data = urllib.urlencode(login_data) 

		login_headers = {	"Referer" : "https://www.gujinsuo.com.cn/login.html", \
							"Host" : "www.gujinsuo.com.cn", \
							"Accept" : "*/*", \
							"Origin" : "https://www.gujinsuo.com.cn", \
							"Content-Type" : "application/x-www-form-urlencoded", \
							"X-Requested-With" : "XMLHttpRequest", \
							"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
						}

		login_request = urllib2.Request(login_url, login_post_data, login_headers)

		login_response = opener.open(login_request).read().decode('utf8').encode('gb18030')
		#print login_response

		login_info = ""
		login_anwser = re.search('"message" : "(.*?)",', login_response)
		if login_anwser:
			login_info = login_anwser.group(1)
			if login_info.find("您已成功登录本系统!") == -1 and login_info.find("验证码输入错误!") == -1 and login_info.find("请输入验证码!") == -1:
				result = "登录失败！"
				return result

		homepage_headers = {	"Referer" : "https://www.gujinsuo.com.cn/login.xhtml", \
								"Host" : "www.gujinsuo.com.cn", \
								"Accept" : "*/*", \
								"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
							}

		homepage_url = "https://www.gujinsuo.com.cn/member/main.html"
		homepage_request = urllib2.Request(homepage_url, headers = homepage_headers)
		homepage_html = opener.open(homepage_request).read().decode('utf8').encode('gb18030')
		#print homepage_html

		if homepage_html.find('退出') == -1:
			print "第" + str(try_times) +"次识别验证码错误，登录失败..."
			continue
		else:
			print "登录成功!"
			is_logined = True
			break

	if is_logined == False:
		#print "尝试20次都登陆失败，程序无能为力了，大侠还是手动签到吧~\n"
		result = "登录失败：尝试20次都登陆失败！"
		return result
	
	#print "开始签到..." 

	# Step3:签到
	sign_url = "https://www.gujinsuo.com.cn/spread/sign?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
	sign_request = urllib2.Request(sign_url, headers = homepage_headers)
	sign_response = opener.open(sign_request).read().decode('utf8').encode('gb18030')

	result1 = ""

	gainPopularity = ""
	sign_anwser = re.search('您已成功签到,系统送您(.*?)元的红包', sign_response)
	if sign_anwser:
		gainPopularity = sign_anwser.group(1)
		result1 = "今日签到获得" + gainPopularity + "元红包。"
	else:
		result1 = "今日已经签到过！"

	# Step4
	home_headers = {	"Referer" : "https://www.gujinsuo.com.cn/customer/main.xhtml", \
						"Host" : "www.gujinsuo.com.cn", \
						"Accept" : "*/*", \
						"X-Requested-With" : "XMLHttpRequest", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
					}
	home_url = "https://www.gujinsuo.com.cn/customer/sign/getSignDays?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
	home_request = urllib2.Request(home_url, headers = home_headers)
	home_html = opener.open(home_request).read().decode('utf8').encode('gb18030')
	#print home_html

	result2 = ""
	totalPopularity = ""
	home_anwser = re.search('"totalSignAmount" : (.*?),', home_html)
	if home_anwser:
		totalPopularity = home_anwser.group(1)
		result2 = "总红包为" + totalPopularity + "。"

	result = result1 + result2
	return result


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = []
	password_array = []

	for line in file("固金所账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			username_array.append(parts[0])
			password_array.append(parts[1])

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";
 
	for i in range(len(username_array)):
		result = sign(username_array[i], password_array[i])
		print username_array[i] + ":" + result
