
import os.path
debug = os.path.exists("debug")

import logging
if debug:
	logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)

from dynamic_config import DynamicConfig
dynamic_config = DynamicConfig()

# 287925905:AAEsaBOKVGoKDiGxBr1aaBxkpYn4AHUpbJQ dev botmoq
#  dev aybir
import photon
if debug:
	bot = photon.Bot("305643264:AAGwALg3QDiH2OrNzqehgoPdeXwpIqY416c") # dynamic_config.debug_token
else:
	bot = photon.Bot(dynamic_config.production_token)

photon.set_bot(bot)

import yaml
from photon.object_dict import objectify

languages = []
for x in ['language_en.yaml']:
	languages.append(objectify(yaml.load(open(x).read(), Loader=yaml.Loader)))


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

engine = create_engine('sqlite:///datebase.db')
sessionmaker = _sessionmaker(bind=engine)
#session = sessionmaker()


