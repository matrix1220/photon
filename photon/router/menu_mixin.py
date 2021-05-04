
from . import Request
from . import globals_

from .misc import catch_request, catch_result
from .result import Result, Incorrect, Done

import re

class MenuMixin:
	async def act(self, menu_class, *args, **kwargs):
		menu_object = self.instantiate(menu_class)
		result = await catch_request(menu_object.act, *args, **kwargs)

		self.menu_stack.push(menu_class._menu_id, args, kwargs)

		raise Done(result)

	async def explicit_act(self, menu_class, *args, **kwargs):
		menu_object = self.instantiate(menu_class)
		result = await catch_request(menu_object.act, *args, **kwargs)

		self.menu_stack.set_current(menu_class._menu_id, args, kwargs)
		#self.db.commit()
		raise Done(result)

	async def main_menu(self, arg=None):
		self.menu_stack.reset()
		return await self.explicit_act(globals_.main_menu, arg=arg)

	async def back(self):
		self.menu_stack.pop()
		if self.menu_stack.empty_menu():
			return await self.main_menu()
		menu_class, args, kwargs = self.menu_stack.current()
		return await self.explicit_act(menu_class, *args, **kwargs)



	async def _handle_message(self, message):
		result = None
		if text := message.text:
			if text == "/start":
				return await self.main_menu()
			elif match:=re.match(r"\A/start (.+)", text):
				return await self.main_menu(match.group(1))

			if self.menu_stack.empty(): 
				return await self.main_menu()

			result = await self.handle_text(text)

		if self.menu_stack.empty():
			return await self.main_menu()
		
		if video := message.video:
			result = await self.handle_video(video)

		if result:
			return result

		menu_object = self.instantiate(self.menu_stack.current_menu())
		return await catch_request(menu_object.handle_message, message)

	async def handle_message(self, message):
		result = await catch_result(self._handle_message, message)
		# if isinstance(result, str):
		# 	return Request(globals_.bot, )
		return result

	async def handle_text(self, text):
		menu_object = self.instantiate(self.menu_stack.current_menu())
		return await catch_request(menu_object.handle_text, text)

	async def handle_video(self, video):
		menu_object = self.instantiate(self.menu_stack.current_menu())
		return await catch_request(menu_object.handle_video, video)