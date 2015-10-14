# coding=utf-8
from interceptor import *
from urlparse import parse_qs
import sys

try:
	from http_parser.parser import HttpParser
except Exception, e:
	from http_parser.pyparser import HttpParser


class HostInterceptor(RequestInterceptorPlugin, ResponseInterceptorPlugin):
	"""对请求进行过滤,并且将数据我们需要的数据记录下来
	"""

	expacted_keys = set(
			('dydtimestamp','_dydphonedevice',
			'_dydphoneversion', '_dyduniquetag', 'dydmethodname',
			'version', 'deviceType', 'pkg', 'appid', 'dydsign'
			)
		)

	def is_dyd_host(sefl, host):
		hosts = ['192.168.17.201:8003','test.dianyadian.com']
		return host in hosts

	def do_request(self, data):
		p = HttpParser()
		
		host = self.msg.hostname + ":" +str(self.msg.port)
		print '>>HttpParser: ', host
		if self.is_dyd_host(host):
			size = len(data)
			p.execute(data, size)
			path = p.get_path()
			body = p.recv_body()
			query = parse_qs(body)
			keys = set(query.keys())
			if not self.expacted_keys.issubset(keys):
				item = '-'*10 + path + '-'*10
				item += '\n'
				item += ', '.join(keys)
				item += '\n' + '='*40 + '\r\n'
				with open('api.txt','a') as fp:
					fp.write(item)

				print >> sys.stderr, '>>HostInterceptor: ' + path  + 'params not OK'
			print '>>HttpParser: ' + repr(query)
		
		return data

	def do_response(self, data):
		return data