from .request import Request
import asyncio

def keyboard_helper(data):
	if "keyboard" in data:
		data['reply_markup'] = {"keyboard":data["keyboard"], "resize_keyboard":True}
		del data["keyboard" ]
		return

	for x in ['inline_keyboard', 'remove_keyboard']:
		if x not in data: continue
		data['reply_markup'] = {x:data[x]}
		del data[x]
		return

class sendMessage(Request):
	def __init__(self, message, chat_id = "{chat_id}", **kwargs):
		keyboard_helper(kwargs)
		Request.__init__(self, "sendMessage", {"chat_id":chat_id, "text":message, **kwargs})

	# def feed(self, **kwargs):
	# 	self.data['chat_id'] = self.data['chat_id'].format(**kwargs)
	# 	#self.data = format(self.data, **kwargs)

class queuedSendMessage(sendMessage):
	def __init__(self, message, chat_id = "{chat_id}", **kwargs):
		sendMessage.__init__(self, message, chat_id, **kwargs)
		self.result = asyncio.Future()

	def set_bot(self, bot):
		bot.message_queue.add_message(self.data, self)
		return super().set_bot(bot)
		
	async def exec(self):
		return await self.result

	def receive(self, result):
		self.result.set_result(result)

	def as_response(self):
		return None

class editMessageReplyMarkup(Request):
	def __init__(self, chat_id = "{chat_id}", message_id = "{message_id}", **kwargs):
		keyboard_helper(kwargs)
		Request.__init__(self, "editMessageReplyMarkup", {"chat_id":chat_id, "message_id":message_id, **kwargs})

class editMessageText(Request):
	def __init__(self, text, chat_id = "{chat_id}", message_id = "{message_id}", **kwargs):
		keyboard_helper(kwargs)
		Request.__init__(self, "editMessageText", {"chat_id":chat_id, "message_id":message_id, "text":text, **kwargs})

	# def feed(self, **kwargs):
	# 	self.data['chat_id'] = self.data['chat_id'].format(**kwargs)
	# 	self.data['message_id'] = self.data['message_id'].format(**kwargs)

class deleteMessage(Request):
	def __init__(self, chat_id = "{chat_id}", message_id = "{message_id}"):
		Request.__init__(self, "deleteMessage", {"chat_id":chat_id, "message_id":message_id})

class answerCallbackQuery(Request):
	def __init__(self, text = None, callback_query_id = "{callback_query_id}", **kwargs):
		Request.__init__(self, "answerCallbackQuery", {"callback_query_id":callback_query_id, "text":text, **kwargs})