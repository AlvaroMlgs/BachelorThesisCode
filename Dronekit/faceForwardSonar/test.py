from connect import Connect
import dronekit
from control import Control
import time

vehicle=Connect()

def changeMode():
	vehicle.mode=dronekit.VehicleMode("GUIDED")

def checkMode():
	return vehicle.mode.name=="GUIDED"

ctrl=Control(changeMode,checkMode)

ctrl.take()

time.sleep(1)
checkLoopFlag=False
