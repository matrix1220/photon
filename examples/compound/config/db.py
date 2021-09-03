
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

from . import config

engine = create_engine(*config.db.args, **config.db.kwargs)
sessionmaker = _sessionmaker(bind=engine)

#session = sessionmaker()

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)