from ..context import Context
#from ..objects import Message

from ..catch import catch_request, catch_result, catch
from ..catch import Done

from .menu import InlineMenu, OutlineMenu, Menu
from .mode import Inline, Outline, Mode
#from .menu_stack import MenuStack
#from .register import Act, ExplicitAct


		# if isinstance(result, Request) or isinstance(result, Done):
		# 	raise Act(menu_class, result.arg, args, kwargs)
		# elif isinstance(result, Incorrect):
		# 	raise result.arg
# abstract class;
class MenuContext(Context):

	def switch_mode(self, metadata):
		#dict(chat_id=self.metadata['chat_id'], message_id=None)
		return self.manager.find(metadata)
		#return self.opposite.switch_from(self)

	async def forward(self, menu_class, *args, **kwargs):
		#assert isinstance(menu_class, type), "menu class required"
		#assert issubclass(menu_class, Menu), "asd"

		menu_object = self.instantiate(menu_class)
		result = await catch_request(menu_object.act, *args, **kwargs)
		result = menu_object.complete_result(result)
		return result

	async def act(self, menu_class, *args, **kwargs):
		if self.mode!=menu_class.mode:
			context = self.switch_mode()
			await context.act(menu_class, *args, **kwargs)

		result = await self.forward(menu_class, *args, **kwargs)
		self.menu_stack.push(menu_class.id, args, kwargs)
		raise Done(result)

	async def explicit_act(self, menu_class, *args, **kwargs):
		if self.mode!=menu_class.mode:
			context = self.switch_mode()
			await context.explicit_act(menu_class, *args, **kwargs)

		result = await self.forward(menu_class, *args, **kwargs)
		self.menu_stack.set_current(menu_class.id, args, kwargs)
		raise Done(result)

	async def _back(self):
		pass

	async def back(self):
		self.menu_stack.pop()
		if self.menu_stack.empty():
			return await self._back()
		menu_class, args, kwargs = self.menu_stack.current()
		return await self.explicit_act(menu_class, *args, **kwargs)

class OutlineMenuContext(Outline, MenuContext):
	async def _back(self):
		return await self.main_menu()

	def switch_mode(self):
		context = super().switch_mode(dict(chat_id=self.metadata['chat_id'], message_id=None))
		context.incomplete = True
		return context

	async def main_menu(self, arg=None):
		self.menu_stack.reset()
		return await self.explicit_act(self.bot.main_menu, arg=arg)


	async def handle_outline_menu(self, message):
		#result = None
		#print(message)
		if self.menu_stack.empty():
			return await catch_result(self.main_menu)
			#print(type(result))
			# print()
			# print("asd")
			# print()

		menu_object = self.instantiate(self.menu_stack.current_menu())

		if text:=message.text:
			if self.keyboard!=None and text in self.keyboard:
				key = self.keyboard[text]
				if hasattr(menu_object, f"handle_keyboard_{key}"):
					result = await getattr(menu_object, f"handle_keyboard_{key}")()
					if result!=False: return result

		for x in ['text', 'video']:
			if x not in message: continue
			return await getattr(menu_object, f"handle_{x}")(message[x])

		return await menu_object.handle_message(message)
	
	# async def set_outline_keyboard(self, keyboard):
	# 	# if keyboard==None: keyboard = self.menu_stack.current_menu().keyboard
	# 	# if keyboard==None: return self.remove_keyboard()
	# 	self.keyboard = parse_keys(keyboard)
	# 	# self.keyboard.clear()
	# 	# self.keyboard.update(parse_keys(keyboard))
	# 	return {"keyboard":parse_values(keyboard)}
	# async def remove_outline_keyboard(self):
	# 	self.keyboard = None
	# 	return {"remove_keyboard":True}

class InlineMenuContext(Inline, MenuContext):
	async def _back(self):
		pass
		#return await self.main_menu()
	def __init__(self):
		self.incomplete = False

	def switch_mode(self):
		context = super().switch_mode(dict(chat_id=self.metadata['chat_id']))
		return context

	def set_message_id(self, message_id):
		pass


	async def act(self, menu_class, *args, **kwargs):
		if self.mode!=menu_class.mode:
			context = self.switch_mode()
			await context.act(menu_class, *args, **kwargs)

		if self.incomplete:
			try:
				await MenuContext.act(self, menu_class, *args, **kwargs)
			except Done as d:
				result = d.arg

			# bug here
			#if not isinstance(result, sendMessage): raise Exception("error")
			self.metadata['message_id'] = (await result).message_id
			self.set_message_id(self.metadata['message_id'])
			self.incomplete = False
			#self.manager.save(self.properties)
			raise Done()

		await MenuContext.act(self, menu_class, *args, **kwargs)

	async def handle_inline_menu(self, callback_query):
		return await self.handle_inline_keyboard(callback_query.data)
		#menu_object = self.instantiate(menu_classes[data.pop(0)])
		#return await catch_request(handler.handle_callback, [callback_query, data])

	async def handle_inline_keyboard(self, data):
		#if not self.keyboard: return
		key = data
		menu_object = self.instantiate(self.menu_stack.current_menu())
		if not hasattr(menu_object, f"handle_keyboard_{key}"): return
		return await catch(getattr(menu_object, f"handle_keyboard_{key}"))


# InlineMenuContext.opposite = OutlineMenuContext
# OutlineMenuContext.opposite = InlineMenuContext