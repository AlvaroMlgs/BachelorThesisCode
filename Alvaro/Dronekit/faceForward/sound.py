import time
import platform
from threads import thrd

OS=platform.system()
if OS=="Windows":
	import winsound
	Beep=winsound.Beep
elif OS=="Linux":
	import os
	def Beep(freq,duration):
		os.system('beep -f %s -l %s' % (freq,duration))

def beep(freq,duration):
	makeBeep=thrd(Beep,freq,duration)
	makeBeep.name="makeBeep"
	makeBeep.start()

def doubleBeep(freq1,duration1,freq2,duration2,pause=0):
	def twoBeeps(freq1,duration1,freq2,duration2,pause=0):
		Beep(freq1,duration1)
		time.sleep(pause/1000)
		Beep(freq2,duration2)
	makeTwoBeeps=thrd(twoBeeps,freq1,duration1,freq2,duration2,pause)
	makeTwoBeeps.name="makeTwoBeeps"
	makeTwoBeeps.start()
	
def tripleBeep(freq1,duration1,freq2,duration2,freq3,duration3,pause1=0,pause2=0):
	def threeBeeps(freq1,duration1,freq2,duration2,freq3,duration3,pause1=0,pause2=0):
		Beep(freq1,duration1)
		time.sleep(pause1/1000)
		Beep(freq2,duration2)
		time.sleep(pause2/1000)
		Beep(freq3,duration3)
	makeThreeBeeps=thrd(threeBeeps,freq1,duration1,freq2,duration2,freq3,duration3,pause1,pause2)
	makeThreeBeeps.name="makeThreeBeeps"
	makeThreeBeeps.start()






