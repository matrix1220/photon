
import logging
logging.basicConfig(level=logging.DEBUG)

import photon
bot = photon.Bot("305643264:AAGwALg3QDiH2OrNzqehgoPdeXwpIqY416c")

async def main():
	await bot.long_polling()

asyncio.run(main())

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.methods import sendMessage

import asyncio

@bot.set_main_menu
class MainMenu(OutlineMenu):
	keyboard = [
		[ ("Button1", "button1") ],
		[ ("Test Menu", "testmenu") ],
	]
	parse_pattern = [
		("/start {arg}", "start"),
		("/id{id}", "start")
	]
	async def _act(self, arg=None):
		return bot.sendMessage(f'Main Menu, arg={arg}', **keyboard)
		# return Message('test bot', keyboard=keyboard)

	async def handle_text(self, text):
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