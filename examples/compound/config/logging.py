from . import config
import logging
logging.basicConfig(**config.logging)

if config.debug:
	logging.getLogger('hpack').setLevel(logging.ERROR)