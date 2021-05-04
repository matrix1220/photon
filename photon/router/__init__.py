

from ..menu import menu_classes
from ..client import Request
from .. import globals_

from .result import Result, Incorrect, Done
from .misc import catch_request, catch_result
from .menu_mixin import MenuMixin

class Router(MenuMixin):
	def __init__(self, menu_stack=None, **kwargs):
		self.menu_stack = menu_stack
		self.kwargs = kwargs
		for x, y in self.kwargs.items():
			setattr(self, x, y)

	def instantiate(self, menu_class):
		menu_object = menu_class()
		menu_object.router = self
		for x, y in self.kwargs.items():
			setattr(menu_object, x, y)
		return menu_object

	async def handle_callback(self, callback_query):
		if data := callback_query.data:
			data = json.loads(data)
			menu_object = self.instantiate(menu_classes[data.pop(0)])
			return await catch_request(handler.handle_callback, [callback_query, data])