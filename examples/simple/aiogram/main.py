

from photon.menu_state import MenuEntryStackRepository

from photon.client.domain.context import extract_context
from photon.state import get_state
from asyncio import run

import os
import logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

from .scenario import main_menu

load_dotenv()

token = os.getenv("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

menu_entry_stack_repository = MenuEntryStackRepository()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    context = extract_context(message)
    state = get_state(context) # aquire state somehow
    response = state.get(main_menu).call("asd") # get response somehow
    return context.handle(response)


@dp.message_handler()
async def echo(message: types.Message):
    context = extract_context(message)
    state = get_state(context)

    response = await state.handle()
    return context.handle(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
