from ..utils import format

class Request(Exception):
	def __init__(self, method, data):
		self.bot = None
		self.method = method
		self.data = data

	def feed(self, **kwargs):
		self.data = format(self.data, **kwargs)

	async def exec(self, bot=None):
		if bot:
			return await bot._send_request(self)
		elif self.bot:
			return await self.bot._send_request(self)
		
		raise Exception("Undefined bot")

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