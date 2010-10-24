# -*- coding: iso-8859-1 -*-
# (c) 2010 Martin Wendt; see http://nxturtle.googlecode.com/
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""Sample for NXTurtle drawing a square and move into the center."""

from nxturtle import NXTurtle
import math

### Create the turtle and connect to LEGO NXT brick
t = NXTurtle(connect=True)

### Calibrate
# All turtles are not created equal, so we have to define how many motor turns
# it takes to move it by one unit, or turn it by one degree.
# Here we do this by a combination of calculation and empirical information ;-)
#
# We assume this preconditions:
# - The left wheel is expected to be connected to motor B.
# - The right wheel is at motor C.
# - Motor A is used to control the pen.
# -  

# Distance between left and right wheel in [cm] (measured from middle of treads)
AXIS_LENGTH = 12.5
# Wheel diameter in [cm]
WHEEL_DIAMETER = 4.4

# Now we can calculate the number of wheel turns it takes, to move the turtle 
# by one unit (i.e. one centimeter) 
tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)
correction = 1.00 
t.set_tacho_units_per_unit(correction * tachoPerUnit)

# It should also be possible to calculate the number of wheel turns it takes, 
# to turn the turtle by one degree 
tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER
# ... observation shows that either Archimedes was wrong, or our turtle is not 
# perfect. Anyway this correction factor will improve the results: 
correction = 0.90 
t.set_tacho_units_per_degree(correction * tachoPerDegree)

# This function is passed to our turtle. It will be called whenever the pen 
# should be raised or put down. 
def pen_handler(turtle, on):
    power = 50
    tacho_units = 150
    if on:
        power *= -1
    turtle.penMotor.turn(power, tacho_units)

t.set_pen_handler(pen_handler)


### Go an try it
t.pendown()
t.forward(10)
t.right(90)
t.forward(10)
t.penup()

t.home()

t.play_tone(440, 500) 

### Close connection
t.disconnect()
