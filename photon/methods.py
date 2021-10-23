
from .client import request

def __getattr__(key):
	# def function(*args, **kwargs):
	# 	return request(key, args, kwargs)
	# return function
	return lambda *args, **kwargs: request(key, args, kwargs)

__path__ = None