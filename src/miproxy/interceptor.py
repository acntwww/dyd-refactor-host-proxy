#!/usr/bin/env python
# coding=utf-8

# import proxy

class InterceptorPlugin(object):
	def __init__(self, server, msg):
		self.server = server
		self.msg = msg

class RequestInterceptorPlugin(InterceptorPlugin):

	def do_request(self, data):
		return data

	
class ResponseInterceptorPlugin(InterceptorPlugin):

	def do_response(self, data):
		return data

class InvalidInterceptorPluginException(Exception):
	pass

class DebugInterceptor(RequestInterceptorPlugin, ResponseInterceptorPlugin):
	
	def do_request(self, data):
		#print '>> %s' % repr(type(data))
		return data

	def do_response(self, data):
		return data