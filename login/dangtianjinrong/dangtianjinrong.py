#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import recognizer_dtjr.recognizer
import string
import multiprocessing

manager = multiprocessing.Manager()
status_list = manager.list()

def sign(line_ptr, username, password):

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
		url = "http://weixin.dtd365.com/index.php/home/account/login.html"
		html = urllib2.urlopen(url).read()

		fw = open('pics_captcha_dtjr/' + str(line_ptr) + '.jpg', 'wb+')
		content = urllib2.urlopen('http://wxticket.dtd365.com/index.php/home/index/getvcode.html').read()
		fw.write(content)
		fw.close()

		randcode = recognizer_dtjr.recognizer.recognize('pics_captcha_dtjr/' + str(line_ptr) + '.jpg', 'pics_train_dtjr')
		print "(" + str(line_ptr) + "," + str(try_times) + ") " + "randcode:" + randcode

		# Step2:登录
		login_url = "http://weixin.dtd365.com/index.php/home/index/login.html"

		login_data = {	"username": username, \
						"password": password, \
						"captcha": randcode \
					}
		print login_data

		login_post_data = urllib.urlencode(login_data) 

		login_headers = {	"Referer" : "http://weixin.dtd365.com/index.php/home/account/login.html", \
							"Host" : "weixin.dtd365.com", \
							"Accept" : "*/*", \
							"Origin" : "http://weixin.dtd365.com", \
							"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
							"X-Requested-With" : "XMLHttpRequest", \
							"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
						}

		login_request = urllib2.Request(login_url, login_post_data, login_headers)

		login_response = opener.open(login_request).read().decode('utf8').encode('gb18030')

		homepage_url = "http://weixin.dtd365.com/index.php/home/account/index.html";
		homepage_html = urllib2.urlopen(homepage_url).read().decode('utf8').encode('gb18030')
		#print homepage_html

		if homepage_html.find('上次登录') == -1:
			#print "第" + str(try_times) +"次识别验证码错误，登录失败..."
			continue
		else:
			#print "登录成功!"
			is_logined = True
			break

	if is_logined == False:
		#print "尝试20次都登陆失败，程序无能为力了，大侠还是手动签到吧~\n"
		result = "登录失败：尝试20次都登陆失败！"
		status_list.append(str(line_ptr) + " " + result)

	# Step3:签到

	result1 = ""
	result3 = ""

	status_url = "http://weixin.dtd365.com/index.php/home/activity/showsign.html"
	status_html = urllib2.urlopen(status_url).read().decode('utf8').encode('gb18030')

	status = ""
	status_anwser = re.search('<input type="hidden" id="showsign_status" value="(.*?)" />', status_html)
	if status_anwser:
		status = status_anwser.group(1)

	if status == "1":
		result1 = "今日已经签到过。"
	else:

		sign_url = "http://weixin.dtd365.com/index.php/home/activity/activitysign.html"

		sign_data = {"sign" : "1"}

		sign_post_data = urllib.urlencode(sign_data)

		sign_headers = {	"Referer" : "http://weixin.dtd365.com/index.php/home/activity/showsign.html", \
							"Host" : "weixin.dtd365.com", \
							"Accept" : "*/*", \
							"Origin" : "http://weixin.dtd365.com", \
							"Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8", \
							"X-Requested-With" : "XMLHttpRequest", \
							"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36" \
						}

		sign_request = urllib2.Request(sign_url, sign_post_data, sign_headers)
		sign_response = opener.open(sign_request).read().decode('utf8').encode('gb18030')

		hongbao_anwser = re.search(',"hongbao":"(.*?)"}', sign_response)
		if hongbao_anwser:
			hongbao = hongbao_anwser.group(1)
			result3 = "获得" + hongbao +"元红包。"

		status_html = urllib2.urlopen(status_url).read().decode('utf8').encode('gb18030')

		status_anwser = re.search('<input type="hidden" id="showsign_status" value="(.*?)" />', status_html)
		if status_anwser:
			status = status_anwser.group(1)
			if status == "1":
				result1 = "签到成功。"

	result2 = ""
	total_anwser = re.search('<p>已签到<br><span>(.*?)</span>&nbsp;天</p>', status_html)
	if total_anwser:
		days = total_anwser.group(1)
		result2 = "已签到" + days + "天。"

	result =  result1 + result2 + result3
	print username + " " + result
	status_list.append(str(line_ptr) + " " + result)
	

def change_list(status_list):
	my_status_list = [None] * len(status_list)
	for status in status_list:
		parts = status.split(" ")
		if len(parts) == 2:
			ptr = string.atoi(parts[0])
			my_status_list[ptr] = parts[1]
	return my_status_list


def sign_all(account_list):
	jobs = []
	for i in xrange(len(account_list)):
		job = multiprocessing.Process(target=sign, args=(i, account_list[i][0], account_list[i][1]))
		jobs.append(job)
		job.start()
	for job in jobs:
		job.join()
	return change_list(status_list)


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";

	account_list = []
	for line in file("当天金融账号密码.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			account_list.append([parts[0], parts[1]])

	my_status_list = sign_all(account_list)

	for status in my_status_list:
		print status.encode('gbk')
