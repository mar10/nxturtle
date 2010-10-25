# -*- coding: iso-8859-1 -*-
# (c) 2010 Martin Wendt; see http://nxturtle.googlecode.com/
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""Sample for NXTurtle using some brick functions

These are functions that a simple Logo turtle can't do.
"""

from nxturtle import NXTurtle
import math
from nxt.sensor import Ultrasonic
from nxt.sensor.common import PORT_4

### Create the turtle and connect to LEGO NXT brick
turtle = NXTurtle(connect=True)

### Calibrate
AXIS_LENGTH = 12.5
WHEEL_DIAMETER = 4.4

tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)
correction = 1.00 
turtle.set_tacho_units_per_unit(correction * tachoPerUnit)

tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER
correction = 0.90 
turtle.set_tacho_units_per_degree(correction * tachoPerDegree)

# This function is passed to our turtle. It will be called whenever the pen 
# should be raised or put down. 
def pen_handler(turtle, on):
    power = 50
    tacho_units = 150
    if on:
        power *= -1
    turtle.penMotor.turn(power, tacho_units)

turtle.set_pen_handler(pen_handler)

# Attach sensor
turtle.eyes = Ultrasonic(turtle.brick, PORT_4)

# Read  sensor data
print "I can see for %s miles..." % turtle.eyes.get_distance()

### Access name and other info

turtle.set_name("Yertle")
print "Hello, my name is '%s'" % turtle.get_name()

print "Info: "
print turtle.get_brick_info()

### Sounds

# Play 'a' note for half a second
turtle.play_tone(440, 500)

print "I know these sounds:"
for name in turtle.find_files("*.rso"):
    print "sound", name

# Play a sound file ('rso' extension is added by default)
turtle.play_sound_file("Goodmorning")
# starting a sound will stop the previous, so we wait a little
turtle.wait(1000)
turtle.play_sound_file("Alarm.rso")

### Programs
print "I know these programs:"
for name in turtle.find_files("*.rxe"):
    print "program", name
#
#turtle.start_program("Turtle1.rxe")


# Wait for 2 seconds
turtle.wait(2000)
### Close connection (will also raise the pen)
turtle.disconnect()
