
from . import globals_

from .misc import catch_request, catch_result
from .result import Result, Incorrect, Done

class InlineMenuRouter:
	async def handle_callback(self, callback_query):
		if data := callback_query.data:
			data = json.loads(data)
			menu_object = self.instantiate(menu_classes[data.pop(0)])
			return await catch_request(handler.handle_callback, [callback_query, data])