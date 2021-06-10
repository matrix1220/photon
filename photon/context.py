


import json

class Context:
	# def __init__(self, metadata):
	# 	self.metadata = metadata

	def close(self):
		#self.manager.save(self)
		pass

	def instantiate(self, class_):
		object_ = class_()
		object_.context = self
		object_.bot = self.bot
		#object_.context_manager = self.manager

		return object_

	async def handle_message(self, message):
		# result = await self.pass_message(_MessageHandler, message)
		# if result: return result
		return await self.handle_outline_menu(message)

	async def handle_callback_query(self, callback_query):
		if data := callback_query.data:
			callback_query.data = json.loads(data)
			return await self.handle_inline_menu(callback_query)
			#menu_object = self.instantiate(menu_classes[data.pop(0)])
			#return await catch_request(handler.handle_callback, [callback_query, data])
	
	async def handle_update(self, update):
		for x in ["message", "callback_query"]:
			if x not in update: continue
			return await getattr(self, f"handle_{x}")(update[x])


