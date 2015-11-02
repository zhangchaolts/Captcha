#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime

sys.path.append("/search/zhangchao/captcha/deal_pics/deal_yirendai/")
import recognizer

class RedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		pass
	def http_error_302(self, req, fp, code, msg, headers):
		pass

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers) 
		result.status = code
		print result
		return result
	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers) 
		result.status = code
		print result
		return result

cookiemap = {}

def cookiestring(cookiemap):
	str = ""
	for key, value in cookiemap.items():
		str += key + "=" + value + "; "
	if len(str) >= 2:
		str = str[:-2]
	return str

class SaveCookieRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		setcookie = str(headers["Set-Cookie"])
		cookieTokens = ["Domain","Expires", "Path", "Max-Age"]
		tokens = setcookie.split(";")
		for cookie in tokens:
			cookie = cookie.strip()
			if cookie.startswith("Expires="):
				cookies = cookie.split(",", 2)
				if len(cookies) > 2:
					cookie = cookies[2]
					cookie = cookie.strip()
			else :
				cookies = cookie.split(",", 1)
				if len(cookies) > 1:
					cookie = cookies[1]
					cookie = cookie.strip()
			namevalue = cookie.split("=", 1)
			if len(namevalue) > 1:
				name = namevalue[0]
				value = namevalue[1]
				if name not in cookieTokens:
					cookiemap[name] = value
		print cookiemap
		newcookie = cookiestring(cookiemap)
		print newcookie
		req.add_header("Cookie", newcookie)
		return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

def sign(username, password):

	# 获取Cookiejar对象（存在本机的cookie消息）
	cj = cookielib.CookieJar()
	#httpHandler = urllib2.HTTPHandler(debuglevel=1)
	#httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
	# 自定义opener,并将opener跟CookieJar对象绑定
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), RedirectHandler)
	# 安装opener,此后调用urlopen()时都会使用安装过的opener对象
	urllib2.install_opener(opener)

	# Step1
	url = 'https://www.yirendai.com/auth/login/home'
	html = urllib2.urlopen(url).read()

	content = urllib2.urlopen('https://p.yixin.com/randomCode?t=').read()
	fw = open('temp.jpg', 'w+')
	fw.write(content)
	fw.close()

	dir_train_pics = '/search/zhangchao/captcha/pics/yirendai/train_pics'
	authcode = '1234'
	authcode = recognizer.recognize('temp.jpg', dir_train_pics)

	print "recognize captcha done!"

	# Step2:登录
	login_url = "https://p.yixin.com/dologin.jhtml"

	login_data = {	"fromSite" : "YRD", \
					"username": username, \
					"password": password, \
					"authcode": authcode, \
					"rememberMe": "0" \
				}

	login_post_data = urllib.urlencode(login_data) 

	login_headers = {	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
						"Accept-Encoding" : "gzip, deflate", \
						"Accept-Language" : "zh-CN,zh;q=0.8", \
						"Cache-Control" : "max-age=0", \
						"Connection" : "keep-alive", \
						"Content-Length" : "82", \
						"Content-Type" : "application/x-www-form-urlencoded", \
						#"X-Requested-With" : "XMLHttpRequest", \
						"Host" : "p.yixin.com", \
						"HTTPS" : "1", \
						"Origin" : "https://www.yirendai.com", \
						"Referer" : "https://www.yirendai.com/auth/login/home", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36 QQBrowser/9.0.3100.400" \
					}

	login_request = urllib2.Request(login_url, login_post_data, login_headers)
	#login_request.get_method = lambda: 'HEAD'

	location = ""

	try:
		login_response = opener.open(login_request).read()
	except urllib2.URLError, e:
		location = e.hdrs['Location']
		print location

	second_data = {}

	second_post_data = urllib.urlencode(second_data) 

	second_headers = {	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", \
						"Accept-Encoding" : "gzip, deflate, sdch", \
						"Accept-Language" : "zh-CN,zh;q=0.8", \
						"Cache-Control" : "max-age=0", \
						"Connection" : "keep-alive", \
						"Host" : "www.yixin.com", \
						"HTTPS" : "1", \
						"Referer" : "https://www.yirendai.com/auth/login/home", \
						"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.69 Safari/537.36 QQBrowser/9.0.3100.400" \
						}

	location2 = ""

	try:
		second_response = urllib2.urlopen(location).read()
	except urllib2.URLError, e:
		location2 = e.hdrs['Location']
		print location2

	third_response = urllib2.urlopen(location2).read()
	#print third_response

	if third_response.find("zhangchao822") != -1:
		print "login successfully!"

	#print error_info
	#print login_response.headers
	
	#login_response = opener.open(login_request).read()
	#print "login_response:"
	#print login_response


if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = ["18211085003"]
	password_array = ["csujk4236238"]

	for i in range(len(username_array)):
		sign(username_array[i], password_array[i])

