

from dbscheme import User
class NewBulkJob(OutlineMenu):
	bulk_send_jobs = {} 
	keyboard = [[("Orqaga", back())]]
	message = 'send message:'
	# async def act(self):
	# 	return Message('send message:')

	async def handle_text(self, text):
		await self.exec(await self.context.act(BulkMenu, text))
		return await self.context.back()


class BulkMenu(InlineMenu):
	keyboard = [[("Orqaga", back())]]
	text = ""
	async def act(self, text):
		return Message('wait for it')

	async def handle_keyboard_pause(self):
		pass

	async def handle_keyboard_resume(self):
		pass

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
