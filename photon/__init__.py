

from .client import inline_button as _inline_button
from . import globals_


import json, re

async def handle(update):
	if message := update.message:
		chat = message.chat
		if chat.type == "private":
			router = globals_.find_router(user_id=chat.id)
			result = await router.handle_message(message)
			if isinstance(result, Request):
				result.feed(chat_id=chat.id)
			return result
		# elif chat.type in ["group", "supergroup"]:
		# 	router = find_router(user_id=chat.id)
		# 	#group = globals_.Group.find(chat.id)

		# 	return await user.handle_message(message)

	elif callback_query := update.callback_query:
		router = globals_.find_router(user_id=callback_query['from'].id, message_id=123)
		if not router:
			return globals_.bot.answerCallbackQuery(callback_query.id)
		return await router.handle_callback(callback_query)

#handle_as_response

from .imports import *