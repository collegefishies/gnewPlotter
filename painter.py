import sys
from printer import *
import numpy as np
from numpy import cos, sin,dot
from numpy import array, linspace
from scipy import misc
from time import sleep
import matplotlib.pyplot as plt
from PIL import Image
import time

current_milli_time = lambda: int(round(time.time() * 1000))
last_color = 0
#parameters
N = 15 #scanning radius
offset = array( (40,0) )
dipradius = 15 #(1/4 mm)
dipposition = [	array((0	,47)),
               	array((0	,135)),
               	array((0	,223)),
               	array((0	,311))
               	]
watertray = (510, 700)
length_til_dip = 50
diptime = 30000

hold_push = 500 #ms
hold_press = hold_push 
hold_release = 400 #ms

step_delay = 0


pressed_ = False

def comp(A,B):
	return A == B
def clear(A):
	return not A
def setImage(M):
	global D
	D = M
def clean(r,n=4,drytime=500):
	moveto( (70, r[1]))
	moveto( (0, (watertray[0] + watertray[1])/2))
	press()
	for dummy in range(n):
		moveto( (25, watertray[0]) )
		moveto( (25, watertray[1]) )
	release()
	sleep(drytime/1000.)
	moveto( (70, watertray[1]))
	moveto( r )
def dip(r,dip):
	global pressed_, dipposition,last_color
	if last_color != dip:
		clean(r,n=10)
		last_color = dip
	moveto( dipposition[dip] + offset+offset)
	moveto( dipposition[dip])
	press(hold_push)
	release(hold_push);
	moveto( dipposition[dip] + offset)
	moveto(r)
def drawBorder():
	global D, offset
	home()
	press(300)
	moveto(D.shape + offset)
	moveto((0,0) + offset)
	release()

def gotonextpoint(r, o,color):
	global length_til_dip, diptime, hold_press,hold_push,hold_release
	global pressed_, D, pixc
	global D, N
	global pixc
	global left_spot,last_time
	r = array(r)
	o = array(o)
	if comp(D[r[0], r[1]], 0):
		D[r[0], r[1]] = clear(D[r[0],r[1]])
		if current_milli_time() - last_time > diptime:
			if color != -1:
				release(hold_release)
				dip(r+o, color)
			last_time = current_milli_time()

		moveto( array((r[1],r[0])) + o,utime_wait=step_delay)
		if not pressed_:
			press(hold_push)
			pressed_ = True
		if pressed_:
			press()
		#check adjacent pixels.
		for dy in xrange(0,2*N+1):
			for dx in xrange(-dy,dy):
				try:
					if comp(D[ r[0]+dx, r[1] + (-1)**dy*dy/2],0):
						gotonextpoint( (r[0] + dx, r[1]+(-1)**dy*dy/2), o, color)
						return
				except:
					pass
	return

def drawImage(color):
	global D, currpos, pressed_,left_spot,last_time,last_color
	sys.setrecursionlimit(10000000)
	dim = D.shape
	home()
	if color != -1:
		dip( currpos, color)
	last_time = current_milli_time()
	left_spot = currpos
	# while D.any():
	for j in xrange(dim[1]):
		for i in xrange(dim[0]):
			gotonextpoint( (i,j), offset, color)
			if pressed_:
				release(hold_release)
				pressed_ = False
	# savepower()

