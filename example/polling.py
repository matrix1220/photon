from config import bot
from bot import handle
import asyncio

async def main():
	await bot.long_polling(handle)

# ioloop.create_task(main())
# tasks = [ioloop.create_task(main())]
# wait_tasks = asyncio.wait(tasks)

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(ioloop.create_task(main()))
ioloop.close()

#asyncio.run(main())