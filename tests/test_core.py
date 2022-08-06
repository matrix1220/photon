
from photon.menu import Menu, Keyboard, Button
from photon.menu import MenuRegistry
from photon.menu import MenuEntryStackRepository
from photon.state import state_back

import pytest

#on_handlers = OnHandlers()
#on_handlers.on("message", test)
# def hndl(update):
#     on_handlers.handle(update)


# def main(update, context_extractor, state_repository: StateRepository):
#     context = context_extractor.extract(update)
#     state = state_repository.get(context)
#     state.handle(update)


main_menu = Menu(
    "Main Menu",
    Keyboard([
        [ Button("calculate 1 + 2", lambda: f"result: {1 + 2}") ],
        [ Button("go to second menu", lambda: second_menu.call()) ]
    ])
)

second_menu = Menu(
    "Second Menu",
    Keyboard([
        [ Button("Back", state_back) ]
    ])
)

# @pytest.mark.asyncio
# async def test_core(update):
#     print(update)

# @pytest.mark.asyncio
# async def test_context_extractor(update, context_extractor):
#     context = context_extractor.extract(update)
#     print(context)

# @pytest.mark.asyncio
# async def test_state_repository(context, state_repository):
#     state = state_repository.get(context)
#     print(state)

# @pytest.mark.asyncio
# async def test_menu(state):
#     print(main_menu.call())

# @pytest.mark.asyncio
# async def test_menu(state, bot):
#     await main_menu.call().exec(bot)

@pytest.mark.asyncio
async def test_menu_2(state, bot):
    await main_menu.call().exec(bot)
    await state.handle().exec(bot)