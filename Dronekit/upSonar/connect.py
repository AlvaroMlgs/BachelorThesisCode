import dronekit

def Connect(mode="udp",address=["127.0.0.1",14550]):
	""" Connects to the vehicle defined in the arguments and returns its class
		Admissible modes: udp (default), serial or tcp """

	if mode=="serial":
		connection_string=address[0]
		baudrate=str(address[1])
	elif mode=="udp":
		connection_string=str(address[0])+":"+str(address[1])
	elif mode=="tcp":
		connection_string="tcp:"+str(address[0])+":"+str(address[1])
	else:
		raise Exception('Connection mode has to be "serial", "udp" or "tcp"')


	print "Connecting on: %s" % connection_string
	if mode=="serial":
		vehicle=dronekit.connect(ip=connection_string,wait_ready=True,rate=50,baud=baudrate)
	else:
		vehicle=dronekit.connect(ip=connection_string,wait_ready=True,rate=50)

	print "Vehicle connected"
	return vehicle
