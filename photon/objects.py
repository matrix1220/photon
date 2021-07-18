

class Object(Exception):
	pass

class Message(Object):
	def __init__(self, text, **kwargs):
		self.text = text
		self.kwargs = kwargs

class AmendMessage(Message):
	pass
