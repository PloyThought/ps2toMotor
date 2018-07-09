#!/usr/bin/env python

import pygame
import time
import RPi.GPIO as GPIO

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

print(chr(27) + "[2J")
print 'Initialized Joystick : %s' % j.get_name()

# Setup the various GPIO values, using the BCM numbers for now

Q1 = 38
Q2 = 40
Q3 = 31
Q4 = 29
Q5 = 36
Q6 = 32
Q7 = 37
Q8 = 35

ControlPin = [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8]
print "Following BCM address to be used "
print ControlPin

#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

for pin in ControlPin:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)

seq = [ [0,0,0,1,0,0,1,0],
                [0,1,0,1,1,0,1,0],
                [0,1,0,0,1,0,0,0],
                [0,1,1,0,1,0,0,1],
                [0,0,1,0,0,0,0,1],
                [1,0,1,0,0,1,0,1],
                [1,0,0,0,0,1,0,0],
                [1,0,0,1,0,1,1,0]]

# Only start the motors when the inputs go above the following threshold
threshold = 0.60
UpdateMotors = False

myAxis3Last = 0
myAxis4Last = 0
myAxis3 = 0
myAxis4 = 0
stepSeqPos = 0
myStr = ""
currStep = 0

# Configure the motors to match the current settings.
def setmotors(CurrPos, LastPos):
        diff = (CurrPos - LastPos)
	#diff = diff + (diff/abs(diff))
	print(chr(27) + "[2J")
	print "LastPos:	" + str(LastPos)
	print "CurrPos:	" + str(CurrPos)
	print "diff:		" + str(diff) + "\n"
        for halfstep in range(int(abs(diff))): #range(int(abs(diff)))[::int(diff/abs(diff))]:
                print "halfstep:	" + str(halfstep + 1)
		currStep = int((LastPos + ((halfstep + 1) * (diff/abs(diff)))))
		print "current step:	" + str(currStep)
		stepSeqPos = int((currStep % 8))
		print "stepSeqPos:	" + str(stepSeqPos)
		setpin(stepSeqPos)

def setpin(position):
	myStr = ""
	for pin in range(8):
		GPIO.output(ControlPin[pin], seq[position][pin])
		myStr = myStr + str(seq[int(position)][pin]) + " "
	print "Motor Seq:	[" + myStr + "]"

# Try and run the main code, and in case of failure we can stop the motors
try:
	# Turn on the motors
	setpin(0)

	# This is the main loop
	while True:

        # Check for any queued events and then process each one
	        events = pygame.event.get()
        	for event in events:
        		UpdateMotors = 0

	        	# Check if one of the joysticks has moved
       			if event.type == pygame.JOYAXISMOTION:
        			if event.axis == 3:
					myAxis3 = round(10 * event.value)
					UpdateMotors = True
					#print "axis 3: " + str(event.value)
					#print "axis 3: " + str(myAxis3)
				if event.axis == 4:
					myAxis4 = round(10 * event.value)
					UpdateMotors = True
					#print "axis 4: " + str(event.value)
					#print "axis 4: " + str(myAxis4)

				# Move Up
				if (myAxis3 != myAxis3Last):
					setmotors(myAxis3, myAxis3Last)
					myAxis3Last = myAxis3
				# Move Right
				#if (myAxis4 != myAxis4Last):
					#setmotors(myAxis4, myAxis4Last)
					#myAxis4Last = myAxis4

except KeyboardInterrupt:
	# Turn off the motors
	for pin in ControlPin:
		GPIO.setup(pin,GPIO.OUT)
                GPIO.output(pin,0)
	GPIO.cleanup()

	j.quit()
