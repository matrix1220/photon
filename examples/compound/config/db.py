
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

engine = create_engine('sqlite:///datebase.db', connect_args={'check_same_thread': False})
sessionmaker = _sessionmaker(bind=engine)

#session = sessionmaker()

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)
