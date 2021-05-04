from photon import Router as Router_
from photon import set_find_router
from config import sessionmaker
from dbscheme import User

#def find_router(**kwargs):
@set_find_router
def find_router(user_id):
	db = sessionmaker()
	user = db.query(User).filter(User.id==user_id).first()
	if not user:
		user = User(id=user_id)
		db.add(user)
		db.commit()

	router = Router(user.menu_stack, user=user, db=db)

	return router

class Router(Router_):
	def __del__(self):
		self.db.commit()
