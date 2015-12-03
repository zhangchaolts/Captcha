#coding=gbk

import sys
import urllib
import urllib2
import cookielib
import re
import time,datetime
import recognizer_gjs.recognizer
import multiprocessing

class Gujinsuo(multiprocessing.Process):
	
	def __init__(self, line_ptr, username, password):
		multiprocessing.Process.__init__(self)
		self.line_ptr = line_ptr
		self.username = username
		self.password = password
		self.status = None

	def run(self):
		# ��ȡCookiejar���󣨴��ڱ�����cookie��Ϣ��
		cj = cookielib.CookieJar()
		# �Զ���opener,����opener��CookieJar�����
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		# ��װopener,�˺����urlopen()ʱ����ʹ�ð�װ����opener����
		urllib2.install_opener(opener)

		#print "�û� " + username + " ������..."

		is_logined = False
		try_times = 0

		while try_times < 20:

			try_times += 1

			# Step1:ʶ����֤��
			url = "https://www.gujinsuo.com.cn/login.html"
			html = urllib2.urlopen(url).read()

			fw = open('pics_captcha_gjs/' + str(self.line_ptr) + '.jpg', 'wb+')
			content = urllib2.urlopen('https://www.gujinsuo.com.cn/auth/random?_=' + str(int(time.mktime(datetime.datetime.now().timetuple()))) + '000').read()
			fw.write(content)
			fw.close()

			randcode = recognizer_gjs.recognizer.recognize('pics_captcha_gjs/' + str(self.line_ptr) + '.jpg', 'pics_train_gjs')
			print str(self.line_ptr) + " randcode:" + randcode

			# Step2:��¼
			login_url = "https://www.gujinsuo.com.cn/login"

			login_data = {	"username": self.username, \
							"password": self.password, \
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

		#print "��ʼǩ��..." 

		# Step3:ǩ��
		sign_url = "https://www.gujinsuo.com.cn/spread/sign?_=" + str(int(time.mktime(datetime.datetime.now().timetuple()))) + "000"
		sign_request = urllib2.Request(sign_url)
		sign_response = opener.open(sign_request).read().decode('utf8').encode('gb18030')

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
		home_html = urllib2.urlopen(home_url).read()

		result2 = ""
		totalPopularity = ""
		home_anwser = re.search('"unused" : (.*?),', home_html)
		if home_anwser:
			totalPopularity = home_anwser.group(1)
			result2 = "�ܺ��Ϊ" + totalPopularity + "��"

		result = result1 + result2
		print str(self.line_ptr) + "\t" + result
		self.status = result

if __name__ == '__main__':

	reload(sys)
	sys.setdefaultencoding("gbk")

	username_array = []
	password_array = []

	for line in file("�̽����˺�����.txt"):
		line = line.strip()
		parts = line.split(" ")
		if len(parts) == 2:
			username_array.append(parts[0])
			password_array.append(parts[1])

	print "\n��" + datetime.datetime.now().strftime("%Y-%m-%d") + "��";

	record = []

	for i in range(len(username_array)):
		record.append(Gujinsuo(i, username_array[i], password_array[i]))

	for process in record:
		process.start()

	for process in record:
		process.join()

	for process in record:
		print process.username
		print process.status   #����ֵ����⣬��֪��Ϊ�δ�ӡ�����Ķ�ΪNone