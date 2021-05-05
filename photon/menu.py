

menu_classes = {}

class Menu:
	def __init_subclass__(_class, **kwargs):
		_class._menu_id = len(menu_classes)
		menu_classes[_class._menu_id] = _class
	# def handle_text(self, text):
	# 	pass
	# def handle_video(self, video):
	# 	pass
	async def handle_message(self, message):
		pass

	async def act(self):
		pass