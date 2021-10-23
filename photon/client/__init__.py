
from .request import Request, request
#from .message_queue import QueuedMessage, MessageQueue
from .bot import Bot

import json
import base64
import pickle

def serialize_callback_data(data):
	return base64.b64encode(pickle.dumps(data)).decode()

def unserialize_callback_data(data):
	return pickle.loads(base64.b64decode(data.encode()))

def inline_button(text, callback_data = None, **kwargs):
	kwargs.update({"text":text})
	if callback_data!=None: kwargs.update({"callback_data": serialize_callback_data(callback_data)})
	return kwargs

# class Exception(Exception):
# 	def __init__(self, description, error_code = None):
# 		super().__init__(description)
# 		self.description = description
# 		self.error_code = error_code

