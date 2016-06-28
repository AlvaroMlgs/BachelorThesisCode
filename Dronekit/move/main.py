
# Stock modules
import time
import math
import threading
import dronekit
from pymavlink import mavutil

# Custom modules
from connect import Connect  # For connecting to the vehicle
from observe import Observe  # For observing the state of the vehicle
from threads import thrd  # For multithreading capabilities
import sound  # For playing sounds on the background (without affecting main thread)
import angle  # For operations with angles (to avoid discontinuities)
from control import Control  # For taking and giving control to the pilot, checking if it was successful
from auto import Auto  # For controling autonomous flight

#### Step 1: Connect to vehicle ####

vehicle = Connect()

#### Step 2: Observe state until "take control" condition is met ####

# ch7Obs=Observe(vehicle.channels["7"], 2001)
# print "Waiting for condition to be met"
# 
# ch7Obs.update(vehicle.channels["7"])
# while not ch7Obs.geq(ch7Obs.value-200):	# 200 PWM tolerance
# 	timeLoop = time.clock()
# 	while (time.clock()-timeLoop) < 0.02:  # Update rate of vehicle class is 50 Hz
# 		pass  # Do not continue until there is new data to update
# 	ch7Obs.update(vehicle.channels["7"])
# 	print "CH7 current value: %i   CH7 target: %i" % (ch7Obs.variable, ch7Obs.value)
# 
# print "Condition met"
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

def do_move(distance,tMove,direction=[1,0,0]):

	def goto_position_target_local_ned(north, east, down):
		"""	
		Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
		location in the North, East, Down frame.

		It is important to remember that in this frame, positive altitudes are entered as negative 
		"Down" values. So if down is "10", this will be 10 metres below the home altitude.

		At time of writing, acceleration and yaw bits are ignored.

		"""
		msg = vehicle.message_factory.set_position_target_local_ned_encode(
			0,       # time_boot_ms (not used)
			0, 0,    # target system, target component
			mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
			0b0000111111111000, # type_mask (only positions enabled)
			north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
			0, 0, 0, # x, y, z velocity in m/s  (not used)
			0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
			0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
		# send command to vehicle
		vehicle.send_mavlink(msg)

		
	def body2ned(frontBody,leftBody,upBody=-vehicle.location.global_relative_frame.alt):

		yaw=vehicle.attitude.yaw
		yawCorrected=yaw+40/180/math.pi	# Weird offset. Don't know why, but it works
		north=frontBody*math.cos(yawCorrected)+leftBody*math.sin(yawCorrected)
		east=frontBody*math.sin(yawCorrected)-leftBody*math.cos(yawCorrected)
		down=-upBody
		return [north,east,down]


	goto_position_target_local_ned(*body2ned(distance*direction[0],distance*direction[1],distance*direction[2]))
	print "Moving"

	time.sleep(tMove+1)


def wait(seconds):
	time.sleep(seconds)
	return True


autoMove = Auto(do_move, wait, [1,10,[1,0,0]], 10)


print "Starting autonomous flight"
autoMove.fly()
autoMove.stop()

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


