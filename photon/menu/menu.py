
from ..objects import Message
from ..client import Request

from ..catch import catch_request, catch_result, catch
from ..catch import Result

from .mode import Inline, Outline, Mode

menu_classes = {}

class Menu:
	def __getattribute__(self, key):
		if key.startswith("handle"):
			async def handle(*args, **kwargs):
				result = await catch(object.__getattribute__(self, key), *args, **kwargs)
				return self.complete_result(result)
			return handle
		return object.__getattribute__(self, key)

	keyboard = None
	def __init_subclass__(menu_class, **kwargs):
		menu_class.id = len(menu_classes)
		menu_classes[menu_class.id] = menu_class

	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs

	async def act(self, *args, **kwargs):
		result = await catch(self._act, *args, **kwargs)
		return self.complete_result(result)

	# async def _act(self):
	# 	pass

	# async def act_(self):
	# 	pass

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
		if keyboard == None:
			keyboard = self.keyboard


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
		if isinstance(result, str):
			result = self.context.bot.answerCallbackQuery(result)

		if isinstance(result, dict):
			result = Request.from_response(result)

		if isinstance(result, Message):
			if self.context.incomplete:
				result = self.context.bot.sendMessage(result.text, **self.set_keyboard())
			else:
				result = self.context.bot.editMessageText(result.text, **self.set_keyboard())

		if isinstance(result, Request):
			result.feed(**self.context.metadata)

		return result

	def set_keyboard(self, keyboard=None):
		if keyboard == None:
			keyboard = self.keyboard
		return {"inline_keyboard": [[inline_button(value, key) for value, key in row] for row in keyboard]}