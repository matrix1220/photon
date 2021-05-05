
from config import bot, languages

from photon import Menu, InlineMenu, set_main_menu
from photon.client import inline_button
from photon.methods import sendMessage
from photon.utils import format

import asyncio

# class OrderMessage(Message):
# 	keyboard = [
# 		[{"Button1":"asd"}]
# 	]
# 	inline_keyboard = [[]]

@set_main_menu
class MainMenu(Menu):
	keyboard = [
		[{"Button1":"asd"}],
		[{"Button2":"asd"}],
	]
	async def act(self, arg=None):
		#if user.language==None: return router.act(SelectLanguage)()
		keyboard = [['/limit'], ['/testmenu']]
		return bot.sendMessage('test bot', keyboard=keyboard)
		# return Message('test bot', keyboard=keyboard)
	async def handle_keyboard_asd(self):
		pass
	async def handle_text(self, text):
		if text == "/help":
			return bot.sendMessage(self.user.id, 'asdasd')
		elif text == "/about":
			#self.user.blocked = not self.user.blocked
			await sendMessage(self.user.id, 'start' + str(self.user.blocked) )
		elif text == "/limit":
			await sendMessage(self.user.id, 'start')
			for x in range(5):
				bot.queuedSendMessage(self.user.id, str(x) + 'a')
			await sendMessage(self.user.id, 'end')
			await asyncio.sleep(3)
			bot.queuedSendMessage(self.user.id, str(x) + 'a')
			return bot.queuedSendMessage(self.user.id, 'end')
		elif text == "/bulksend":
			pass
			#return await self.router.act(BulkSend)()
		elif text == "/testmenu":
			return await self.router.act(TestMenu)

class TestMenu(Menu):
	async def act(self):
		#if user.language==None: return router.act(SelectLanguage)()
		keyboard = [['back']]
		return bot.sendMessage('test menu', keyboard=keyboard)
	async def handle_keyboard_asd(self):
		pass
	async def handle_text(self, text):
		if text == "back":
			return await self.router.back()



class SelectLanguage(Menu):
	async def act(self):
		text = ''
		keyboard = []
		for language in languages:
			text += language.select_language + "\n"
			keyboard.append([language.language])
		return bot.sendMessage(self.user.id, text, keyboard=keyboard)
	async def handle_text(self, text):
		for x, language in enumerate(languages):
			if text == language.language:
				self.user.language = x
				self.user.lang = languages[self.user.language]
				return self.router.back()