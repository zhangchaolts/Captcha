#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime

#sys.path.append("/search/zhangchao/captcha/deal_pics/deal_gujinsuo/")
import recognizer

FW_LOG = open("result.txt", "w")

def sign(username, password):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	print "用户 " + username + " 进行中..."
	print "开始登陆..."

	is_logined = False
	try_times = 0

	while try_times < 20:

		try_times += 1

		# Step1:识别验证码
		url = "https://www.gujinsuo.com.cn/login.html"
		html = urllib2.urlopen(url).read()

		fw = open('captcha.jpg', 'wb+')
		content = urllib2.urlopen('https://www.gujinsuo.com.cn/auth/random?_=' + str(int(time.mktime(datetime.datetime.now().timetuple()))) + '000').read()
		fw.write(content)
		fw.close()

		randcode = recognizer.recognize('captcha.jpg', 'pics_train')
		#print "randcode:" + randcode

		# Step2:登录
		login_url = "https://www.gujinsuo.com.cn/login"

		login_data = {	"username": username, \
						"password": password, \
						"randcode": randcode \
					}

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

		login_info = ""
		login_anwser = re.search('"message" : "(.*?)",', login_response)
		if login_anwser:
			login_info = login_anwser.group(1)
			if login_info.find("您已成功登录本系统!") != False and login_info.find("验证码输入错误!") != False and login_info.find("请输入验证码!") != False:
				print login_info + "\n"
				return

		homepage_url = "https://www.gujinsuo.com.cn/member/main.html";
		homepage_html = urllib2.urlopen(homepage_url).read().decode('utf8').encode('gb18030')
		#print homepage_html

		if homepage_html.find('安全退出') == -1:
			print "第" + str(try_times) +"次识别验证码错误，登录失败..."
			continue
		else:
			print "登录成功!"
			is_logined = True
			break

	if is_logined == False:
		print "尝试20次都登陆失败，程序无能为力了，大侠还是手动签到吧~\n"
		FW_LOG.write(username + "\n")
		return

	print "开始签到..." 

	# Step3:签到
	sign_url = "https://www.gujinsuo.com.cn/spread/sign?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
	sign_request = urllib2.Request(sign_url)
	sign_response = opener.open(sign_request).read()

	sign_info = ""
	sign_anwser = re.search('"message" : "(.*?)",', sign_response)
	if sign_anwser:
		sign_info = sign_anwser.group(1).decode("utf8").encode("gbk")
		print sign_info + "\n"
	else:
		print "今日已经签到过!\n"


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	timestamp_now_date = time.mktime(datetime.datetime.now().timetuple())
	timestamp_expired_date = time.mktime(time.strptime("2015-12-01 00:00:00", '%Y-%m-%d %H:%M:%S'))
	if timestamp_now_date >= timestamp_expired_date:
		print "程序过期，请重新下载"
		time.sleep(3)
		sys.exit(0)

	username_array = []
	password_array = []

	for line in file("gujinsuo.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			username_array.append(parts[0])
			password_array.append(parts[1])

	print "\n【" + datetime.datetime.now().strftime("%Y-%m-%d") + "】";

	FW_LOG.write("%s 登陆失败的账号如下：\n" % datetime.datetime.now().strftime("%Y-%m-%d"))

	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])
 
	print "\n程序执行结束，窗口即将关闭！"
	time.sleep(2)
