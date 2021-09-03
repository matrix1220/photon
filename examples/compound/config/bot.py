from . import config

from photon import Bot
from context import ContextManager
# TODO: fix
bot = Bot(config.token)
ContextManager(bot)
