from .client import Request

class Result(Exception):
	def __init__(self, arg=None):
		self.arg = arg

class Incorrect(Result):
	pass

class Done(Result):
	pass


async def catch(func, *args, **kwargs):
	try:
		result = await func(*args, **kwargs)
		if isinstance(result, Result):
			result = result.arg
	except Request as e:
		return e
	except Result as e:
		result = e.arg

	return result

async def catch_request(func, *args, **kwargs):
	try:
		result = await func(*args, **kwargs)
	except Request as e:
		return e

	return result

async def catch_result(func, *args, **kwargs):
	try:
		result = await func(*args, **kwargs)
		if isinstance(result, Result):
			result = result.arg
	except Result as e:
		return e.arg

	return result