
from .client import Bot as Bot_
from .client import Request

import asyncio
import logging


from .menu import MenuStack
#from .context import Context
#from .menu.menu_context import InlineMenuContext, OutlineMenuContext
from .context_manager import ContextManager


class Bot(Bot_):
	def __init__(self, token):
		super().__init__(token)
		self.handlers = []
	
	def set_main_menu(self, main_menu_):
		self.main_menu = main_menu_
		return main_menu_

	async def long_polling(self, skip_updates=True):
		async for update in Bot_.long_polling(self, skip_updates):
			await self._handle_update(update)
			#asyncio.create_task(self._handle_update(update))

	async def _handle_update(self, update):
		try:
			for handler in self.handlers:
				temp = await handler(update)
				#print(temp)
				if not temp: return
				if not isinstance(temp, Request): return
				await temp
		except Exception as e:
			logging.exception(e)

	def webhook(self, url):
		pass