
from . import Request, Result

async def catch(func, *args, **kwargs):
	try:
		result = await func(*args, **kwargs)
		if isinstance(result, Result):
			result = result.arg
	except Request as e:
		return e
	except Result as e:
		result = e.arg

	if isinstance(result, dict):
		return Request.from_response(globals_.bot, result)

	return result

# async def feed(func, data, *args, **kwargs):
# 	result = await func(*args, **kwargs)
# 	if isinstance(result, Request):
# 		result.feed(**data)

# 	return result


async def catch_request(func, *args, **kwargs):
	try:
		result = await func(*args, **kwargs)
	except Request as e:
		return e

	if isinstance(result, dict):
		return Request.from_response(globals_.bot, result)

	return result

async def catch_result(func, *args, **kwargs):
	try:
		result = await func(*args, **kwargs)
	except Result as e:
		return e.arg

	if isinstance(result, Result):
		return result.arg

	return result