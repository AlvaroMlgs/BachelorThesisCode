# this script connects to the vehicle via tcp (through mavproxy), displays some
# general parameters and arms the vehicle, takes-off to an altitude of 10 metres,
# and then lands at the same place and disconnects

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math


# Connect to the vehicle
connection_string="127.0.0.1:14550"	# Change to match the vehicle's address
print "Connecting to vehicle on: %s" % connection_string
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print "Autopilot Firmware version: %s" % vehicle.version
print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
print "Global Location: %s" % vehicle.location.global_frame
print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
print "Local Location: %s" % vehicle.location.local_frame    #NED
print "Attitude: %s" % vehicle.attitude
print "Velocity: %s" % vehicle.velocity
print "GPS: %s" % vehicle.gps_0
print "Groundspeed: %s" % vehicle.groundspeed
print "Airspeed: %s" % vehicle.airspeed
print "Gimbal status: %s" % vehicle.gimbal
print "Battery: %s" % vehicle.battery
print "EKF OK?: %s" % vehicle.ekf_ok
print "Last Heartbeat: %s" % vehicle.last_heartbeat
print "Rangefinder: %s" % vehicle.rangefinder
print "Rangefinder distance: %s" % vehicle.rangefinder.distance
print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
print "Heading: %s" % vehicle.heading
print "System status: %s" % vehicle.system_status.state
print "Is Armable?: %s" % vehicle.is_armable
print "Armed: %s" % vehicle.armed    # settable
print "Mode: %s" % vehicle.mode.name    # settable

def arm():
	print "Doing basic pre-arm checks"
	# Don't let the user try to arm until autopilot is ready
	while not vehicle.is_armable: 
		print " Waiting for vehicle to initialise..."
		time.sleep(1)

	vehicle.mode = VehicleMode("GUIDED")	# Copter should arm in GUIDED mode
	print "Arming motors"
	vehicle.armed = True

	while not vehicle.armed:      
		vehicle.arme = True
		print " Waiting for arming..."
		time.sleep(1)

def takeoff(alt):
	print "Taking off! Target altitude: %f metres" % alt
	vehicle.simple_takeoff(alt) # Take off to target altitude

	while True: # Wait until the vehicle reaches a safe height before continuing
		print " Altitude: ", vehicle.location.global_relative_frame.alt      
		if vehicle.location.global_relative_frame.alt>=alt*0.97: # Allow some margin for position error
			print "Reached target altitude: %f metres" % vehicle.location.global_relative_frame.alt
			break
		time.sleep(0.5)	

def landHere():
	print "Landing at current location"
	vehicle.mode = VehicleMode("LAND")
	while True:
		print " Altitude: ", vehicle.location.global_relative_frame.alt
		time.sleep(1)
		if vehicle.location.global_relative_frame.alt<1: # 1 metre margin to allow for position error
			time.sleep(3)
			print "Vehicle is on the ground"
		if vehicle.armed == False:
			print "Vehicle is on the ground and safely disarmed"
			break


##################################################
################# Mission begin ##################

arm() # Arm already sets vehicle into GUIDED mode
takeoff(1) # Vehicle must be in GUIDED mode
time.sleep(2)
landHere()


################# Mission end ####################
##################################################

#Close vehicle object before exiting script
print "Closing vehicle object"
vehicle.close()

print("Test completed")
raw_input("Press Enter to end this script")



