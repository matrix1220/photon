from typing import Any, Dict, List

from .context_vars import state
from .context import Context
#from .state import State

from .menu import Menu

# class MenuRegistry:
#     def register(self, context: str, menu: Menu):
#         pass

class MenuState:
    def __init__(self, args = list(), kwargs = dict()):
        self.args = args
        self.kwargs = kwargs

class MenuEntry:
    def __init__(self, menu: Menu) -> None:
        self.menu = menu
        self.menu_state = MenuState()

class MenuEntryStack:
    def __init__(self, menu_registry: MenuRegistry, stack: list):
        self.menu_registry = menu_registry
        self.stack = stack
    
    def new(self, menu: Menu) -> MenuEntry:
        menu_entry = MenuEntry(menu)
        self.push(menu_entry)
        return menu_entry

    def push(self, menu_entry: MenuEntry):
        self.stack.append(menu_entry)

    def pop(self) -> MenuEntry:
        return self.stack.pop()
    
    def head(self) -> MenuEntry:
        return self.stack[-1]

    def reset(self):
        self.stack.clear()


class MenuEntryStackRepository:
    def __init__(self, menu_registry: MenuRegistry):
        self.menu_registry = menu_registry
        self.set = {}

    def get(self, context: Context) -> MenuEntryStack:
        if context.chat_id not in self.set:
            self.set[context.chat_id] = MenuEntryStack(
                menu_registry=self.menu_registry,
                stack=[]
            )

        return self.set[context.chat_id]

