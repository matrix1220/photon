
from .client import Bot as Bot_
from .client import Request

import asyncio
import logging


from .menu import MenuStack
#from .context import Context
#from .menu.menu_context import InlineMenuContext, OutlineMenuContext
from .context_manager import ContextManager

class Ctx:
	pass

class Bot(Bot_):
	def __init__(self, token):
		super().__init__(token)
		self.handlers = []
		self.middlewares = []

	async def long_polling(self, skip_updates=True):
		async for update in Bot_.long_polling(self, skip_updates):
			ctx = Ctx()
			ctx.bot = self
			ctx.update = update
			temp = await self._next(iter(self.middlewares))(ctx)
			await self._send_request(temp)
			#asyncio.create_task(self._handle_update(update))

	def _next(self, iter_):
		try:
			next_iter = next(iter_)
			#next_ = self._next(iter_)
			async def func(ctx):
				next_ = self._next(iter_)
				return await next_iter(next_, ctx)
		except StopIteration:
			next_iter = self._handle
			async def func(ctx):
				return await next_iter(ctx)

		return func

	async def _handle(self, ctx):
		for handler in self.handlers:
			try:
				temp = await handler(ctx)
			except Exception as e:
				logging.exception(e)
			
			if not temp: continue
			return temp
	

	def webhook(self, url):
		pass