import threading			# For thread events
from threads import thrd	# For other threads
import sound
import time

class Control:

	def __init__(self,takeFun,checkTakeFun,giveFun,checkGiveFun,takeArgs=None,checkTakeArgs=None,giveArgs=None,checkGiveArgs=None):
		self.takenFlag=threading.Event()	# Create event flag to allow input from check() thread
		self.takeFun=takeFun		# Function executed to take control
		self.checkTakeFun=checkTakeFun	# Condition checked for control taken (Boolean function)
		self.giveFun=giveFun		# Function executed to give control
		self.checkGiveFun=checkGiveFun	# Condition checked for control give (Boolean function)

		if takeArgs!=None: self.takeArgs=takeArgs
		if checkTakeArgs!=None: self.checkTakeArgs=checkTakeArgs
		if giveArgs!=None: self.giveArgs=giveArgs
		if checkGiveArgs!=None: self.checkGiveArgs=checkGiveArgs


	def take(self):

		def takeThrd():
			while not self.takenFlag.isSet():
				try:
					self.takeArgs
				except:
					self.takeFun
				else:
					self.takeFun(self.takeArgs)
				self.takenFlag.wait(0.02)	# Lock thread until released via self.takenFlag.set() in self.check() method or timed out

		takeClass=thrd(takeThrd)
		takeClass.name="takeClass"
		takeClass.start()


	def checkTake(self):

		def checkTakeThrd():
			while not self.takenFlag.isSet():
				try:	# Call function either with or without arguments
					self.checkTakeArgs
				except:
					if self.checkTakeFun():
						time.sleep(0.1)
						sound.beep(1000,1000)
						self.takenFlag.set()
				else:
					if self.checkTakeFun(self.checkTakeArgs):
						time.sleep(0.1)
						sound.beep(1000,1000)
						self.takenFlag.set()

		checkTakeClass=thrd(checkTakeThrd)
		checkTakeClass.name="checkTakeClass"
		checkTakeClass.start()
		

	def give(self):

		def giveThrd():
			while self.takenFlag.isSet():
				try:
					self.giveArgs
				except:
					self.giveFun
				else:
					self.giveFun(self.giveArgs)
				self.takenFlag.wait(0.02)	# Lock thread until released via self.takenFlag.set() by self.check() method or timed out

		giveClass=thrd(giveThrd)
		giveClass.name="giveClass"
		giveClass.start()


	def checkGive(self):

		def checkGiveThrd():
			while self.takenFlag.isSet():
				try:	# Call function either with or without arguments
					self.checkGiveArgs
				except:
					if self.checkGiveFun():
						self.takenFlag.clear()
				else:
					if self.checkGiveFun(self.checkGiveArgs):
						self.takenFlag.clear()

		checkGiveClass=thrd(checkGiveThrd)
		checkGiveClass.name="checkGiveClass"
		checkGiveClass.start()
		
