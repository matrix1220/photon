
from ..objects import Message
from ..client import Request

from ..catch import catch_request, catch_result, catch
from ..catch import Result

from .mode import Inline, Outline, Mode

menu_classes = {}

class Menu:
	def __init__(self, context):
		self.context = context
		self.bot = context.bot
		# self._explicit = None
		# self.reset = None

	def _init(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs

	keyboard = None
	def keyboard_(self):
		return self.keyboard

	text = None
	def text_(self):
		return self.text
		
	def __getattribute__(self, key):
		if key.startswith("handle"):
			async def handle(*args, **kwargs):
				result = await catch(object.__getattribute__(self, key), *args, **kwargs)
				return self.complete_result(result)
			return handle
		return object.__getattribute__(self, key)

	
	def __init_subclass__(menu_class, **kwargs):
		menu_class.id = len(menu_classes)
		menu_classes[menu_class.id] = menu_class

	def register(self):
		if self._explicit:
			self.context.menu_stack.set_current(self.id, self.args, self.kwargs)
		else:
			self.context.menu_stack.push(self.id, self.args, self.kwargs)

	def instantiate(self, class_):
		if self.mode!=class_.mode:
			context = self.context.switch_mode()
		else:
			context = self.context

		return class_(context)

	async def act(self, *args, **kwargs):
		self._explicit = False
		self._init(*args, **kwargs)
		result = await catch(self._act, *args, **kwargs)
		return self.complete_result(result)

	async def explicit_act(self, *args, **kwargs):
		self._explicit = True
		self._init(*args, **kwargs)
		result = await catch(self._act, *args, **kwargs)
		return self.complete_result(result)

	async def reset(self, *args, **kwargs):
		self.context.menu_stack.reset()
		return await self.explicit_act(*args, **kwargs)

	async def _act(self, *args, **kwargs):
		pass

	async def handle_key(self, key, *args, **kwargs):
		if not hasattr(self, f"handle_key_{key}"): return
		return await getattr(self, f"handle_key_{key}")(*args, **kwargs)

	async def handle(self, key, *args, **kwargs):
		if not hasattr(self, f"handle_{key}"): return
		return await getattr(self, f"handle_{key}")(*args, **kwargs)

	async def exec(self, result):
		result = self.complete_result(result)
		if result:
			return await result
		# if hasattr(result, "__await__"):
		# 	return await result

	# def keyboard(self, keyboard = None):
	# 	if keyboard == None:
	# 		return self.keyboard
	# 	return keyboard

	def complete_result(self, result):
		if isinstance(result, Result):
			result.arg = self.complete_request(result.arg)
		else:
			result = self.complete_request(result)

		return result

	async def handle_keyboard(self, keyboard):
		key_, *rest = keyboard
		if key_==0:
			target, args, kwargs = rest
			return await self.handle_key(target, *args, **kwargs)
		elif key_==1:
			target, args, kwargs = rest
			return await self.context.act(menu_classes[target], *args, **kwargs)
		elif key_==2:
			target, args, kwargs = rest
			return await self.context.explicit_act(menu_classes[target], *args, **kwargs)
		elif key_==3:
			return await self.back()


	async def _back(self):
		pass

	async def back(self):
		self.context.menu_stack.pop()
		if self.context.menu_stack.empty():
			return await self._back()
		menu_class, args, kwargs = self.context.menu_stack.current()
		return await self.context.explicit_act(menu_class, *args, **kwargs)


#outline_menu_classes = {}
class OutlineMenu(Outline, Menu):
	
	def complete_request(self, result):
		if isinstance(result, str):
			result = Message(result)

		if isinstance(result, dict):
			result = Request.from_response(result)

		if isinstance(result, Message):
			result = self.bot.sendMessage(result.text, **self.set_keyboard())

		if isinstance(result, Request):
			result.feed(**self.context.metadata)

		return result


	async def handle_text(self, text):
		pass
	async def handle_message(self, message):
		pass

	def set_keyboard(self, keyboard=None):
		if keyboard == None: keyboard = self.keyboard
		if not keyboard: return {}
		
		self.context.keyboard.clear()
		#keyboard_ = {}

		for row in keyboard:
			for button in row:
				#print(button)
				value, key = button
				self.context.keyboard[value] = key

		#self.context.properties.keyboard = keyboard_
		return {"keyboard": [[value for value, key in row] for row in keyboard]}

#inline_menu_classes = {}
from photon.client import inline_button

class InlineMenu(Inline, Menu):
	def complete_request(self, result):
		if result==True:
			# bug, check for keyboard, text
			result = self.bot.editMessageReplyMarkup(**self.set_keyboard())

		if isinstance(result, str):
			result = self.bot.answerCallbackQuery(result)

		if isinstance(result, dict):
			result = Request.from_response(result)

		if isinstance(result, Message):
			if self.context.incomplete:
				result = self.bot.sendMessage(result.text, **self.set_keyboard())
			else:
				result = self.bot.editMessageText(result.text, **self.set_keyboard())

		if isinstance(result, Request):
			result.feed(**self.context.metadata)

		return result

	# def _parse_keynoard(self):
	# 	pass

	def set_keyboard(self, keyboard=None):
		if keyboard == None: keyboard = self.keyboard
		if keyboard == None: return {}

		return {
			"inline_keyboard": [
				[inline_button(value, key) for value, key in row]
					for row in keyboard
			]
		}

	async def act(self, *args, **kwargs):
		result = await Menu.act(self, *args, **kwargs)
		if self.context.incomplete:
			if not result:return result
			result = await result
			if "message_id" in result:
				self.context.get_message_id(result.message_id)
			return
		return result

	async def explicit_act(self, *args, **kwargs):
		result = await Menu.explicit_act(self, *args, **kwargs)
		if self.context.incomplete:
			if not result:return result
			result = await result
			if "message_id" in result:
				self.context.get_message_id(result.message_id)
			return
		return result