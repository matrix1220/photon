from ..object_dict import objectify, dictify
import requests_async as requests

from .message_queue import QueuedMessage, MessageQueue
from .request import Request, request

import asyncio
import logging
logger = logging.getLogger(__name__)

class Bot:
	def __init__(self, token):
		self._token = token
		self.message_queue = MessageQueue(self)


	async def _send(self, method, args={}):
		logger.debug([method, args])
		result = await requests.post('https://api.telegram.org/bot' + self._token + '/' + method, json=args)
		data = objectify(result.json())
		logger.debug(data)

		if not data.ok:
			logger.error(data.description)
			raise Exception(data.description, data.error_code)
		return data.result

	async def _send_response(self, response):
		if not response: return
		return await self._send(response.pop('method'), response)

	async def long_polling(self, handler=None, skip_updates=True):
		offset = None
		if skip_updates:
			while offset==None:
				offset = await self._handle_updates(handler, offset=-1, timeout=30)
		else:
			while offset==None:
				offset = await self._handle_updates(handler, timeout=30)

		while True:
			tmp = await self._handle_updates(handler, offset=offset + 1, timeout=30)
			if tmp: offset = tmp

		# for update in await self.getUpdates(offset=-1):
		# 	offset = update.update_id

	async def _handle_updates(self, handler, **kwargs):
		offset = None
		try:
			updates = await self.getUpdates(**kwargs)
		except Exception as e:
			logging.exception(e)
			return 

		for update in updates:
			offset = update.update_id
			asyncio.create_task(self._handle_update(handler, update))
			

		return offset

	async def _handle_update(self, handler, update):
		try:
			temp = await handler(update)
			if not temp: return
			if not isinstance(temp, Request): return
			await temp
		except Exception as e:
			logging.exception(e)


	def __getattr__(self, key):
		def function(*args, **kwargs):
			return request(self, key, args, kwargs)
		return function
		#return lambda *args, **kwargs: await Request(key, args, kwargs, self)