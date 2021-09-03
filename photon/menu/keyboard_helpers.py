
def key(key, *args, **kwargs):
	return [0, key, args, kwargs]

def act(menu, *args, **kwargs):
	return [1, menu.id, args, kwargs]
	
def explicit_act(menu, *args, **kwargs):
	return [2, menu.id, args, kwargs]

def reset(menu, *args, **kwargs):
	return [3, menu.id, args, kwargs]

def func(func_, *args, **kwargs):
	return [4, func_.id, args, kwargs]

def back():
	return [5]

none = [6]


