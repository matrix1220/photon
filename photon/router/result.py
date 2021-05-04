

class Result(Exception):
	def __init__(self, arg):
		self.arg = arg

class Incorrect(Result):
	pass

class Done(Result):
	pass