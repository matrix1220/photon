
from config import sessionmaker

from dbscheme import User, Message

from photon import ContextManager as ContextManager_
from photon import Context as Context_
#from photon import OutlineMenuContext as OutlineMenuContext_
from photon import OutlineMenuContext
from photon import InlineMenuContext as InlineMenuContext_
from photon.catch import Done
from photon.menu.menu_context import MenuContext


# class OutlineMenuContext(OutlineMenuContext_):
# 	pass

class InlineMenuContext(InlineMenuContext_):
	def set_message_id(self, message_id):
		self.message.message_id = self.metadata['message_id']
		self.db.add(self.message)
		self.db.commit()

#db.commit()
class ContextManager(ContextManager_):
	def find(self, metadata):
		if "chat_id" not in metadata: return
		db = sessionmaker()
		chat_id = metadata['chat_id']

		if "message_id" in metadata:
			message_id = metadata['message_id']
			message = db.query(Message).filter_by(
				chat_id=chat_id,
				message_id=message_id
			).first()
			if not message:
				message = Message(
					chat_id=chat_id,
					message_id=message_id,
					menu_stack = []
				)
				db.add(message)
				#db.commit()
				
			context = self.instantiate(InlineMenuContext, metadata)
			context.db = db
			context.message = message
			context.menu_stack = message.menu_stack
			context.keyboard = message.keyboard
			print(message.menu_stack)

			return context


		user = db.query(User).filter_by(id=chat_id).first()
		if not user:
			user = User(id=chat_id)
			db.add(user)
			db.commit()

		context = self.instantiate(OutlineMenuContext, metadata)
		context.db = db
		context.user = user
		context.menu_stack = user.menu_stack
		context.keyboard = user.keyboard

		return context

	def save(self, context):
		context.db.commit()
		# metadata = context_properties.metadata
		# if "chat_id" not in metadata: return
		# chat_id = metadata['chat_id']
		# if "message_id" in metadata:
		# 	message_id = metadata['message_id']
		# 	context_properties.db.merge(context_properties.message)
		# 	context_properties.db.commit()
		# 	return

		# context_properties.db.merge(context_properties.user)
		# context_properties.db.commit()
		# return
