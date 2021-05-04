
	

inline_menu_classes = {}

class InlineMenu:
	def __init_subclass__(_class, **kwargs):
		_class._inline_menu_id = len(inline_menu_classes)
		inline_menu_classes[_class._inline_menu_id] = _class