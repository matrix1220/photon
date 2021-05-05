

from ..menu import menu_classes
from ..message_handler import MessageHandler
from ..client import Request
from .. import globals_

from .result import Result, Incorrect, Done
from .misc import catch, catch_request, catch_result

from .menu_router import MenuRouter
from .inline_menu_router import InlineMenuRouter
from .message_handler_router import MessageHandlerRouter

class Router(
	MenuRouter,
	InlineMenuRouter,
	MessageHandlerRouter
):
	def __init__(self, menu_stack, keyboard=None, kwargs={}):
		self.menu_stack = menu_stack
		self.keyboard = keyboard
		self.kwargs = kwargs
		for x, y in self.kwargs.items():
			setattr(self, x, y)

	def instantiate(self, menu_class):
		menu_object = menu_class()
		menu_object.router = self
		for x, y in self.kwargs.items():
			setattr(menu_object, x, y)
		return menu_object

	async def act(self, menu_class, *args, **kwargs):
		menu_object = self.instantiate(menu_class)
		result = await catch_request(menu_object.act, *args, **kwargs)
		self.menu_stack.push(menu_class._menu_id, args, kwargs)
		raise Done(result)

	async def explicit_act(self, menu_class, *args, **kwargs):
		menu_object = self.instantiate(menu_class)
		result = await catch_request(menu_object.act, *args, **kwargs)
		self.menu_stack.set_current(menu_class._menu_id, args, kwargs)
		raise Done(result)

	async def back(self):
		self.menu_stack.pop()
		if self.menu_stack.empty():
			return await self.main_menu()
		menu_class, args, kwargs = self.menu_stack.current()
		return await self.explicit_act(menu_class, *args, **kwargs)

	async def handle_message(self, message):
		result = await self.pass_message(MessageHandler, message)
		if result: return result
		return await self.handle_menu(message)