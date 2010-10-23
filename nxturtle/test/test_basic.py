# -*- coding: iso-8859-1 -*-
# (c) 2010 Martin Wendt; see http://nxturtle.googlecode.com/
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""Unit tests for wsgidav.util"""

import unittest
from nxturtle import NXTurtle
import math

class BasicTest(unittest.TestCase):                          
    """Test ."""

            
    def setUp(self):
        ### Create the turtle and connect to LEGO NXT brick
        self.turtle = NXTurtle(connect=True)
        t = self.turtle
    
        ### Calibrate
        AXIS_LENGTH = 12.5
        WHEEL_DIAMETER = 4.4
    
        tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER
        correction = 0.90 
        t.set_tacho_units_per_degree(correction * tachoPerDegree)
    
        tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)
        correction = 1.00 
        t.set_tacho_units_per_unit(correction * tachoPerUnit)
    
        def pen_handler(turtle, on):
            power = 50
            tacho_units = 150
            if on:
                power *= -1
            turtle.penMotor.turn(power, tacho_units)
    
        t.set_pen_handler(pen_handler)
    

    def tearDown(self):
        t = self.turtle
        t.penup()
        t.home()
        t.disconnect()
        self.turtle = None
        

    def testBasics(self):                          
        """Test basic tool functions."""
        t = self.turtle
        ### Print some infos
    #    t._autoHome = True
        assert t.screen.mode() == "standard"
        self.assertEqual(t.heading(), 0)
        self.assertEqual(t._orient, (1, 0))
        
        t.speed(1)
    #    print "\nfd(5)"
    #    t.fd(5)
    #    print "\nsetheading(90)"
    #    t.setheading(90)
    #    print "\nreset()"
    #    t.reset()
    
    #    t.fd(10)
    #    t.left(90)
    #    t.fd(10)
    #    t.home()
        
        ### Go an try it
        t.play_tone(440, 500) 
        t.pendown()
        t.fd(10)
        self.assertEqual(t.pos(), (10, 0))


if __name__ == "__main__":
    unittest.main()   
#    suite = suite()
#    TextTestRunner(descriptions=0, verbosity=2).run(suite)
