import serial
import os
from time import sleep
from numpy import array, linspace

#connect to Arduino
devdir = (os.walk('/dev/').next())[2]

for device in devdir:
	if device.find('ACM') != -1:
		print device
		ser = serial.Serial('/dev/' + device, 50, timeout = 1);
		print "Success!"
maxpos = array( (1030, 730) )
currpos = array( (0,0) )

def moveto( r , time_wait=0, utime_wait = 0):
	global currpos
	r = array(r)
	delta = r - currpos
	currpos = array((min(r[0],maxpos[0]), min(r[1],maxpos[1])))
	if delta[0] < 0:
		for dummy in xrange( int(abs(delta[1])) ):
			if delta[1] > 0:
				ser.write('MY1\n')
			elif delta[1] < 0:
				ser.write('MY0\n')
			sleep(utime_wait/1000000.)
			ser.flushInput()
		for dummy in xrange( int(abs(delta[0])) ):
			if delta[0] > 0:
				ser.write('MX1\n')
			elif delta[0] < 0:
				ser.write('MX0\n')
			sleep(utime_wait/1000000.)
			ser.flushInput()
	else:
		for dummy in xrange( int(abs(delta[0])) ):
			if delta[0] > 0:
				ser.write('MX1\n')
			elif delta[0] < 0:
				ser.write('MX0\n')
			sleep(utime_wait/1000000.)
			ser.flushInput()
		for dummy in xrange( int(abs(delta[1])) ):
			if delta[1] > 0:
				ser.write('MY1\n')
			elif delta[1] < 0:
				ser.write('MY0\n')
			sleep(utime_wait/1000000.)
			ser.flushInput()
	sleep(time_wait/1000.)


def push(time_wait=0):
	ser.write('P')
	sleep(time_wait/1000.)
def press(time_wait=0):
	ser.write('P')
	sleep(time_wait/1000.)
def release(time_wait=0):
	ser.write('R')
	sleep(time_wait/1000.)

def home():
	release()
	for x in xrange(50):
		ser.write('MX1\n')
		ser.flush()
		ser.flushInput()
	for x in xrange(800):
		ser.write('MY0\n')
		ser.flush()
		ser.flushInput()
		# sleep(1/10000.)
	for x in xrange(1100):
		ser.write('MX0\n')
		ser.flush()
		print ser.read()
		ser.flushInput()
		# sleep(1/10000.)
		
	currpos[0] = 0
	currpos[1] = 0

def close():
	ser.close()

def savepower():
	ser.write('S')
	ser.flushInput()