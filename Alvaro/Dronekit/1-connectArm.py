from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math


# Connect to the vehicle
connection_string="127.0.0.1:14450"	# Change to match the vehicle's address
"""
Valid connection strings:
	TCP connection: "tcp:[ip:port]"
	UDP connection: "[ip:port]"
	Serial connection: "com[port]"
"""
print "Connecting to vehicle on: %s" % connection_string
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print "Autopilot Firmware version: %s" % vehicle.version
#print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
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
		print " Waiting for arming..."
		time.sleep(1)


arm()
if vehicle.armed:
	print "Vehicle is now armed"
	time.sleep(10)	# Allow some time for the user to read the message




#Close vehicle object before exiting script
print "Closing vehicle object"
vehicle.close()

print("Test completed")
time.sleep(5)



