from sonar import Sonar
from threads import thrd

import time
import matplotlib.pyplot as plt
import numpy as np

sonar1=Sonar(14,15)
sonar2=Sonar(17,18)

SONARINUSE=False	# True whenever a sonar is in use. Used to avoid interference between multiple sonars

plt.ion()	# Interactive mode on (updates plots automatically)
plt.figure()

while True:
	print ""
	print "Sonar 1: %s [m]	%s [m/s]" % (sonar1.measureDistance(), sonar1.measureVelocity())
	time.sleep(0.01)
	print "Sonar 2: %s [m]	%s [m/s]" % (sonar2.measureDistance(), sonar2.measureVelocity())

	time.sleep(1)


