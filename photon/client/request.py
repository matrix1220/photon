

class Request(Exception):
	def __init__(self, bot, method, kwargs):
		self.bot = bot
		self.method = method
		self.data = kwargs

	def feed(self, data):
		pass

	async def exec(self):
		return await self.bot._send(self.method, self.data)

	def __await__(self):
		return self.exec().__await__()

	@classmethod
	def from_response(cls, bot, response):
		if "method" in response:
			return Request(bot, response.pop('method'), response)
		return response

	def as_response(self):
		return {"method":self.method, **self.data}

from . import methods

def request(bot, method, args, kwargs):
	if hasattr(methods, method):
		return getattr(methods, method)(bot, *args, **kwargs)
	else:
		return Request(bot, method, kwargs)