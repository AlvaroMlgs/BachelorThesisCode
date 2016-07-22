# Stock modules
import sys
import logging
import time
import dronekit
import threading
import numpy

# Custom modules
from connect import Connect  # For connecting to the vehicle
from observe import Observe  # For observing the state of the vehicle
from threads import thrd  # For multithreading capabilities
import sound  # For playing sounds on the background (without affecting main thread)
import angle  # For operations with angles (to avoid discontinuities)
from control import Control  # For taking and giving control to the pilot, checking if it was successful
from auto import Auto  # For controling autonomous flight
from sonar import Sonar	# For sonar sensors operation

## Set-up logging ##
logFilename=".\\logs\\"+str(time.strftime("%Y%m%d-%H%M%S"))+".txt"

fid=open(logFilename,"w")	# Open and then close to create a new file
fid.close()

logging.basicConfig(filename=logFilename,level=logging.DEBUG,format='%(asctime)s %(name)s:%(levelname)s %(message)s')


#### Step 1: Connect to vehicle ####

vehicle = Connect()

#### Step 2: Observe state until "take control" condition is met ####

sonars=[Sonar(2,3),Sonar(14,15),Sonar(17,18)]

for c in range(10):	# Measure several times to have data on velocity
	for s in range(3):
		sonars[s].measureDistance()
		sonars[s].computeVelocity()

	try:	# In the case of bad measurement, avoid errors related to None type

		stdDistance=numpy.std([numpy.mean(sonars[0].distanceBuffer),numpy.mean(sonars[1].distanceBuffer),numpy.mean(sonars[2].distanceBuffer)])

		avgDistance=numpy.mean([numpy.mean(sonars[0].distanceBuffer),numpy.mean(sonars[1].distanceBuffer),numpy.mean(sonars[2].distanceBuffer)])
		avgVelocity=numpy.mean([numpy.mean(sonars[0].velocityBuffer),numpy.mean(sonars[1].velocityBuffer),numpy.mean(sonars[2].velocityBuffer)])
		#logStr = "Mean sonar distance: %.3f [m]  STD: %.4f" % (avgDistance,stdDistance)
		#print logStr
		#logging.info(logStr)

		#Tcollision=min(sonars[0].distance,sonars[1].distance,sonars[2].distance)/max(sonars[0].velocity,sonars[1].velocity,sonars[2].velocity)	# Time to collision at current velocity
		Tcollision=avgDistance/avgVelocity
		Treaction=0		# Time for the script to take control
		Tstop=1		# Time for the script to stop the vehicle (at a given velocity)
		Tmargin=0	# Accounting for clearance to obstacle and measurement errors

		Tsafe=Tcollision-Treaction-Tstop-Tmargin

		logStr = "Distance: %.3f [m] std: %.4f  Velocity: %.2f [m/s]  Tcollision: %.2f [s]  Tsafe: %.2f [s]" % (avgDistance,stdDistance,avgVelocity,Tcollision,Tsafe)
		print logStr
		logging.info(logStr)

	except: pass

while not (Tsafe < 0 and Tcollision > 0):
#while not avgDistance < 1:

	for s in range(3):
		sonars[s].measureDistance()
		sonars[s].computeVelocity()

	try:	# In the case of bad measurement, avoid errors related to None type

		stdDistance=numpy.std([numpy.mean(sonars[0].distanceBuffer),numpy.mean(sonars[1].distanceBuffer),numpy.mean(sonars[2].distanceBuffer)])

		if stdDistance < 0.1:	# Do not consider large discrepancies between sensors
			avgDistance=numpy.mean([numpy.mean(sonars[0].distanceBuffer),numpy.mean(sonars[1].distanceBuffer),numpy.mean(sonars[2].distanceBuffer)])
			avgVelocity=numpy.mean([numpy.mean(sonars[0].velocityBuffer),numpy.mean(sonars[1].velocityBuffer),numpy.mean(sonars[2].velocityBuffer)])
			#logStr = "Mean sonar distance: %.3f [m]  STD: %.4f" % (avgDistance,stdDistance)
			#print logStr
			#logging.info(logStr)

			#Tcollision=min(sonars[0].distance,sonars[1].distance,sonars[2].distance)/max(sonars[0].velocity,sonars[1].velocity,sonars[2].velocity)	# Time to collision at current velocity
			Tcollision=avgDistance/avgVelocity
			Treaction=0		# Time for the script to take control
			Tstop=1		# Time for the script to stop the vehicle (at a given velocity)
			Tmargin=0	# Accounting for clearance to obstacle and measurement errors

			Tsafe=Tcollision-Treaction-Tstop-Tmargin

			logStr = "Distance: %.3f [m] std: %.4f  Velocity: %.2f [m/s]  Tcollision: %.2f [s]  Tsafe: %.2f [s]" % (avgDistance,stdDistance,avgVelocity,Tcollision,Tsafe)
			print logStr
			logging.info(logStr)

	except: pass

logStr = "Condition met"
print logStr
logging.info(logStr)
sound.beep(440, 200)


#### Step 3: Take control ####

def changeMode(mode):
	vehicle.mode = dronekit.VehicleMode(mode)


def checkMode(mode):
	return vehicle.mode.name==mode


ctrl = Control(takeFun=changeMode, checkTakeFun=checkMode, giveFun=changeMode, checkGiveFun=checkMode,
			   takeArgs="LOITER", checkTakeArgs="LOITER", giveArgs="ALT_HOLD", checkGiveArgs="ALT_HOLD")

logStr = "Taking control"
print logStr
logging.info(logStr)

ctrl.take()
ctrl.checkTake()

while not threading.activeCount() <= 3:
	time.sleep(0.02)
logStr = "Control taken"
print logStr
logging.info(logStr)


#### Step 4: Autonomous flight ####

time.sleep(10)	# Mission does nothing, just loiters for 10 seconds

logStr = "Mission finished"
print logStr
logging.info(logStr)

#### Step 5: Return control to the pilot ####

logStr = "Returning control"
print logStr
logging.info(logStr)

# Recovering ctrl class instance that was created in step 3
ctrl.give()
ctrl.checkGive()

while not threading.activeCount() <= 3:
	time.sleep(0.02)

sound.tripleBeep(700, 150, 600, 150, 500, 300)

logStr = "\nTerminating script"
print logStr
logging.info(logStr)
vehicle.close()


