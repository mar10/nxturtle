# -*- coding: iso-8859-1 -*-
# (c) 2010 Martin Wendt; see http://nxturtle.googlecode.com/
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""Unit tests for wsgidav.util"""

from nxturtle import NXTurtle
import math

def test():
    ### Create the turtle and connect to LEGO NXT brick
    turtle = NXTurtle(connect=True)
    t = turtle

    ### Calibrate
    AXIS_LENGTH = 12.5
    WHEEL_DIAMETER = 4.4

    tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER 
    corr = 0.90
    t.set_tacho_units_per_degree(corr * tachoPerDegree)

    tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)
    t.set_tacho_units_per_unit(tachoPerUnit)

    def pen_handler(turtle, on):
        power = 50
        tacho_units = 150
        if on:
            power *= -1
        turtle.penMotor.turn(power, tacho_units)

    t.set_pen_handler(pen_handler)


        
    # --------------------------------------------------------------------------
#    t.pendown()
#    
#    t.fd(25)
#    t.lt(90)
#    t.fd(25)
#    t.lt(90)
#    t.fd(25)
#    t.lt(90)
#    t.fd(25)
#    t.lt(135)
#    t.fd(18)

    t.wait(5000)
    # --------------------------------------------------------------------------
    t.disconnect()
    turtle = None


if __name__ == "__main__":
    test()
