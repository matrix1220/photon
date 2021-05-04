
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Integer, String, Boolean, Text, DateTime
from sqlalchemy import Column, ForeignKey

from sqlalchemy.ext.mutable import Mutable, MutableList, MutableDict
from object_dict import ObjectDict, objectify, dictify

from photon import MenuStack as MenuStack_

from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class JSONEncoded(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None: value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None: value = json.loads(value)
        return value


class MutableObject(MutableDict):
	@classmethod
	def coerce(cls, key, value):
		if isinstance(value, dict):
			return MutableObject(objectify(value))
		return MutableDict.coerce(key, value)

	def __setattr__(self, attr, value):
		MutableDict.__setitem__(self, attr, value)

	def __getattr__(self, attr):
		if attr in self: return self[attr] # MutableDict.__getitem__(self, index)
		else: return object.__getattr__(self, attr) # return MutableDict.__getattr__(self, attr)

class MenuStack(MutableList, MenuStack_):
	pass

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	menu_stack = Column(MenuStack.as_mutable(JSONEncoded), nullable=False, default=[])
	menu_arguments = Column(MutableObject.as_mutable(JSONEncoded))
	language = Column(Integer)
	blocked = Column(Boolean, default=False)


from config import engine
Base.metadata.create_all(engine)