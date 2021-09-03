import yaml
from photon.object_dict import objectify

config = objectify(yaml.load(open('config.yaml').read(), Loader=yaml.Loader))

import logging
if config.debug:
	logging.basicConfig(level=logging.DEBUG)
	logging.getLogger('hpack').setLevel(logging.ERROR)
else:
	logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

engine = create_engine(*config.db.args, **config.db.kwargs)
sessionmaker = _sessionmaker(bind=engine)

#session = sessionmaker()

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

from photon import Bot
from context import ContextManager
bot = Bot(config.token)
ContextManager(bot)
