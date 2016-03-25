from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, Command
from pymavlink import mavutil # Needed for command message definitions
import time
import math


# Connect to the vehicle
connection_string="tcp:127.0.0.1:5760"	# Change to match the vehicle's address
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

def gotoPostitionLocalNED(north,east,down):
    """
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified
    location in the North, East, Down frame.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down,
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    # send command to vehicle
    vehicle.send_mavlink(msg)
	
    while True:

		nor=vehicle.location.local_frame.north
		eas=vehicle.location.local_frame.east
		dow=vehicle.location.local_frame.down
		
		northCond=math.fabs(nor-north)<1 # 1 metre margins to allow for possition error
		eastCond=math.fabs(eas-east)<1
		downCond=math.fabs(dow-down)<1
		
		print "Position NED: %s" % vehicle.location.local_frame
		if northCond==True and eastCond==True and downCond==True:
			print "Reached target position"
			break
		time.sleep(1)

def getCoordinatesFromRelativeNED(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned Location has the same `alt` value
    as `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.
    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius=6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    return LocationGlobal(newlat, newlon,original_location.alt)

def add_square_mission(aLocation, aSize):
    """
    Adds a takeoff command and four waypoint commands to the current mission. 
    The waypoints are positioned to form a square of side length 2*aSize around the specified LocationGlobal (aLocation).

    The function assumes vehicle.commands matches the vehicle mission state 
    (you must have called download at least once in the session and after clearing the mission)
    """	

    cmds = vehicle.commands

    print " Clear any existing commands"
    cmds.clear() 
    
    print " Define/add new commands."
    # Add new commands. The meaning/order of the parameters is documented in the Command class. 
     
    #Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, 10))

    #Define the four MAV_CMD_NAV_WAYPOINT locations and add the commands
    point1 = getCoordinatesFromRelativeNED(aLocation, aSize, -aSize)
    point2 = getCoordinatesFromRelativeNED(aLocation, aSize, aSize)
    point3 = getCoordinatesFromRelativeNED(aLocation, -aSize, aSize)
    point4 = getCoordinatesFromRelativeNED(aLocation, -aSize, -aSize)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point1.lat, point1.lon, 11))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point2.lat, point2.lon, 12))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point3.lat, point3.lon, 13))
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))
    #add dummy waypoint "5" at point 4 (lets us know when have reached destination)
    cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, point4.lat, point4.lon, 14))    

    print " Upload new commands to vehicle"
    cmds.upload()
    waypointNumber=cmds.count
    return waypointNumber # Number of waypoints stored, to check if mission is complete

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

def returnToLaunch():
	print "Returning To Launch"
	vehicle.mode = VehicleMode("RTL")
	while True:
		print " Altitude: ", vehicle.location.global_relative_frame.alt
		time.sleep(1)
		if vehicle.location.global_relative_frame.alt<1: # 1 metre margin to allow for position error
			time.sleep(3)
			print "Vehicle is on the ground"
		if vehicle.armed == False:
			print "Vehicle is on the ground and safely disarmed"
			break


arm() # Arm already sets vehicle into GUIDED mode
waypointNumber=add_square_mission(vehicle.location.global_frame,30)
takeoff(10) # Vehicle must be in GUIDED mode
vehicle.commands.next=0 # Reset mission set to first (0) waypoint
vehicle.mode = VehicleMode("AUTO") # Set mode to AUTO to start mission
while True:
	print "Next waypoint # ", vehicle.commands.next
	print "Waypoint number:", waypointNumber
	if vehicle.commands.next>=waypointNumber:
		print "Reached end of mission"
		break
	time.sleep(1)
returnToLaunch()


#Close vehicle object before exiting script
print "Closing vehicle object"
vehicle.close()

print("Test completed")
time.sleep(5)



