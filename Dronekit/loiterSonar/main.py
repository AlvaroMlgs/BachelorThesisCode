# Stock modules
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

#### Step 1: Connect to vehicle ####

initTime=time.time()
print "%.3fs>> Start of script" % (time.time()-initTime)
vehicle = Connect()
print "%.3fs>> Vehicle connected" % (time.time()-initTime)

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

		print "S%d>> Distance: %.3f [m] Velocity: %.2f [m/s]  Tcollision: %.2f [s]  Tsafe: %.2f [s]" % (s,sonars[s].avgDistance,sonars[s].avgVelocity,sonars[s].Tcollision,sonars[s].Tsafe)


print "%.3fs>> Starting measurements" % (time.time()-initTime)
while not (sonars[s].Tsafe < 0 and sonars[s].Tcollision > 0):
#while not avgDistance < 1:

	for s in range(3):

		sonars[s].measureDistance()
		sonars[s].computeVelocity()
		sonars[s].calculateCollision()


		print "S%d>> Distance: %.3f [m] Velocity: %.2f [m/s]  Tcollision: %.2f [s]  Tsafe: %.2f [s]" % (s,sonars[s].avgDistance,sonars[s].avgVelocity,sonars[s].Tcollision,sonars[s].Tsafe)
	print ""


print "%.3fs>> Condition met" % (time.time()-initTime)
sound.beep(440, 200)


#### Step 3: Take control ####

def changeMode(mode):
	vehicle.mode = dronekit.VehicleMode(mode)


def checkMode(mode):
	return vehicle.mode.name==mode


ctrl = Control(takeFun=changeMode, checkTakeFun=checkMode, giveFun=changeMode, checkGiveFun=checkMode,
			   takeArgs="LOITER", checkTakeArgs="LOITER", giveArgs="ALT_HOLD", checkGiveArgs="ALT_HOLD")

print "%.3fs>> Taking control" % (time.time()-initTime)
ctrl.take()
ctrl.checkTake()

while not threading.activeCount() <= 3:
	time.sleep(0.02)
print "%.3fs>> Control taken" % (time.time()-initTime)


#### Step 4: Autonomous flight ####

time.sleep(10)	# Mission does nothing, just loiters for 10 seconds

print "%.3fs>> Mission finished" % (time.time()-initTime)

#### Step 5: Return control to the pilot ####

print "%.3fs>> Returning control" % (time.time()-initTime)

# Recovering ctrl class instance that was created in step 3
ctrl.give()
ctrl.checkGive()

while not threading.activeCount() <= 3:
	time.sleep(0.02)
print "%.3fs>> Control returned" % (time.time()-initTime)

sound.tripleBeep(700, 150, 600, 150, 500, 300)

print "%.3fs>> Terminating script" % (time.time()-initTime)
vehicle.close()


