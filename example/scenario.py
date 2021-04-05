from config import bot, languages
from photon.utils import format
from photon.client import inline_button
from photon import MenuHandler, CallbackHandler
from photon.methods import sendMessage

from dbscheme import session

import asyncio
class MainMenu(MenuHandler):
	async def act(user, arg=None):
		#if user.language==None: return user.act(SelectLanguage)()
		user.passes() # MainMenu.ids
		keyboard = [['/limit']]
		return bot.sendMessage(user.id, 'test bot', keyboard=keyboard)

	async def handle_text(user, text):
		if text == "/help":
			return bot.sendMessage(user.id, 'asdasd')
		elif text == "/about":
			user.blocked = not user.blocked
			await sendMessage(user.id, 'start' + str(user.blocked) )
		elif text == "/limit":
			await sendMessage(user.id, 'start')
			for x in range(5):
				bot.queuedSendMessage(user.id, str(x) + 'a')
			await sendMessage(user.id, 'end')
			await asyncio.sleep(3)
			bot.queuedSendMessage(user.id, str(x) + 'a')
			return bot.queuedSendMessage(user.id, 'end')
		elif text == "/bulksend":
			return await user.act(BulkSend)()





class SelectLanguage(MenuHandler):
	async def act(user):
		user.passes()
		text = ''
		keyboard = []
		for language in languages:
			text += language.select_language + "\n"
			keyboard.append([language.language])
		return bot.sendMessage(user.id, text, keyboard=keyboard)
	async def handle_text(user, text):
		for x, language in enumerate(languages):
			if text == language.language:
				user.language = x
				user.lang = languages[user.language]
				return user.back()


from dbscheme import User
class BulkSend(MenuHandler):
	bulk_send_jobs = {} 
	async def act(user, arg=None):
		user.passes()
		keyboard = [['/back']]
		return bot.sendMessage(user.id, 'send message:', keyboard=keyboard)

	async def handle_text(user, text):
		if text == "/back":
			return await user.back()

		#session.query(User)
		id = len(BulkSend.bulk_send_jobs)
		keyboard = [[inline_button("pause", [BulkSend.id, id, 1]), inline_button("stop", [BulkSend.id, id, 3])]]
		message = await sendMessage(user.id, f'wait for it', inline_keyboard=keyboard)
		BulkSend.bulk_send_jobs[id] = BulkSendJob(message, text)
		
		return await user.back()

	async def handle_callback(user, query, data):
		id, action = data
		if id not in BulkSend.bulk_send_jobs: return
		bulk_send_job = BulkSend.bulk_send_jobs[id]
		if action == 1:
			bulk_send_job.pause()
			keyboard = [[inline_button("unpause", [BulkSend.id, id, 2]), inline_button("stop", [BulkSend.id, id, 3])]]
			bulk_send_job.base_message = await bot.editMessageReplyMarkup(user.id, query.message.message_id, inline_keyboard=keyboard)
		elif action == 2:
			bulk_send_job.unpause()
			keyboard = [[inline_button("pause", [BulkSend.id, id, 1]), inline_button("stop", [BulkSend.id, id, 3])]]
			bulk_send_job.base_message = await bot.editMessageReplyMarkup(user.id, query.message.message_id, inline_keyboard=keyboard)
		elif action == 3:
			bulk_send_job.stop()
			bulk_send_job.base_message = await bot.editMessageReplyMarkup(user.id, query.message.message_id)


class BulkSendJob:
	link = {}
	def __init__(self, base_message, data):
		self.base_message = base_message
		self.data = data

		#self.sent_users = []
		self.paused_from = None
		self.sent_users_count = 0
		self.users_count = session.query(User).count()
		self.users = iter([x.id for x in session.query(User)])
		self.done = False
		# self.id = len(link)
		# link[self.id] = self

		asyncio.create_task(self.progres_job())
		self.send_task = asyncio.create_task(self.send_job())

	async def edit_message(self, text):
		if text==self.base_message.text: return
		self.base_message = await bot.editMessageText(self.base_message.chat.id, self.base_message.message_id, text, inline_keyboard=self.base_message.reply_markup.inline_keyboard)

	async def progres_job(self):
		while not self.done:
			await asyncio.sleep(3)
			if self.paused_from!=None:
				self.paused_from += 1
				text = f"paused {self.paused_from}"
				await self.edit_message(text)
				if self.paused_from>5:
					await self.edit_message("time out")
					del self
					return
			else:
				text = f"progress: {self.sent_users_count}/{self.users_count}"
				await self.edit_message(text)

		await self.edit_message("done")

	async def send_job(self):
		while True:#self.paused_from==None and not self.done:
			await asyncio.sleep(2)
			# target = self.users.pop()
			try:
				target = next(self.users)
			except StopIteration:
				self.done = True
				break

			try:
				await sendMessage(target, self.data)
			except Exception as e:
				continue

			self.sent_users_count += 1
			#self.sent_users.append(target)


	def pause(self):
		self.paused_from = 0
		self.send_task.cancel()

	def unpause(self):
		self.paused_from = None
		self.send_task = asyncio.create_task(self.send_job())

	def stop(self):
		self.done = True
		self.send_task.cancel()
