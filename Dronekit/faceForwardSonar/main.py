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

vehicle = Connect()

#### Step 2: Observe state until "take control" condition is met ####

initYaw=vehicle.heading	# Temporal fix (I hope) for step 4

sonars=[Sonar(2,3),Sonar(14,15),Sonar(17,18)]

for c in range(3):	# Measure several times to have data on velocity
	for s in range(3):
		sonars[s].measureDistance()
		#sonars[s].computeVelocity()

try:	# In the case of bad measurement, avoid errors related to None type
	avgDistance=numpy.mean([sonars[0].distance,sonars[1].distance,sonars[2].distance])
	print "Mean sonar distance: %.3f [m]" % avgDistance
except: pass


""" Maybe at a later time
Tcollision=min(sonars[0].distance,sonars[1].distance,sonars[2].distance)/max(sonars[0].velocity,sonars[1].velocity,sonars[2].velocity)	# Time to collision at current velocity
Treaction=0		# Time for the script to take control
Tstop=0		# Time for the script to stop the vehicle (at a given velocity)
Tmargin=0	# Accounting for clearance to obstacle and measurement errors

Tsafe=Tcollision-Treaction-Tstop-Tmargin
"""

#while not Tsafe < 0 and not min(sonars[0].distance,sonars[1].distance,sonars[2].distance) < 0.5:
while not avgDistance < 1:

	for s in range(3):
		sonars[s].measureDistance()
		#sonars[s].computeVelocity()

	try:	# In the case of bad measurement, avoid errors related to None type
		avgDistance=numpy.mean([sonars[0].distance,sonars[1].distance,sonars[2].distance])
		print "Mean sonar distance: %.3f [m]" % avgDistance
	except: pass

	"""
	Tcollision=min(sonars[0].distance,sonars[1].distance,sonars[2].distance)/max(sonars[0].velocity,sonars[1].velocity,sonars[2].velocity)	# Time to collision at current velocity
	Treaction=0		# Time for the script to take control
	Tstop=0		# Time for the script to stop the vehicle (at a given velocity)
	Tmargin=0	# Accounting for clearance to obstacle and measurement errors

	Tsafe=Tcollision-Treaction-Tstop-Tmargin
	"""


print "Condition met"
sound.beep(440, 200)


#### Step 3: Take control ####

def changeMode(mode):
	vehicle.mode = dronekit.VehicleMode(mode)


def checkMode(mode):
	return vehicle.mode.name==mode


ctrl = Control(takeFun=changeMode, checkTakeFun=checkMode, giveFun=changeMode, checkGiveFun=checkMode,
			   takeArgs="GUIDED", checkTakeArgs="GUIDED", giveArgs="ALT_HOLD", checkGiveArgs="ALT_HOLD")

print "Taking control"
ctrl.take()
ctrl.checkTake()

while not threading.activeCount() <= 3:
	time.sleep(0.02)
print "Control taken"


#### Step 4: Autonomous flight ####

def cmd_yaw(heading, relative=False):
	if relative:
		is_relative = 1  # yaw relative to direction of travel
	else:
		is_relative = 0  # yaw is an absolute angle

	# create the CONDITION_YAW command using command_long_encode()
	msg = vehicle.message_factory.command_long_encode(
		0, 0,  # target system, target component
		dronekit.mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
		0,  # confirmation
		heading,  # param 1, yaw in degrees
		0,  # param 2, yaw speed deg/s
		1,  # param 3, direction -1 ccw, 1 cw
		is_relative,  # param 4, relative offset 1, absolute angle 0
		0, 0, 0)  # param 5 ~ 7 not used
	# send command to vehicle
	vehicle.send_mavlink(msg)


def condition_yaw(yaw):
	return abs(vehicle.heading-yaw) <= 5


autoYaw = Auto(cmd_yaw, condition_yaw, initYaw, initYaw)

print "Starting autonomous flight"
autoYaw.fly()
autoYaw.stop()

while not threading.activeCount() <= 3:
	time.sleep(0.02)
print "Mission finished"

#### Step 5: Return control to the pilot ####

print "Returning control"

# Recovering ctrl class instance that was created in step 3
ctrl.give()
ctrl.checkGive()

while not threading.activeCount() <= 3:
	time.sleep(0.02)

sound.tripleBeep(700, 150, 600, 150, 500, 300)

print "\nTerminating script"
vehicle.close()


