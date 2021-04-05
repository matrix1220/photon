

# class methods_meta(type):
# 	def __getattr__(self, key):
# 		return key

# class methods(metaclass=methods_meta):
# 	pass

# print(methods.hello)

x = ['asd', 'qwe']
print( {y:y for y in x} )