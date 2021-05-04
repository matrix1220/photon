import config, router, photon, scenario

from photon import handle

#handle = photon.handle

#handle_as_response

# async def handle(update):
# 	if message := update.message:
# 		chat = message.chat
# 		if chat.type == "private":
# 			router = globals_.find_router(user_id=chat.id)
# 			return await router.handle_message(message)
# 		# elif chat.type in ["group", "supergroup"]:
# 		# 	router = find_router(user_id=chat.id)
# 		# 	#group = globals_.Group.find(chat.id)

# 		# 	return await user.handle_message(message)

# 	elif callback_query := update.callback_query:
# 		router = globals_.find_router(user_id=callback_query['from'].id, message_id=123)
# 		if not router:
# 			return globals_.bot.answerCallbackQuery(callback_query.id)
# 		return await router.handle_callback(callback_query)


