
from .client import Bot as Bot_
from .client import Request

import asyncio
import logging


from .menu import MenuStack
#from .context import Context
#from .menu.menu_context import InlineMenuContext, OutlineMenuContext
from .context_manager import ContextManager


class Bot(Bot_):
	def __init__(self, token, context_manager=None):
		super().__init__(token)
		if context_manager==None:
			self.context_manager = ContextManager()
		else:
			self.context_manager = context_manager

		self.context_manager.bot = self

		self.handler = self.context_manager.handle_update
		#self.context_manager = self._new_context_manager()

	# def _new_context_manager(self):
	# 	self.context_manager = ContextManager(self)
	
	def set_main_menu(self, main_menu_):
		self.main_menu = main_menu_
		return main_menu_

	async def long_polling(self, skip_updates=True):
		async for update in Bot_.long_polling(self, skip_updates):
			await self._handle_update(update)
			#asyncio.create_task(self._handle_update(update))

	async def _handle_update(self, update):
		try:
			temp = await self.handler(update)
			#print(temp)
			if not temp: return
			if not isinstance(temp, Request): return
			await temp
		except Exception as e:
			logging.exception(e)

	def webhook(self, url):
		pass

	# def handler(self, update):
	# 	context_metadata = self.context_manager.parse_metadata(update)
	# 	if not context_metadata: return
	# 	context = self.context_manager.find(**context_metadata)
	# 	request = context.handle_update(update)
	# 	context.close()
	# 	return request