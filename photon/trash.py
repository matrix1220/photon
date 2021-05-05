#class User:
	# def __init__(self):
	# 	self.menu_stack = MenuStack()

	# @classmethod
	# def find(cls, user_id):
	# 	raise NotImplemented

	# def __init_subclass__(cls, **kwargs):
	# 	_globals.User = cls

	# def passes(self):
	# 	self._passes = True

	# import virtualmod
# from .client import request
# _methods = virtualmod.create_module('photon.methods')
# def _tmp(key):
# 	def function(*args, **kwargs):
# 		return request(globals_.bot, key, args, kwargs)
# 	return function

# _methods.__getattr__ = _tmp

# try:
# 	from config import bot
# except ImportError:
# 	bot = None

# try:
# 	from router import find_router
# except ImportError:
# 	find_router = None

# try:
# 	from senario import MainMenu as main_menu
# except ImportError:
# 	main_menu = None

# def set(bot_, find_router_, main_menu_):
# 	nonlocal bot, find_router, main_menu
# 	bot, find_router, main_menu = bot_, find_router_, main_menu_