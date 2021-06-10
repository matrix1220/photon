import asyncio, time

class QueuedMessage:
	def __init__(self, message, sender=None):
		self.message = message
		self.sender = sender
		self.next = None

# class PriorityMessageQueue:
# 	def __init__(self):
# 		self.first_message = None
# 		self.message_priorities_last = defaultdict()
# 	def add_message(self, message, priority, sender=None):
# 		queued_message = QueuedMessage(message, sender)
		
# 		if last_priority_message := self.message_priorities_last[priority]:
# 			#if last_priority_message.next != None:
# 			queued_message.next = last_priority_message.next

# 			self.message_priorities_last[priority].next = queued_message
		
# 		self.message_priorities_last[priority] = queued_message

# 		if self.first_message==None:
# 			self.first_message = queued_message

# 	def __await__(self):
# 		while True:
# 			if self.first_message==None:
# 				yield
# 				continue
# 			queued_message = self.first_message
# 			result = yield from bot._send("sendMessage", queued_message.message)
# 			if queued_message.sender!=None:
# 				queued_message.sender.receive(result)
# 			self.first_message = queued_message.next

class MessageQueue:
	def __init__(self, bot):
		self.bot = bot
		#self.contains = asyncio.Future()
		self.task = None
		self.first_message = None
		self.last_message = None

	def add_message(self, message, sender=None):
		queued_message = QueuedMessage(message, sender)
		if self.last_message!=None:
			self.last_message.next = queued_message

		self.last_message = queued_message

		if self.first_message==None:
			self.first_message = queued_message

		# if not self.contains.done():
		# 	self.contains.set_result(None)

		if self.task==None:
			print("task crated")
			self.task = asyncio.create_task(self.exec())

	async def exec(self):
		counter = 0
		current_time = int(time.time())
		# while True:
		# 	await self.contains
		while self.first_message!=None:
			queued_message = self.first_message
			result = await self.bot._send("sendMessage", queued_message.message)

			if queued_message.sender!=None:
				queued_message.sender.receive(result)

			self.first_message = queued_message.next

			counter += 1

			if counter > 25:
				await asyncio.sleep(1)

			if int(time.time()) >= current_time + 1:
				counter = 0
				current_time = int(time.time())

		self.task = None

		#self.contains = asyncio.Future()

	def __await__(self):
		return self.exec().__await__()