
#from . import Request
from . import globals_

from .misc import catch
from .result import Result, Incorrect, Done

import re

class MenuRouter:
	async def main_menu(self, arg=None):
		self.menu_stack.reset()
		return await self.explicit_act(globals_.main_menu, arg=arg)

	async def handle_menu(self, message):
		result = None
		if self.menu_stack.empty():
			return await self.main_menu()

		for x in ['text', 'video']:
			if x not in message: continue
			result = await getattr(self, f"handle_{x}")(message[x])

		if result: return result

		menu_object = self.instantiate(self.menu_stack.current_menu())
		return await catch(menu_object.handle_message, message)

	async def handle_text(self, text):
		menu_object = self.instantiate(self.menu_stack.current_menu())
		return await catch(menu_object.handle_text, text)

	async def handle_video(self, video):
		menu_object = self.instantiate(self.menu_stack.current_menu())
		return await catch(menu_object.handle_video, video)