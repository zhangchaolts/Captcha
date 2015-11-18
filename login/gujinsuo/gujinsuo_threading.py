#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import recognizer_gjs.recognizer
import string
import threading

class Gujinsuo(threading.Thread):

	def __init__(self, username, password, line_ptr):
		threading.Thread.__init__(self)
		self.username = username
		self.password = password
		self.line_ptr = line_ptr
		self.status = None
		self.cj = None
		self.opener = None

	def run(self):
		# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
		self.cj = cookielib.CookieJar()
		# �Զ���opener,����opener��CookieJar�����
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		# ��װopener
		urllib2.install_opener(self.opener)

		is_logined = False
		try_times = 0

		while try_times < 3:
			print 'try_times:' + str(try_times)
		
			try_times += 1

			# Step1:ʶ����֤��
			url = "https://www.gujinsuo.com.cn/login.html"
			html = urllib2.urlopen(url).read()

			fw = open('captcha_gjs_' +str(self.line_ptr) + '.jpg', 'wb+')
			content = urllib2.urlopen('https://www.gujinsuo.com.cn/auth/random?_=' + str(int(time.mktime(datetime.datetime.now().timetuple()))) + '000').read()
			fw.write(content)
			fw.close()

			#randcode = recognizer_gjs.recognizer.recognize('captcha_gjs_' +str(self.line_ptr) + '.jpg', 'pics_train_gjs')
			randcode = "111111"
			print "randcode:" + randcode

			# Step2:��¼
			login_url = "https://www.gujinsuo.com.cn/login"

			login_data = {	"username": self.username, \
							"password": self.password, \
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

			login_response = self.opener.open(login_request).read().decode('utf8').encode('gb18030')

			login_info = ""
			login_anwser = re.search('"message" : "(.*?)",', login_response)
			if login_anwser:
				login_info = login_anwser.group(1)
				if login_info.find("���ѳɹ���¼��ϵͳ!") != False and login_info.find("��֤���������!") != False and login_info.find("��������֤��!") != False:
					#print login_info + "\n"
					return "��¼ʧ�ܣ�"

			homepage_url = "https://www.gujinsuo.com.cn/member/main.html";
			homepage_html = urllib2.urlopen(homepage_url).read().decode('utf8').encode('gb18030')
			#print homepage_html

			if homepage_html.find('��ȫ�˳�') == -1:
				#print "��" + str(try_times) +"��ʶ����֤����󣬵�¼ʧ��..."
				continue
			else:
				#print "��¼�ɹ�!"
				is_logined = True
				break

		if is_logined == False:
			#print "����20�ζ���½ʧ�ܣ���������Ϊ���ˣ����������ֶ�ǩ����~\n"
			return "��¼ʧ�ܣ�����20�ζ���½ʧ�ܣ�"

		print "��ʼǩ��..." 

		# Step3:ǩ��
		sign_url = "https://www.gujinsuo.com.cn/spread/sign?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
		sign_request = urllib2.Request(sign_url)
		sign_response = self.opener.open(sign_request).read().decode('utf8').encode('gb18030')

		result1 = ""

		gainPopularity = ""
		sign_anwser = re.search('���ѳɹ�ǩ��,ϵͳ����(.*?)Ԫ�ĺ��', sign_response)
		if sign_anwser:
			gainPopularity = sign_anwser.group(1)
			result1 = "����ǩ�����" + gainPopularity + "Ԫ�����"
		else:
			result1 = "�����Ѿ�ǩ������"

		# Step4
		home_url = "https://www.gujinsuo.com.cn/spread/mywefares?start=0&limit=10&_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
		#home_html = urllib2.urlopen(home_url).read()
		home_request = urllib2.Request(home_url)
		home_html = self.opener.open(home_request).read()

		result2 = ""
		totalPopularity = ""
		home_anwser = re.search('"unused" : (.*?),', home_html)
		if home_anwser:
			totalPopularity = home_anwser.group(1)
			result2 = "�ܺ��Ϊ" + totalPopularity + "��"

		result = result1 + result2

		self.status = result

if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	print "\n��" + datetime.datetime.now().strftime("%Y-%m-%d") + "��";

	threads = []

	line_ptr = 0
	for line in file("�̽����˺�����.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			threads.append(Gujinsuo(parts[0], parts[1], line_ptr))
			line_ptr += 1

	for t in threads:
		t.start()

	for t in threads:
		t.join()

	for t in threads:
		print t.username + "\tfail"
		#print t.username + "\t" + t.status


