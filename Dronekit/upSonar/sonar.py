import RPi.GPIO as GPIO
import time
import signal
import numpy

from threads import thrd

class Sonar():
	
	def __init__(self,trigPin,echoPin,bufferLen=5):

		GPIO.setmode(GPIO.BCM)

		self.echoPin=echoPin
		self.trigPin=trigPin

		GPIO.setup(self.trigPin,GPIO.OUT)
		GPIO.setup(self.echoPin,GPIO.IN)

		self.distance=100
		self.distanceBuffer=[100]*bufferLen
		self.avgDistance=100

		self.velocity=1e-5
		self.velocityBuffer=[1e-5]*bufferLen
		self.avgVelocity=1e-5

		self.initialTime=time.time()
		self.timeArray=[time.time()-self.initialTime]*bufferLen

		self.Tcollision=100
		self.Treaction=0.5
		self.Tstop=1
		self.Tmargin=0.5
		self.Tsafe=100

	def __del__(self):
		GPIO.cleanup()


	def measureDistance(self):

		time.sleep(0.05)	# Wait a bit to avoid interference from previous measurement

		def triggerSonar():
			GPIO.output(self.trigPin,False)
			time.sleep(2e-6)    # 2 microseconds
			GPIO.output(self.trigPin,True)
			time.sleep(1e-5)     # 10 microseconds
			GPIO.output(self.trigPin,False)
		thrdTriggerSonar=thrd(triggerSonar)
		thrdTriggerSonar.start()

	#	while GPIO.input(self.echoPin)==0:  # Overwrite pulseStart until pulse is detected
	#		pulseStart=time.time()-self.initialTime
			# Performing rolling average over the buffers to reduce noise-related errors

	#	while GPIO.input(self.echoPin)==1:  # Overwrite pulseEnd until pulse has ended
	#		pulseEnd=time.time()-self.initialTime

		GPIO.wait_for_edge(self.echoPin,GPIO.RISING,timeout=100)
		pulseStart=time.time()-self.initialTime
		GPIO.wait_for_edge(self.echoPin,GPIO.FALLING,timeout=100)
		pulseEnd=time.time()-self.initialTime

		try:

			pulseDuration=pulseEnd-pulseStart
            
			sonarDistance=(pulseDuration/2.0)*340

			if sonarDistance<4:	# Sensor not accurate for higher values
				self.distance=sonarDistance

				# Update buffer
				for b in range(len(self.distanceBuffer)-1,0,-1):	# Shift position of the old values
					self.distanceBuffer[b]=self.distanceBuffer[b-1]
				self.distanceBuffer[0]=self.distance	# Include latest measurement

				# Update filtered distance
				self.avgDistance=numpy.mean(self.distanceBuffer)

				# Update time array
				for t in range(len(self.timeArray)-1,0,-1):
					self.timeArray[t]=self.timeArray[t-1]
				self.timeArray[0]=(pulseEnd+pulseStart)/2

				return self.distance

		except:
			print "Error reading the distance. Trying again"


	def computeVelocity(self):

		try:	# To avoid divisions by 0 from throwing an error

			# Backward differences with a three-data-points stencil
			self.velocity=(2*self.distanceBuffer[0]-self.distanceBuffer[1]-self.distanceBuffer[2])/(2*self.timeArray[0]-self.timeArray[1]-self.timeArray[2])

		except:
			pass

		else:
			for v in range(len(self.velocityBuffer)-1,0,-1):
				self.velocityBuffer[v]=self.velocityBuffer[v-1]
			self.velocityBuffer[0]=self.velocity

			self.avgVelocity=numpy.mean(self.velocityBuffer)

			return self.avgVelocity
		
	
	def calculateCollision(self):
		
		self.Tcollision=self.avgDistance/self.avgVelocity
		self.Tsafe=self.Tcollision-self.Treaction-self.Tstop-self.Tmargin

		return self.Tsafe
