
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
# 305643264:AAGwALg3QDiH2OrNzqehgoPdeXwpIqY416c dev aybir

import yaml
from photon.object_dict import objectify

languages = []
for x in ['language_en.yaml']:
	languages.append(objectify(yaml.load(open(x).read(), Loader=yaml.Loader)))


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

engine = create_engine('sqlite:///datebase.db', connect_args={'check_same_thread': False})
sessionmaker = _sessionmaker(bind=engine)
#session = sessionmaker()

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

import photon
if debug:
	_token = "305643264:AAGwALg3QDiH2OrNzqehgoPdeXwpIqY416c" # dynamic_config.debug_token
else:
	_token = dynamic_config.production_token

from context import ContextManager
bot = photon.Bot(_token, context_manager=ContextManager())
