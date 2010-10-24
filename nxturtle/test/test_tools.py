# -*- coding: iso-8859-1 -*-
# (c) 2010 Martin Wendt; see http://nxturtle.googlecode.com/
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
"""Unit tests for wsgidav.util"""

import unittest
from nxturtle import lazyAngle, shortAngle, normAngle

class ToolTest(unittest.TestCase):                          
    """Test ."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAngles(self):                          
        """Test angle tool functions."""
        # normAngle always +/- 360°
        self.assertEqual(normAngle(0), 0)
        self.assertEqual(normAngle(360), 0)
        self.assertEqual(normAngle(180), 180)
        self.assertEqual(normAngle(-180), -180)
        self.assertEqual(normAngle(270), 270)
        self.assertEqual(normAngle(-270), -270)
        self.assertEqual(normAngle(720), 0)
        self.assertEqual(normAngle(400), 40)
        self.assertEqual(normAngle(-400), -40)
        # shortAngle always +/- 180°
        self.assertEqual(shortAngle(0), 0)
        self.assertEqual(shortAngle(360), 0)
        self.assertEqual(shortAngle(170), 170)
        self.assertEqual(shortAngle(180), 180)
        self.assertEqual(shortAngle(190),-170)
        self.assertEqual(shortAngle(-170), -170)
        self.assertEqual(shortAngle(-180), -180)
        self.assertEqual(shortAngle(-190), +170)
        self.assertEqual(shortAngle(260), -100)
        self.assertEqual(shortAngle(270), -90)
        self.assertEqual(shortAngle(-270), 90)
        self.assertEqual(shortAngle(720), 0)
        self.assertEqual(shortAngle(400), 40)
        self.assertEqual(shortAngle(-400), -40)
        # lazyAngle +/- 90°
        self.assertEqual(lazyAngle(0), (0, False))
        
        self.assertEqual(lazyAngle( 80), (+80, False))
        self.assertEqual(lazyAngle( 90), (+90, False))
        self.assertEqual(lazyAngle(100), (-80, True))

        self.assertEqual(lazyAngle( -80), (-80, False))
        self.assertEqual(lazyAngle( -90), (-90, False))
        self.assertEqual(lazyAngle(-100), (+80, True))

        self.assertEqual(lazyAngle(260), (+80, True))
        self.assertEqual(lazyAngle(270), (-90, False))
        self.assertEqual(lazyAngle(280), (-80, False))
        
        self.assertEqual(lazyAngle(260), (+80, True))
        self.assertEqual(lazyAngle(270), (-90, False))
        self.assertEqual(lazyAngle(280), (-80, False))

        self.assertEqual(lazyAngle(180), (0, True))
        self.assertEqual(lazyAngle(-180), (0, True))
        self.assertEqual(lazyAngle(135), (-45, True))
        self.assertEqual(lazyAngle(-135), (45, True))

if __name__ == "__main__":
    unittest.main()   
#    suite = suite()
#    TextTestRunner(descriptions=0, verbosity=2).run(suite)
