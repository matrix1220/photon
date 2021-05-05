
message_handlers = []

class MessageHandler:
	def __init_subclass__(handler_class, **kwargs):
		message_handlers.append(handler_class)

	async def handle_message(self, message):
		for handler_class in message_handlers:
			result = await self.router.pass_message(handler_class, message)
			if result: return result


text_message_handlers = []
class TextMessageHandler(MessageHandler):
	def __init_subclass__(handler_class, **kwargs):
		text_message_handlers.append(handler_class)

	async def handle_message(self, message):
		if "text" not in message: return
		self.message = message
		return await self.handle_text(message.text)

	async def handle_text(self, text):
		for handler_class in text_message_handlers:
			result = await self.router.pass_message(handler_class, self.message)
			if result: return result

static_text_message_handlers = {}
class _StaticTextMessageHandler(TextMessageHandler):
	def __init_subclass__(handler_class, **kwargs):
		pass

	async def handle_text(self, text):
		if text not in static_text_message_handlers: return
		result = await self.router.pass_message(static_text_message_handlers[text], self.message)
		if result: return result

class StaticTextMessageHandler(_StaticTextMessageHandler):
	static_text = ''
	def __init_subclass__(handler_class, **kwargs):
		static_text_message_handlers[handler_class.static_text] = handler_class

	async def handle_text(self, text):
		if text==self.static_text: return await self.handle()

	async def handle(self):
		pass
			
#class RegexpTextMessageHandler(TextMessageHandler):
import parse
#from parse import compile as compile_
parse_text_message_handlers = []
class _ParseTextMessageHandler(TextMessageHandler):
	def __init_subclass__(handler_class, **kwargs):
		pass

	async def handle_text(self, text):
		for handler_class in parse_text_message_handlers:
			tmp = handler_class.compiled.parse(text)
			if not tmp: continue
			handler_object = self.router.instantiate(handler_class)
			result = handler_object.handle(*tmp.fixed, **tmp.named)
			if result: return result
			

class ParseTextMessageHandler(_ParseTextMessageHandler):
	parse = ''
	def __init_subclass__(handler_class, **kwargs):
		handler_class.compiled = parse.compile(handler_class.parse)
		parse_text_message_handlers.append(handler_class)

	async def handle_text(self, text):
		tmp = self.compiled.parse(text)
		if tmp: return await self.handle(*tmp.fixed, **tmp.named)
		
	async def handle(self, *args, **kwargs):
		pass

class StartHandler(StaticTextMessageHandler):
	static_text = '/start'
	async def handle(self):
		return await self.router.main_menu()

class StartArgHandler(ParseTextMessageHandler):
	parse = '/start {arg}'
	async def handle(self, arg=None):
		return await self.router.main_menu(arg)