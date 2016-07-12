import threading
from threads import thrd


class Auto:

	def __init__(self,missionFun,stopFun,missionArgs=None,stopArgs=None):
		self.stopAutoFlag=threading.Event()	# For stopping the autonomous flight at any time

		self.missionFun=missionFun
		self.stopFun=stopFun

		if missionArgs!=None: self.missionArgs=missionArgs
		if stopArgs!=None: self.stopArgs=stopArgs


	def fly(self):
		
		def flyThrd():
			while not self.stopAutoFlag.isSet():
				try:
					self.missionArgs
				except:
					self.missionFun
				else:
					self.missionFun(self.missionArgs)

		flyClass=thrd(flyThrd)
		flyClass.name="flyClass"
		flyClass.start()


	def stop(self):

		def stopThrd():
			while not self.stopAutoFlag.isSet():
				try:
					self.stopArgs
				except:
					if self.stopFun: self.stopAutoFlag.set()
				else:
					if self.stopFun(self.stopArgs): self.stopAutoFlag.set()
                
		stopClass=thrd(stopThrd)
		stopClass.name="stopClass"
		stopClass.start()






