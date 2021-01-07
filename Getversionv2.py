import requests
import re
import sys
import urllib3
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random

#python3 Getversion.py url.txt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]

#随机ua
def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua

#获取版本信息
def getversion(url):

	rr=re.compile(r'version":"(.*?)",', re.I)
	headers = {'User-Agent': get_ua()}
	try:
		r=requests.get(url,headers=headers,timeout=15,verify=False)
		if re.search(r'version',r.text):
			str1=rr.findall(r.text)
			if str1:
				print('[+]'+url + '		version:' + str1[0])
			else:
				print('[-]'+url)
	except Exception as e:
		print('[!]%s is timeout' %url)

#多线程
def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(getversion, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':
	show = r'''
	 ______           _                                   _             
	|___  /          | |                                 (_)            
	   / /  ___ _ __ | |_ __ _  ___   __   _____ _ __ ___ _  ___  _ __  
	  / /  / _ \ '_ \| __/ _` |/ _ \  \ \ / / _ \ '__/ __| |/ _ \| '_ \ 
	./ /__|  __/ | | | || (_| | (_) |  \ V /  __/ |  \__ \ | (_) | | | |
	\_____/\___|_| |_|\__\__,_|\___/    \_/ \___|_|  |___/_|\___/|_| |_|
	                                                                    
	                                                                    
                                                        By m2
	'''
	print(show + '\n')
	arg=ArgumentParser(description='ZenTao get version By m2')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
						"--file",
						help="Target URL; Example:url.txt")
	args=arg.parse_args()
	url=args.url
	filename=args.file
	start=time()
	if url != None and filename == None:
		url=parse.urlparse(url)
		url=url.scheme + '://' + url.netloc + '/zentao/index.php?mode=getconfig'
		getversion(url)
	elif url == None and filename != None:
		for i in open(filename):
			i=i.replace('\n','')
			if re.search(r'http',i):
				i=parse.urlparse(i)
				url=i.scheme + '://' + i.netloc + '/zentao/index.php?mode=getconfig'
			else:
				url='http://' + i + '/zentao/index.php?mode=getconfig'
			url_list.append(url)
		multithreading(url_list,10)
	end=time()
	print('任务完成，用时%d' %(end-start))