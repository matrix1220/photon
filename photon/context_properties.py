
from .menu import MenuStack


class ContextProperties:
	def __init__(self, metadata):
		self.metadata = metadata

class MenuContextProperties(ContextProperties):
	def __init__(self, metadata):
		super().__init__(metadata)
		self.menu_stack = MenuStack()
		self.keyboard = None


# class ContextProperties:
# 	def __init__(self, **kwargs):
# 		for x, y in kwargs.items():
# 			object.__setattr__(self, x, y)

# 		object.__setattr__(self, "references", {})
# 		#object.__setattr__(self, "manager", ContextManager(self))

# 	def reference_properties(self, object_, properties):
# 		for property_ in properties:
# 			self.references[property_] = object_

# 	def __getattr__(self, key):
# 		if key not in self.references: return
# 		return getattr(self.references[key], key)

# 	def __setattr__(self, key, value):
# 		if key not in self.references: return
# 		return setattr(self.references[key], key, value)