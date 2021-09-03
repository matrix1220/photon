from .debug import debug
from .dynamic_config import dynamic_config

if debug:
	_token = dynamic_config.debug_token
else:
	_token = dynamic_config.production_token

from photon import Bot
from context import ContextManager
# TODO: fix
bot = Bot(_token, context_manager=ContextManager())
