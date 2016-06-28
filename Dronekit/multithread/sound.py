import winsound
import time
from threads import thrd

def beep(freq,duration):
	makeBeep=thrd(winsound.Beep,freq,duration)
	makeBeep.name="makeBeep"
	makeBeep.start()

def doubleBeep(freq1,duration1,freq2,duration2,pause=0):
	def twoBeeps(freq1,duration1,freq2,duration2,pause=0):
		winsound.Beep(freq1,duration1)
		time.sleep(pause/1000)
		winsound.Beep(freq2,duration2)
	makeTwoBeeps=thrd(twoBeeps,freq1,duration1,freq2,duration2,pause)
	makeTwoBeeps.name="makeTwoBeeps"
	makeTwoBeeps.start()
	
def tripleBeep(freq1,duration1,freq2,duration2,freq3,duration3,pause1=0,pause2=0):
	def threeBeeps(freq1,duration1,freq2,duration2,freq3,duration3,pause1=0,pause2=0):
		winsound.Beep(freq1,duration1)
		time.sleep(pause1/1000)
		winsound.Beep(freq2,duration2)
		time.sleep(pause2/1000)
		winsound.Beep(freq3,duration3)
	makeThreeBeeps=thrd(threeBeeps,freq1,duration1,freq2,duration2,freq3,duration3,pause1,pause2)
	makeThreeBeeps.name="makeThreeBeeps"
	makeThreeBeeps.start()
