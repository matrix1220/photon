
def key(key, *args, **kwargs):
	return [0, key, args, kwargs]

def act(menu, *args, **kwargs):
	return [1, menu.id, args, kwargs]
	
def explicit_act(menu, *args, **kwargs):
	return [2, menu.id, args, kwargs]

# def back():
# 	return [3]
