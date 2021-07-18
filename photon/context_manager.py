
#from .context import Context
from .menu import InlineMenuContext, OutlineMenuContext
from .menu import Mode

#from .context_properties import ContextProperties, MenuContextProperties


#context_properties = {}
contexts = {}

# class MenuContextManager:
# 	def switch_menu_mode(self, context):
# 		if context.mode==Mode.inline:
# 			return OutlineMenuContext.switch_from(context)
# 		elif context.mode==Mode.outline:
# 			return InlineMenuContext.switch_from(context)
#class ContextManager(MenuContextManager):

class ContextManager:
	# def __init__(self, bot):
	# 	bot.context_manager = self

	# def _append_commit_list(self, item):
	# 	self.commit_list.append(item)

	# def commit(self):
	# 	for item in self.commit_list:
	# 		item.commit()

	def instantiate(self, Context, metadata):
		context = Context() # Context(metadata)
		context.metadata = metadata
		context.bot = self.bot
		context.manager = self
		#context.properties = self.find(metadata)
		return context

	async def handle_update(self, update):
		metadata = self.parse(update)
		if not metadata: return
		context = self.find(metadata)
		if not context: return
		#if not context: return
		#context.properties = self.find(metadata)
		#if not context.properties: return
		result = await context.handle_update(update)
		context.commit()
		#self.save(context)
		return result 

	# def create(self, metadata):
	# 	if "chat_id" not in metadata: return
	# 	if "message_id" in metadata:
	# 		return self.instantiate(InlineMenuContext, metadata)

	# 	return self.instantiate(OutlineMenuContext, metadata)

	def find_inline(self, metadata):
		pass
		# chat_id = metadata['chat_id']
		# message_id = metadata['message_id']

		# key = f"chat_id:{chat_id}:message_id:{message_id}"
		# if key in context_properties:
		# 	return context_properties[key]

		# context_properties_ = MenuContextProperties(metadata)

		# #context_properties[key] = context_properties_
		# return context_properties_

	def find_outline(self, metadata):
		pass
		# chat_id = metadata['chat_id']
		# key = f"chat_id:{chat_id}"
		# if key in context_properties:
		# 	return context_properties[key]

		# context_properties_ = MenuContextProperties(metadata)

		# context_properties[key] = context_properties_
		# return context_properties_


	def find(self, metadata):
		if "chat_id" not in metadata: return

		if "message_id" in metadata:
			return self.find_inline(metadata)
			
		return self.find_outline(metadata)
		

	# def save(self, context_properties_):
	# 	metadata = context_properties_.metadata
	# 	if "chat_id" in metadata:
	# 		chat_id = metadata['chat_id']
	# 		if "message_id" in metadata:
	# 			message_id = metadata['message_id']
	# 			key = f"chat_id:{chat_id}:message_id:{message_id}"
	# 			context_properties[key] = context_properties_
	# 			return

	# 		key = f"chat_id:{chat_id}"
	# 		context_properties[key] = context_properties_
	# 		return

	# def exists(self, metadata):
	# 	pass

	def parse(self, update):
		metadata = None
		if message := update.message:
			chat = message.chat
			if chat.type == "private":
				metadata = dict(chat_id = chat.id)
				#feed_data = dict(chat_id = chat.id)
			elif chat.type in ["group", "supergroup"]:
				metadata = dict(chat_id = chat.id)
				#metadata = dict(chat_id = chat.id, from_id = message['from'].id)
		elif callback_query := update.callback_query:
			if not "message" in callback_query: return
			message = callback_query.message
			metadata = dict(
				chat_id=message.chat.id,
				message_id=message.message_id,
				callback_query_id=callback_query.id,
			)
		return metadata
