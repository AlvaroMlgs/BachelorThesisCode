from sonar import Sonar
from threads import thrd

import time

sonar1=Sonar(2,3)
sonar2=Sonar(14,15)
sonar3=Sonar(17,18)

while True:
	print ""
	time.sleep(0.02)	# Avoids echo noise and runtime errors
	print "Sonar 1: %s [m]	%s [m/s]" % (sonar1.measureDistance(), sonar1.computeVelocity())
	#time.sleep(0.02)	# Avoids echo noise and runtime errors
	print "Sonar 2: %s [m]	%s [m/s]" % (sonar2.measureDistance(), sonar2.computeVelocity())
	#time.sleep(0.02)	# Avoids echo noise and runtime errors
	print "Sonar 3: %s [m]	%s [m/s]" % (sonar3.measureDistance(), sonar3.computeVelocity())
	#time.sleep(0.02)	# Avoids echo noise and runtime errors

	time.sleep(0.5)


