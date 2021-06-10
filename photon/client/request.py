from ..utils import format

class Request(Exception):
	def __init__(self, method, data):
		self.bot = None
		self.method = method
		self.data = data

	def set_bot(self, bot):
		self.bot = bot
		return self

	def feed(self, **kwargs):
		self.data = format(self.data, **kwargs)

	async def exec(self):
		if not self.bot: raise Exception("bot is not set")
		return await self.bot._send(self.method, self.data)

	def __await__(self):
		return self.exec().__await__()

	@classmethod
	def from_response(cls, response):
		if "method" in response:
			return Request(response.pop('method'), response)
		return response

	def as_response(self):
		return {"method":self.method, **self.data}

from . import _methods

def request(method, args, kwargs):
	if hasattr(_methods, method):
		return getattr(_methods, method)(*args, **kwargs)
	else:
		return Request(method, kwargs)