import RPi.GPIO as GPIO
import time
import signal

from threads import thrd

class Sonar():
	
	def __init__(self,trigPin,echoPin,bufferLen=5):

		GPIO.setmode(GPIO.BCM)

		self.echoPin=echoPin
		self.trigPin=trigPin

		GPIO.setup(self.trigPin,GPIO.OUT)
		GPIO.setup(self.echoPin,GPIO.IN)

		self.initialTime=time.time()
		self.timeArray=[None]*bufferLen

		self.distance=None
		self.distanceBuffer=[None]*bufferLen

		self.velocity=None
		self.velocityBuffer=[None]*bufferLen

	def __del__(self):
		GPIO.cleanup()


	def measureDistance(self):

		time.sleep(0.05)	# Wait a bit to avoid interference from previous measurement
		print "%.4fs> Wait is over" % time.time()

		def triggerSonar():
			GPIO.output(self.trigPin,False)
			time.sleep(2e-6)    # 2 microseconds
			GPIO.output(self.trigPin,True)
			time.sleep(1e-5)     # 10 microseconds
			GPIO.output(self.trigPin,False)
			print "%.4fs> Sonar triggered" % time.time()
		thrdTriggerSonar=thrd(triggerSonar)
		thrdTriggerSonar.start()

	#	while GPIO.input(self.echoPin)==0:  # Overwrite pulseStart until pulse is detected
	#		pulseStart=time.time()-self.initialTime

	#	while GPIO.input(self.echoPin)==1:  # Overwrite pulseEnd until pulse has ended
	#		pulseEnd=time.time()-self.initialTime

		print "%.4fs> Listening for echo" % time.time()
		a=GPIO.wait_for_edge(self.echoPin,GPIO.RISING,timeout=100)
		pulseStart=time.time()-self.initialTime
		print "%.4fs> Up edge detected" % time.time()
		GPIO.wait_for_edge(self.echoPin,GPIO.FALLING,timeout=100)
		pulseEnd=time.time()-self.initialTime
		print "%.4fs> Down edge detected" % time.time()

		try:

			pulseDuration=pulseEnd-pulseStart
            
			sonarDistance=(pulseDuration/2.0)*343

			if sonarDistance>4:	# Sensor not accurate for higher values
				sonarDistance=-1

		except:
            
			print "Error reading the distance. Trying again"

		else:

			if sonarDistance!=-1:
				
				self.distance=sonarDistance
				# Update buffer
				for b in range(len(self.distanceBuffer)-1,0,-1):	# Shift position of the old values
					self.distanceBuffer[b]=self.distanceBuffer[b-1]
				self.distanceBuffer[0]=self.distance	# Include latest measurement

				# Update time array
				for t in range(len(self.timeArray)-1,0,-1):
					self.timeArray[t]=self.timeArray[t-1]
				self.timeArray[0]=(pulseEnd+pulseStart)/2

			return self.distance

	
	def computeVelocity(self):

		try:	# To avoid divisions by 0 from throwing an error
			# Backward differences with a three-data-points stencil
			self.velocity=(-2*self.distanceBuffer[0]+self.distanceBuffer[1]+self.distanceBuffer[2])/((self.timeArray[0]-self.timeArray[1])+(self.timeArray[0]-self.timeArray[2]))

		except:
			pass

		else:
			for v in range(len(self.velocityBuffer)-1,0,-1):
				self.velocityBuffer[v]=self.velocityBuffer[v-1]
			self.velocityBuffer[0]=self.velocity

			return self.velocity
		





