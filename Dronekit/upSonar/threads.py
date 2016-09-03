import threading

class thrd(threading.Thread):

	def __init__(self,fun,*args):
		threading.Thread.__init__(self)
		self.function=fun
		if len(args)!=0:
			self.arguments=args
		#else:
		#	self.arguments=None

	def run(self):
		#if self.arguments==None:
		#	self.function
		#else:
		#	self.function(*self.arguments)

		try:
			self.arguments
		except:
			self.function()
		else:
			self.function(*self.arguments)
