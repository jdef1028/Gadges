# This is a Python function that simulates the Struct function in Ruby
# By using this function, you can construct a object class quickly
# Remarkable gadget

class Struct():
	def __init__(self, *args, **kwargs):
		# init
		for arg in args:
			self.__dict__[arg] = None
		
