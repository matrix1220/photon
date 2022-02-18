#from photon import Bot, ContextManager
import logging, asyncio, photon

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.methods import sendMessage
from photon.objects import Message
from photon import key, act, explicit_act, back

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('hpack').setLevel(logging.ERROR)

bot = photon.Bot("305643264:AAHoW3g1QO-XQk2-I-iQpwongbDlHBZ2t5A")
photon.ContextManager(bot)

class TestMenu(OutlineMenu):
	keyboard = [
		[ ("Back", back()) ],
	]
	async def act_(self):
		return Message('Test Menu')

class MainMenu(OutlineMenu):
	keyboard = [
		[ ("Button1", key("button1")) ],
		[ ("Test Menu", act(TestMenu)) ],
	]
	async def act_(self, arg=None):
		self.register()
		return Message(f'Main Menu, arg={arg}')

handlers = photon.OnHandlers(bot)
@handlers.on("message")
async def start(request, message):
	#await bot.sendMessage('salom', "108268232")
	return request.context.act(MainMenu)

async def main():
	await bot.long_polling()

asyncio.run(main())