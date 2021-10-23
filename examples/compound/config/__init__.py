

import yaml
from photon.object_dict import objectify

config = objectify(yaml.load(open('config.yaml').read(), Loader=yaml.Loader))

from .logging import _
from .bot import bot
from .db import engine, sessionmaker