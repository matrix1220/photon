from ..object_dict import objectify, dictify
import requests_async as requests

from .message_queue import QueuedMessage, MessageQueue
from .request import Request, request

import asyncio
import logging
logger = logging.getLogger(__name__)

#from . import methods_

class Bot:
	def __init__(self, token):
		self.token = token
		self.message_queue = MessageQueue(self)
		#self.session = requests.Session()

	async def _send(self, method, args={}):
		logger.debug([method, args])
		#self.session
		result = await requests.post(f'https://api.telegram.org/bot{self.token}/{method}', json=args)
		data = objectify(result.json())
		logger.debug(data)

		if not data.ok:
			logger.error(data.description)
			raise Exception(data.description, data.error_code)
		return data.result

	async def _send_response(self, response):
		if not response: return
		return await self._send(response.pop('method'), response)

	async def long_polling(self, skip_updates=True):
		offset = None
		if skip_updates:
			kwargs = dict(offset=-1, timeout=30)
		else:
			kwargs = dict(timeout=30)

		while offset==None:
			async for update in self.safeGetUpdates(**kwargs):
				offset = update.update_id
				yield update

		while True:
			async for update in self.safeGetUpdates(offset=offset + 1, timeout=30):
				offset = update.update_id
				yield update

	async def safeGetUpdates(self, **kwargs):
		try:
			updates = await self.getUpdates(**kwargs)
		except Exception as e:
			logger.exception(e)
			await asyncio.sleep(1)
			return 

		for update in updates:
			yield update


	def __getattr__(self, key):
		# def function(*args, **kwargs):
		# 	return request(key, args, kwargs).set_bot(self)
		# return function
		return lambda *args, **kwargs: request(key, args, kwargs).set_bot(self)
