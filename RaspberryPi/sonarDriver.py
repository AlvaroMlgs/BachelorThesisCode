from sonar import Sonar
from threads import thrd

import time

sonar1=Sonar(14,15)
sonar2=Sonar(17,18)

print "Measuring..."
while True:
	print ""
	print sonar1.measureDistance()
	print sonar1.measureVelocity()
	time.sleep(1)


