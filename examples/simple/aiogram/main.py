
from photon.client.bot import Bot
from photon.menu_state import MenuRegistry
from photon.menu_state import MenuEntryStackRepository

from photon.context import extract_context
from photon.state import get_state
from asyncio import run

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
bot = Bot(token)

menu_registry = MenuRegistry()
menu_entry_stack_repository = MenuEntryStackRepository(
    menu_registry=menu_registry,
)
from .scenario import main_menu

async def start_message_handler(update):
    state = get_state(update)
    state.get(main_menu).call("asd")
    #await main_menu.call().exec(bot)

async def all_message_handler(update):
    state = get_state(menu_entry_stack_repository, update)
    await state.handle().exec(bot) 

# async def main():
#     async for update__ in bot.long_polling():
#         state = get_state(menu_entry_stack_repository, update__)
#         if update__['message']['text'] == '/start':
#             await main_menu.call().exec(bot)
#             continue 
        
#         await state.handle().exec(bot) 
#         #update_.set(update__)
#         #return update__

#run(main())