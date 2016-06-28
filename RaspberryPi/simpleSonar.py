import RPi.GPIO as GPIO
import time


#### SETUP ####

GPIO.setmode(GPIO.BCM)

sonarTrigPin=14
sonarEchoPin=15

GPIO.setup(sonarTrigPin,GPIO.OUT)
GPIO.setup(sonarEchoPin,GPIO.IN)


#### MAIN LOOP ####

try:
    
	while True:

		time.sleep(0.2)

		time.sleep(0.000002)
		GPIO.output(sonarTrigPin,False)
		time.sleep(0.000002)    # 2 microseconds
		GPIO.output(sonarTrigPin,True)
		time.sleep(0.00001)     # 10 microseconds
		GPIO.output(sonarTrigPin,False)

		while GPIO.input(sonarEchoPin)==0:  # Overwrite pulseStart until pulse is detected
			pulseStart=time.time()

		while GPIO.input(sonarEchoPin)==1:  # Overwrite pulseEnd until pulse has ended
			pulseEnd=time.time()

		try:

			pulseDuration=pulseEnd-pulseStart
            
			sonarDistance=(pulseDuration/2.0)*343

			if sonarDistance>4:	# Sensor not accurate for higher values
				sonarDistance=-1

			print "Sonar distance: %.2f [m]" % sonarDistance

		except:
            
			print GPIO.input(sonarEchoPin)
			print "Read value was not valid. Trying again"

except (KeyboardInterrupt,SystemExit):
    
	print "Keyboard interrupt catched. Closing"
	GPIO.cleanup()




