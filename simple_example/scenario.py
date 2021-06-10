
import logging
logging.basicConfig(level=logging.DEBUG)

import photon
bot = photon.Bot("305643264:AAGwALg3QDiH2OrNzqehgoPdeXwpIqY416c")

async def main():
	await bot.long_polling(handle)

asyncio.run(main())

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.methods import sendMessage

import asyncio


@bot.set_main_menu
class MainMenu(OutlineMenu):
	keyboard = [
		# Button([Format,"str"], [key, menu, trigger])
		[ ("Button1", "button1") ],
		[ ("Test Menu", "testmenu") ],
	]
	parse_pattern = [
		("/start {arg}", "start"),
		("/id{id}", "start")
	]
	async def act(self, arg=None):
		#if user.language==None: return manager.act(SelectLanguage)()
		keyboard = await self.set_keyboard()
		return bot.sendMessage(f'Main Menu, arg={arg}', **keyboard)
		# return Message('test bot', keyboard=keyboard)
	async def handle_keyboard_button1(self):
		return bot.sendMessage(f'Button1')
	async def handle_keyboard_testmenu(self):

		#return TestMenu.act("data")
		#return TestMenu(self.context).act("data")
		return self.context.act(TestMenu, "data")
		#return TestMenu.explicit_act(asdasd)
		return await self.context.act(TestMenu)
	async def handle_text(self, text):
		# return bot.sendMessage(self.user.id, 'asdasd')
		# bot.queuedSendMessage(self.user.id, str(x) + 'a')
		# await sendMessage(self.user.id, 'end')
		# if text == "/testmenu":
		# 	return await self.context.act(TestMenu)
		pass

class TestMenu(InlineMenu): # OutlineMenu InlineMenu
	keyboard = [
		[ ("Button2", "button2") ],
		[ ("Back", "back") ],
	]
	async def act(self):
		keyboard = await self.set_keyboard()
		return bot.sendMessage('Test Menu', **keyboard)
	async def handle_keyboard_button2(self):
		return bot.sendMessage(f'Button1')
	async def handle_keyboard_back(self):
		return await self.context.back()

	async def handle_text(self, text):
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