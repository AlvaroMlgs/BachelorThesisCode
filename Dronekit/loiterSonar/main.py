# Stock modules
import os
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
logFilename=os.path.dirname(os.path.realpath(__file__))+"/logs/"+str(time.strftime("%Y%m%d-%H%M%S"))+".txt"

fid=open(logFilename,"w")	# Open and then close to create a new file
fid.close()

logging.basicConfig(filename=logFilename,level=logging.DEBUG,format='%(asctime)s %(name)s:%(levelname)s %(message)s')


#### Step 1: Connect to vehicle ####

logStr = "\nStart of script"
print logStr
logging.info(logStr)

vehicle = Connect()

logStr = "Vehicle connected"
print logStr
logging.info(logStr)

#### Step 2: Observe state until "take control" condition is met ####

sonars=[Sonar(3,4),Sonar(14,15),Sonar(17,18)]

"""
for c in range(10):	# Measure several times to have data on velocity
	for s in range(3):
		sonars[s].measureDistance()
		sonars[s].computeVelocity()
"""

for c in range(10):		# Pre-populate arrays
	print ""

	for s in range(3):
		sonars[s].measureDistance()
		sonars[s].computeVelocity()
		sonars[s].calculateCollision()

		logStr = "S%d>> Distance: %.3f [m] Velocity: %.2f [m/s]  Tcollision: %.2f [s]  Tsafe: %.2f [s]" % (s,sonars[s].avgDistance,sonars[s].avgVelocity,sonars[s].Tcollision,sonars[s].Tsafe)
		print logStr
		logging.info(logStr)


logStr = "Starting measurements"
print logStr
logging.info(logStr)

while not (sonars[s].Tsafe < 0 and sonars[s].Tcollision > 0):
#while not avgDistance < 1:

	for s in range(3):

		sonars[s].measureDistance()
		sonars[s].computeVelocity()
		sonars[s].calculateCollision()

		logStr = "S%d>> Distance: %.3f [m] Velocity: %.2f [m/s]  Tcollision: %.2f [s]  Tsafe: %.2f [s]" % (s,sonars[s].avgDistance,sonars[s].avgVelocity,sonars[s].Tcollision,sonars[s].Tsafe)
		print logStr
		logging.info(logStr)

	logStr = ""
	print logStr
	logging.info(logStr)


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
			   takeArgs="GUIDED", checkTakeArgs="GUIDED", giveArgs="LOITER", checkGiveArgs="LOITER")

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

logStr = "Control returned"
print logStr
logging.info(logStr)

sound.tripleBeep(700, 150, 600, 150, 500, 300)

logStr = "\nTerminating script\n"
print logStr
logging.info(logStr)
vehicle.close()


