

menu_classes = {}

class Menu:
	def __init_subclass__(_class, **kwargs):
		_class._menu_id = len(menu_classes)
		menu_classes[_class._menu_id] = _class
	# def handle_text(self, text):
	# 	pass
	# def handle_video(self, video):
	# 	pass
	def handle_message(self, message):
		pass

	async def act(self):
		pass

	# def __init__(self, explicit=False):
	# 	self.explicit = explicit

	def passes(self):
		if self.explicit:
			self.menu_stack.set_current([handler.id, args, kwargs])
		else:
			self.menu_stack.push([handler.id, args, kwargs])