
# try:
# 	from config import bot
# except ImportError:
# 	bot = None

# try:
# 	from router import find_router
# except ImportError:
# 	find_router = None

# try:
# 	from senario import MainMenu as main_menu
# except ImportError:
# 	main_menu = None

bot = None
find_router = None
main_menu = None

# def set(bot_, find_router_, main_menu_):
# 	nonlocal bot, find_router, main_menu
# 	bot, find_router, main_menu = bot_, find_router_, main_menu_

def set_bot(bot_):
	global bot
	bot = bot_
	return bot_

def set_find_router(find_router_):
	global find_router
	find_router = find_router_
	return find_router_

def set_main_menu(main_menu_):
	global main_menu
	main_menu = main_menu_
	return main_menu_