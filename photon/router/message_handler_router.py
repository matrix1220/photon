
from .misc import catch

class MessageHandlerRouter:
	async def pass_message(self, handler_class, message):
		handler_object = self.instantiate(handler_class)
		return await catch(handler_object.handle_message, message)

