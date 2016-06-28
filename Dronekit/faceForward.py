# this script connects to the vehicle via tcp (through mavproxy), displays some
# general parameters and arms the vehicle, waiting 10 seconds to disarm and end


from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math
import winsound


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

########## FUNCTION DEFINITIONS ############

def pause():
	programPause = raw_input("Press the <ENTER> key to continue...")


def takeControl():
	vehicle.mode=VehicleMode("GUIDED")
	winsound.Beep(600,1000)	# Make beep sound to alert of mode change
	if vehicle.mode=="GUIDED":
		return True	#controlTakenFlag=True
	else:
		return False

def returnControl():
	vehicle.mode=VehicleMode("ALT_HOLD")
	time.sleep(0.1)
	for s in range(5):
		winsound.Beep(1500,300)	# Make beep sound to alert of mode change
		time.sleep(0.1)
	winsound.Beep(1500,1000)
	print vehicle.mode
	if vehicle.mode=="GUIDED":
		return True	#controlTakenFlag=True
	else:
		return False

def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

##################### SCRIPT ######################################

while vehicle.armed==False:		# Won't do anything if vehicle not manually armed
	print "Waiting for pilot to arm the vehicle"
	time.sleep(1)

armedHeading=vehicle.heading
print "Initial heading is %i" % armedHeading 

while abs(vehicle.heading-armedHeading)<90:		# Infinite loop until condition for taking control is met
	print "Heading difference: %i" % (vehicle.heading-armedHeading)
	time.sleep(0.5)

controlTakenFlag=False
while controlTakenFlag==False:	# Infinite loop until control is taken (mode==GUIDED)
	print "Trying to take control"
	controlTakenFlag=takeControl()

while not abs(vehicle.heading-armedHeading)<=2:	# Wait until heading is back to armedHeading
	condition_yaw(armedHeading,relative=False)	# Command to return to armed Heading
	print "Heading difference: %i" % (vehicle.heading-armedHeading)
	time.sleep(0.1)

while controlTakenFlag==True:	# Loop until control returned to the pilot
	controlTakenFlag=returnControl()
print "Control returned to the pilot"

endFlag=False
while not endFlag:
	print "Ending script"
	pause()
	endFlag=True

vehicle.close()

