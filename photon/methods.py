
from . import globals_
from .client import request

def __getattr__(key):
	def function(*args, **kwargs):
		return request(globals_.bot, key, args, kwargs)
	return function

__path__ = None