class Observe:
	"""
	The Observe class stores two values:
		self.value		is the target value on a certain state variable of the observed system
		self.variable	is the actual (probably changing) value of that state variable
	
	self.value and self.variable can be set at instance initialization, or with the self.update() method
	Additionally, there exist some methods that allow for easy comparison of self.variable vs self.value:
		Method		|	.equ()	.neq()	.gtr()	.geq()	.lss()	.leq()	|
		Equivalent	|	==		!=		>		>=		<		<=		|
	With these methods self.value will not be updated
	"""

	def __init__(self,*args):
		if len(args)==0:
			self.initial=None
			self.value=None
			self.variable=None
		elif len(args)==1:
			self.initial=args[0]
			self.value=None
			self.variable=None
		elif len(args)==2:
			self.initial=args[0]
			self.value=args[1]
			self.variable=None
		elif len(args)==3:
			self.initial=args[0]
			self.value=args[1]
			self.variable=args[2]

	def update(self,var,*args):
		self.variable=var
		if len(args)>0:
			self.value=args[0]

	def equ(self,*args):
		if len(args)==1:	# If argument inserted, compare against it instead of using self.value
			if self.variable==args[0]:
				return True
			else:
				return False
		else:
			if self.variable==self.value:
				return True
			else:
				return False
	def neq(self,*args):
		if len(args)==1:	# If argument inserted, compare against it instead of using self.value
			if self.variable!=args[0]:
				return True
			else:
				return False
		else:
			if self.variable!=self.value:
				return True
			else:
				return False
	def gtr(self,*args):
		if len(args)==1:	# If argument inserted, compare against it instead of using self.value
			if self.variable>args[0]:
				return True
			else:
				return False
		else:
			if self.variable>self.value:
				return True
			else:
				return False
	def geq(self,*args):
		if len(args)==1:	# If argument inserted, compare against it instead of using self.value
			if self.variable>=args[0]:
				return True
			else:
				return False
		else:
			if self.variable>=self.value:
				return True
			else:
				return False
	def lss(self,*args):
		if len(args)==1:	# If argument inserted, compare against it instead of using self.value
			if self.variable<args[0]:
				return True
			else:
				return False
		else:
			if self.variable<self.value:
				return True
			else:
				return False
	def leq(self,*args):
		if len(args)==1:	# If argument inserted, compare against it instead of using self.value
			if self.variable<=args[0]:
				return True
			else:
				return False
		else:
			if self.variable<=self.value:
				return True
			else:
				return False
