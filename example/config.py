
import os.path
debug = os.path.exists("debug")

import logging
if debug:
	logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)

from dynamic_config import DynamicConfig
dynamic_config = DynamicConfig()

import photon
if debug:
	bot = photon.Bot(dynamic_config.debug_token)
else:
	bot = photon.Bot(dynamic_config.production_token)

import yaml
from photon.object_dict import objectify

languages = []
for x in ['language_en.yaml']:
	languages.append(objectify(yaml.load(open(x).read(), Loader=yaml.Loader)))


