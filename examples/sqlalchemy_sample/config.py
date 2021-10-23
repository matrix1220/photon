

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

engine = create_engine('sqlite:///datebase.db', connect_args={'check_same_thread': False})
sessionmaker = _sessionmaker(bind=engine)


from photon import Bot
from context import ContextManager
bot = Bot("TOKEN", context_manager=ContextManager())
