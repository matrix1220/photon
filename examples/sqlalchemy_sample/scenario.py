
from config import bot

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.objects import Message
from photon import key, act, explicit_act, back

#from photon.methods import sendMessage

class TestMenu2(InlineMenu): 
	keyboard = [
		[ ("Button2", key("button2")) ],
		[ ("Back", key("back")) ],
	]
	async def act_(self):
		return Message('Test Menu 2')
	async def handle_keyboard_button2(self):
		return Message(f'Button1')
	async def handle_keyboard_back(self):
		return await self.context.back()

	async def handle_text(self, text):
		pass

class TestMenu(InlineMenu):
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
		[ ("Button1", key("button1")) ],
		[ ("Test Menu", act(TestMenu)) ],
	]

	async def act_(self, arg=None):
		self.register()
		return Message(f'Main Menu, arg={arg}')
	async def handle_keyboard_button1(self):
		return "Button1"

	async def handle_text(self, text):
		pass
