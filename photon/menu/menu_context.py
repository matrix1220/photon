from ..context import Context
#from ..objects import Message

from ..catch import catch_request, catch_result, catch
from ..catch import Done

from .menu import InlineMenu, OutlineMenu, Menu
from .menu import menu_classes
from .mode import Inline, Outline, Mode

#from .menu_stack import MenuStack

# abstract class;
class MenuContext(Context):
	def switch_mode(self, metadata):
		#dict(chat_id=self.metadata['chat_id'], message_id=None)
		context = self.manager.find(metadata)
		self._append_commit_list(context)
		return context
		#return self.opposite.switch_from(self)

	def _check_mode(self, menu_class):
		if self.mode!=menu_class.mode:
			return self.switch_mode()

		return self

	async def act(self, menu_class, *args, **kwargs):
		context = self._check_mode(menu_class)
		menu_object = menu_class(context)
		return await menu_object.act(*args, *kwargs)

	async def explicit_act(self, menu_class, *args, **kwargs):
		context = self._check_mode(menu_class)
		menu_object = menu_class(context)
		return await menu_object.explicit_act(*args, *kwargs)

	async def reset(self, menu_class, *args, **kwargs):
		context = self._check_mode(menu_class)
		menu_object = menu_class(context)
		return await menu_object.reset(*args, *kwargs)

	async def _back(self):
		pass

	async def back(self):
		self.menu_stack.pop()
		if self.menu_stack.empty():
			return await self._back()
		menu_class, args, kwargs = self.menu_stack.current()
		return await self.explicit_act(menu_class, *args, **kwargs)

	

class OutlineMenuContext(Outline, MenuContext):
	async def main_menu(self, arg=None):
		return await self.reset(self.bot.main_menu, arg=arg)

	async def _back(self):
		return await self.main_menu()

	def switch_mode(self):
		metadata = dict(chat_id=self.metadata['chat_id'], message_id=None)
		context = super().switch_mode(metadata)
		context.incomplete = True
		return context

	async def handle_outline_menu(self, message):
		if self.menu_stack.empty():
			return await self.main_menu()

		menu_object = self.instantiate(*self.menu_stack.current())
		#menu_object = None

		if text:=message.text:
			if self.keyboard!=None and text in self.keyboard:
				key = self.keyboard[text]
				result = await menu_object.handle('keyboard', key)
				#return result
				if result!=False: return result

		for x in ['text', 'video']:
			if x not in message: continue
			result = await menu_object.handle(x, message[x])
			if result!=False: return result
			#break

		return await menu_object.handle_message(message)

class InlineMenuContext(Inline, MenuContext):
	async def _back(self):
		pass
		#return await self.main_menu()
	def __init__(self):
		super().__init__()
		self.incomplete = False

	def switch_mode(self):
		metadata = dict(chat_id=self.metadata['chat_id'])
		context = super().switch_mode(metadata)
		return context

	def set_message_id(self, message_id):
		pass

	def get_message_id(self, message_id):
		self.metadata['message_id'] = message_id
		self.set_message_id(message_id)
		self.incomplete = False

	async def handle_inline_menu(self, callback_query):
		return await self.handle_inline_keyboard(callback_query.data)

	async def handle_inline_keyboard(self, data):
		if self.menu_stack.empty():
			print("bla")
			return
		menu_object = self.instantiate(*self.menu_stack.current())
		return await menu_object.handle_keyboard(data)


# InlineMenuContext.opposite = OutlineMenuContext
# OutlineMenuContext.opposite = InlineMenuContext