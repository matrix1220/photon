
from .context_vars import state #, update, context, 
from .client.domain.context import Context, _extract_context
from .menu_state import MenuEntry, MenuEntryStack, MenuEntryStackRepository

class State:
    def __init__(self, menu_entry_stack: MenuEntryStack):
        self.menu_entry_stack = menu_entry_stack
    
    # def menu_entry(self):
    #     return self.menu_entry_stack.head()
        
    def call(self, menu_entry: MenuEntry):
        result = menu_entry.menu.function(menu_entry.menu_state)
        #self.menu_entry_stack.push(menu_entry)
        return result

    def back(self, *args, **kwargs):
        self.menu_entry_stack.pop()
        menu_entry = self.menu_entry_stack.head()
        result = menu_entry.menu.back(menu_entry.menu_state, *args, **kwargs)
        return result

    
    def handle(self):
        menu_entry = self.menu_entry_stack.head()
        return menu_entry.menu.handle(menu_entry.menu_state)


class StateRepository:
    def __init__(self, menu_entry_stack_repository: MenuEntryStackRepository):
        self.menu_entry_stack_repository = menu_entry_stack_repository

    def get(self, context: Context) -> State:
        return get_state(self.menu_entry_stack_repository, context)


def state_back(*args, **kwargs):
    state_: State = state.get()
    return state_.back(*args, **kwargs)

# def get_state(
#         menu_entry_stack_repository: MenuEntryStackRepository,
#         context: Context
#     ) -> State:
#         menu_entry_stack = menu_entry_stack_repository.get(context)
#         state_ = State(menu_entry_stack)
#         state.set(state_)
#         return state_


def get_state(
        menu_entry_stack_repository: MenuEntryStackRepository,
        _update
    ) -> State:
        #update.set(_update)
        context = _extract_context(_update)
        menu_entry_stack = menu_entry_stack_repository.get(context)
        state_ = State(menu_entry_stack)
        state.set(state_)
        return state_