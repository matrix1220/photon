
from .request import Request, request
#from .message_queue import QueuedMessage, MessageQueue
from .bot import Bot

import json

def inline_button(text, callback_data = None, **kwargs):
	kwargs.update({"text":text})
	if callback_data!=None: kwargs.update({"callback_data":json.dumps(callback_data)})
	return kwargs

# class Exception(Exception):
# 	def __init__(self, description, error_code = None):
# 		super().__init__(description)
# 		self.description = description
# 		self.error_code = error_code

