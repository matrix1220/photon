

from .client import unserialize_callback_data

class Context:
	def __init__(self):
		self.commit_list = []

	def _append_commit_list(self, item):
		self.commit_list.append(item)

	def commit(self):
		for item in self.commit_list:
			item.commit()

	def instantiate(self, class_, args = [], kwargs = {}):
		object_ = class_(self)
		object_._init(*args, **kwargs)
		#object_.context_manager = self.manager

		return object_

	async def handle_message(self, message):
		# result = await self.pass_message(_MessageHandler, message)
		# if result: return result
		return await self.handle_outline_menu(message)

	async def handle_callback_query(self, callback_query):
		if data := callback_query.data:
			callback_query.data = unserialize_callback_data(data)
			return await self.handle_inline_menu(callback_query)
			#menu_object = self.instantiate(menu_classes[data.pop(0)])
			#return await catch_request(handler.handle_callback, [callback_query, data])
	
	async def handle_update(self, update):
		# bug
		for x in ["message", "callback_query"]:
			if x not in update: continue
			return await getattr(self, f"handle_{x}")(update[x])


