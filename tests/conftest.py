from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from dotenv import dotenv_values

from photon.client.bot import Bot

from photon.menu import MenuEntryStackRepository, MenuRegistry

from photon.context_vars import update as update_

from photon.state import StateRepository
from photon.context import ContextExtractor

from photon.context import extract_context
from photon.state import get_state

config = dotenv_values(".env")

@fixture
def bot():
    token = config['TOKEN']
    return Bot(token)

@fixture
def menu_registry():
    return MenuRegistry()

@fixture
def menu_entry_stack_repository(menu_registry):
    return MenuEntryStackRepository(
        menu_registry=menu_registry,
    )

# @fixture
# def context_extractor():
#     return ContextExtractor()

# @fixture
# def state_repository(menu_entry_stack_repository):
#     return StateRepository(
#         menu_entry_stack_repository=menu_entry_stack_repository,
#     )

@async_fixture
async def update(bot):
    async for update__ in bot.long_polling():
        update_.set(update__)
        return update__

@fixture
def context(update):
    #return context_extractor.extract(update)
    return extract_context(update)

@fixture
def state(context, menu_entry_stack_repository):
    #return state_repository.get(context)
    return get_state(menu_entry_stack_repository, context)