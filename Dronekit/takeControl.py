# this script connects to the vehicle via tcp (through mavproxy), displays some
# general parameters and arms the vehicle, waiting 10 seconds to disarm and end


from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math


# Connect to the vehicle
connection_string="127.0.0.1:14550"	# Change to match the vehicle's address
"""
Valid connection strings:
	TCP connection: "tcp:[ip:port]"
	UDP connection: "[ip:port]"
	Serial connection: "com[port]"
"""
print "Connecting to vehicle on: %s" % connection_string
vehicle = connect(connection_string, wait_ready=True)

def pause():
	programPause = raw_input("Press the <ENTER> key to continue...")


def takeControl():
	if vehicle.location.global_relative_frame.alt >=0.5:
		vehicle.mode=VehicleMode("ALT_HOLD")
		return True	#controlTakenFlag=True
	
controlTakenFlag=False
while controlTakenFlag==False:
	print "Trying to take control"
	controlTakenFlag=takeControl()

endFlag=False
while not endFlag:
	pause()
	endFlag=True

vehicle.close()

