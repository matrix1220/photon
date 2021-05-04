from .menu import menu_classes

class MenuStack(list):
	def current(self):
		if not self.empty():
			return menu_classes[self[-1][0]], *self[-1][1:]
	def current_menu(self):
		if not self.empty():
			return menu_classes[self[-1][0]]

	def set_current(self, menu_class_id, args, kwargs):
		if self.empty():
			self.append([menu_class_id, args, kwargs])
		else:
			self[-1] = [menu_class_id, args, kwargs]

	# def pop(self):
	# 	return self.pop()
	def push(self, menu_class_id, args, kwargs):
		return self.append([menu_class_id, args, kwargs])
	def reset(self):
		self.clear()
	def empty(self):
		return len(self)==0