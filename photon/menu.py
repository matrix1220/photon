from typing import Any, Dict, List

from .context_vars import state
from .context import Context
#from .state import State

class Representable:
    def represent(self):
        pass

class Button(Representable):
    def __init__(self, title, func):
        self.title = title
        self.func = func
    
    def handle(self):
        return self.func()
    
    def represent(self):
        return self.title

class Keyboard(Representable):
    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.key_map = {
            button.title: button
                for button_row in keyboard
                for button in button_row
        }
    
    def handle(self, key):
        return self.key_map[key].handle()
    
    def represent(self):
        return [
            [ button.represent() for button in button_row ]
            for button_row in self.keyboard
        ]
    
    # def state(self,):
    #     pass

# class SpecialMenu:
#     def _call(self, ):
#         pass

class MenuBase(Representable):
    pass

class Menu:
    def __init__(self, message, keyboard: Keyboard):
        self.message = message
        self.keyboard = keyboard
    
    def function(self, state):
        context_: Context = state.context
        return context_.transform(self.message, self.keyboard.represent())
    
    def back(self, state, *args, **kwargs):
        return self.function(state)
    
    def handle(self, state):
        context_: Context = state.context
        #context_.transform()
        return self.keyboard.handle(context_.message)
    
    # helper functions
    def call(self, *args, **kwargs):
        #state_: State = state.get()
        state_ = state.get()
        #menu_entry_stack_: MenuEntryStack = menu_entry_stack.get()
        menu_entry = state_.menu_entry_stack.new(self)
        menu_state = menu_entry.menu_state
        menu_state.args, menu_state.kwargs = args, kwargs
        result = self.function(menu_state)
        return result # state_.call(menu_entry)