from config import bot
from dbscheme import User, session
import photon, scenario

async def handle(update):
	try:
		_response = await main(update) # photon.handle
	finally:
		session.commit()
	return _response

async def main(update):
	if message := update.message:
		chat = message.chat
		if chat.type == "private":
			user = User.find(chat.id)
			#user.update = update

			return await user.handle_message(message)
		elif chat.type in ["group", "supergroup"]:
			user = User.find(message['from'].id)
			#group = _globals.Group.find(chat.id)

			return await user.handle_message(message)

	elif callback_query := update.callback_query:
		user = User.find(callback_query['from'].id)
		if not user:
			return _globals.bot.answerCallbackQuery(callback_query.id)
		return await user.handle_callback(callback_query)


