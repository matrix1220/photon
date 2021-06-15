
from config import bot, languages

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.objects import Message
from photon import key, act, explicit_act

#from photon.methods import sendMessage

import asyncio

# class OrderMessage(Message):
# 	keyboard = [
# 		[{"Button1":"asd"}]
# 	]

# class CoolKeyboard(Keyboard):
# 	def __init__(self):
# 		super().__init__(
# 			[Button(self.context.language.help), Button(self.context.language.about)]
# 		)

class TestMenu2(InlineMenu): # OutlineMenu InlineMenu
	keyboard = [
		[ ("Button2", key("button2")) ],
		[ ("Back", key("back")) ],
	]
	async def act_(self):
		#keyboard = self.set_keyboard()
		return Message('Test Menu 2')
	async def handle_keyboard_button2(self):
		return Message(f'Button1')
	async def handle_keyboard_back(self):
		return await self.context.back()

	async def handle_text(self, text):
		pass

class TestMenu(InlineMenu): # OutlineMenu InlineMenu
	keyboard = [
		[ ("Button2", act(TestMenu2)) ],
		[ ("Back", key("back")) ],
	]
	async def act_(self):
		return Message('Test Menu')
	async def handle_keyboard_back(self):
		return await self.context.back()	

@bot.set_main_menu
class MainMenu(OutlineMenu):
	keyboard = [
		# Button([Format,"str"], [key, menu, trigger])
		[ ("Button1", key("button1")) ],
		[ ("Test Menu", act(TestMenu)) ],
	]
	parse_pattern = [
		("/start {arg}", "start"),
		("/id{id}", "start")
	]
	async def act_(self, arg=None):
		#if user.language==None: return manager.act(SelectLanguage)()
		return Message(f'Main Menu, arg={arg}')
		# return Message('test bot', keyboard=keyboard)
	async def handle_keyboard_button1(self):
		return "Button1"

	async def handle_text(self, text):
		# return bot.sendMessage(self.user.id, 'asdasd')
		# bot.queuedSendMessage(self.user.id, str(x) + 'a')
		# await sendMessage(self.user.id, 'end')
		# if text == "/testmenu":
		# 	return await self.context.act(TestMenu)
		pass







# class SelectLanguage(OutlineMenu):
# 	async def act(self):
# 		text = ''
# 		keyboard = []
# 		for language in languages:
# 			text += language.select_language + "\n"
# 			keyboard.append([language.language])
# 		return bot.sendMessage(self.user.id, text, keyboard=keyboard)
# 	async def handle_text(self, text):
# 		for x, language in enumerate(languages):
# 			if text == language.language:
# 				self.user.language = x
# 				self.user.lang = languages[self.user.language]
# 				return self.context.back()