# -*- coding: iso-8859-1 -*-
# (c) 2010 Martin Wendt; see http://nxturtle.googlecode.com/
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

"""
Implementation of a Python turtle for LEGO Mindstorms NXT

NXTurtle is a mashup of the Python `Turtle graphics for TK` module 
(http://docs.python.org/library/turtle.html) and the LEGO Mindstorms driver 
NXT-Python (http://nxt-python.googlecode.com/). 

See http://nxturtle.googlecode.com/ for details.

@author: Martin Wendt
"""
import math
import time
import nxt.locator
#from nxt.sensor import PORT_1, PORT_2, PORT_3
#from nxt.sensor import Touch, Sound, Light, Ultrasonic, Color20
from nxt.brick import FileFinder, ModuleFinder, FileReader
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C, SynchronizedMotors
import sys
import traceback
from pprint import pprint
from turtle import Turtle, Vec2D
from version import __version__

#===============================================================================
# Helpers
#===============================================================================
# Convert radians to degree
_RTOD = 180.0 / math.pi
 
# Diameter of a standard LEGO wheel in centimeters
_TURTLE_WHEEL_DIAMETER = 4.4

# Axis length of our Turtle in centimeters 
# (distance between the two wheels, measured from middle to middle)
# This value is typically different for your very special Turtle :-)
_TURTLE_AXIS_LENGTH = 12.5

# Turn angles smaller than this will be ignored
_EPS_DEGREE = 1.0

# Movement distances smaller than this will be ignored [cm]
_EPS_UNITS = 1.0

def _default_pen_handler(turtle, down): 
    """Default dummy implementation of a pen handler."""
    turtle.debug("turtle._pen_handler(%s): NOT IMPLEMENTED. Call turtle.set_pen_handler()" % down)
    return

def normAngle(degree):
    """Return degree clamped to [-360..+360]."""
    a = math.fmod(degree, 360)
    if math.fabs(a) < _EPS_DEGREE:
        return 0
    return a

def shortAngle(degree):
    """Return degree normalized to [-180..+180] using the shortest turn."""
    a = math.fmod(degree, 360)
    if math.fabs(a) < _EPS_DEGREE:
        a = 0
    elif a > 180:
        a = a - 360
    elif a < -180:
        a = a + 360 
    return a

def lazyAngle(degree):
    """Return a tuple (degree normalized to [-90..+90], direction factor).
    
    Example: if degree is 100°, the result will (-80°, -1), becaus it is faster
    to turn right by 10° and then drive backwards.
    """
    a = shortAngle(degree)
    revert = 1
    if a > 90:
        a -= 180
        revert = -1
    elif a < -90:
        a += 180
        revert = -1
    if math.fabs(a) < _EPS_DEGREE:
        a = 0
    return (a, revert)

#===============================================================================
# NXTurtle
#===============================================================================
class NXTurtle(Turtle):
    """Turtle graphics for LEGO Mindstorms NXT.
    
    This class is derived from Turtle graphics for Tk 
    (http://docs.python.org/library/turtle.html)
    """
    DEFAULT_CONFIG = {
        # Motor turn angle in degree, that will turn the turtle by one degree left  
        "tachoPerDegree": _TURTLE_AXIS_LENGTH / _TURTLE_WHEEL_DIAMETER,
        # Motor turn angle in degree, that will move the turtle by one unit  
        "tachoPerUnit": 360.0 / (_TURTLE_WHEEL_DIAMETER * math.pi),
        # This power will be applied to the motor for turning 
        "turnPower": 75,
        # This power will be applied to the motor for moving 
        "drivePower": 75,
        }  
    
    def __init__(self, connect=True):

        super(NXTurtle, self).__init__()
        
        self.brick = None
        self.leftMotor = None 
        self.rightMotor = None
        self.penMotor = None
        
        self.verbose = 2
        self._lazy = False
        self._autoRaisePen = True
        self._autoHome = False

        self._brickHeading = 0
        self._brickCoords = Vec2D(0, 0)
        self._brickDown = False

        self._pen_handler = _default_pen_handler
        
        self.config = self.DEFAULT_CONFIG.copy()
        if connect:
            self.connect()

    def __del__(self):
        print "__del__"
        self.disconnect()
        super(NXTurtle, self).__del__()

    def __str__(self):
        if self._brickDown:
            d = "down"
        else:
            d = "up"
        s =  "NXTurtle<%s %.1f° %s>" % (self._brickCoords, self._brickHeading, d)
        if abs(self._brickCoords - self.pos()) > _EPS_UNITS:
            s += ", Internal pos: %s" % str(self.pos())
        if math.fabs(self._brickHeading - self.heading()) > _EPS_DEGREE:
            s += ", Internal heading: %s°" % self.heading()
        if not self.brick:
            s += " !! NOT CONNECTED"
        return s
    
    def debug(self, msg):
        if self.verbose >= 2:
            print "%0.3f" % time.clock(), msg
        
    def log(self, msg):
        if self.verbose >= 1:
            print "%0.3f" % time.clock(), msg
        
    def connect(self):
        """Connect NXTurtle with LEGO NXT brick."""
        self.debug("Connecting...")
        self.disconnect()
        self.brick = nxt.locator.find_one_brick()
        self.leftMotor = Motor(self.brick, PORT_B)
        self.rightMotor = Motor(self.brick, PORT_C)
        self.penMotor = Motor(self.brick, PORT_A)
        self.log("Connected to %s." % self.brick)
        if self.verbose >= 2:
            pprint(self.get_brick_info())
        
    def disconnect(self):
        """Close connection and restore defined status.
        
        Should be called at the end of a program, because turtle's destructor
        is not reliably called by Python. 
        """
        if self.brick:
            if self._autoRaisePen:
                self.penup()
            if self._autoHome:
                self.home()
            self.debug("Disconnecting...")
            self.leftMotor = self.rightMotor = self.penMotor = None
            self.brick = None
            self.log("Disconnected.")
        # Brick is disconnected in its destructor
        self.brick = None
        
    def _drive(self, units):
        """Run motors B and C to advance turtle by a number of units.
        
        A negative value will go backwards.
        turtle.set_tacho_units_per_unit() should have been called before for
        calibration.
        """
        if not self.brick:
            return
        syncedMotor = SynchronizedMotors(self.leftMotor, self.rightMotor, 
                                         turn_ratio=0)
        syncedMotor.debug = (self.verbose >= 3)
        tacho_units = units * self.config["tachoPerUnit"]
        if math.fabs(tacho_units) < _EPS_DEGREE:
            self.log("NXTurtle._drive(%f) -> turn wheel by %f°) ignored" % (units, tacho_units))
            return True
        power = self.config["drivePower"]
        if units < 0:
            syncedMotor.turn(-power, tacho_units=-tacho_units)
        else:
            syncedMotor.turn(power, tacho_units=tacho_units)
        self._brickCoords += units * Vec2D(1, 0).rotate(self._brickHeading)
        self.debug("NXTurtle._drive(%s) -> %s" % (units, str(self)))
        
    def _turn(self, degree, radius=0):
        """Turn turtle left (counterclockwise) by degree.
        
        A negative degree value will turn right (clockwise).
        Run motors B and C to turn turtle by degree around it's z-axis.
        turtle.set_tacho_units_per_degree() should have been called before for
        calibration.
        """
        if radius != 0:
            raise NotImplementedError
        if not self.brick:
            return
        if math.fabs(degree) < _EPS_DEGREE:
            self.log("NXTurtle._turn(%f°) ignored" % degree)
            return True

        tacho_units = degree * self.config["tachoPerDegree"]
        
        # Use turn_ration=100; swap motors for left turns
        if tacho_units < 0:
            b, a = self.leftMotor, self.rightMotor 
            tacho_units *= -1
        else:
            a, b = self.leftMotor, self.rightMotor 
        syncedMotor = SynchronizedMotors(a, b, turn_ratio=100)
        syncedMotor.debug = (self.verbose >= 3)
        syncedMotor.turn(power=self.config["turnPower"], tacho_units=tacho_units)
        self._brickHeading += degree
        self.debug("NXTurtle._turn(%s°, %s) -> %s" % (degree, radius, str(self)))
        
    def set_tacho_units_per_degree(self, tacho_units):
        """Number of degrees that the wheel motors have to spin (in opposite
        direction), in order to turn Turtle by 1°.
        
        This value may be found by experimentation, or calculated as 
            AXIS_LENGTH / WHEEL_DIAMETER.
        @see: http://code.google.com/p/nxturtle/wiki/ConstructAndCalibrate
        """
        self.config["tachoPerDegree"] = tacho_units
        return
    
    def set_tacho_units_per_unit(self, tacho_units):
        """Number of degrees that the wheel motors have to spin, in order to 
        move Turtle by 1 unit.
        
        This value may be found by experimentation, or calculated as 
            360.0 / (WHEEL_DIAMETER * math.pi)
        @see: http://code.google.com/p/nxturtle/wiki/ConstructAndCalibrate
        """
        self.config["tachoPerUnit"] = tacho_units
        return
    
    def set_lazy_mode(self, on):
        """Allow to go backwards, if this results in shorter turn angles.
        
        This only applies go goto(), home() or reset(). In this case our turtle
        may choose to move backwards, so it has  only to turn max. 90°.
        @return: the previous lazy mode
        """
        prev = self._lazy
        self._lazy = on
        return prev
    
    def set_pen_handler(self, func):
        """Define a callback function that raises or lowers the pen.
        
        The function must be defined like
        
            def pen_handler(turtle, down):
                ...
        
        It may use `turtle.penMotor` to perform this. 
        @see: http://code.google.com/p/nxturtle/wiki/ConstructAndCalibrate
        """
        self._pen_handler = func
        return
    
    def get_brick_info(self):
        """Return a dictionary with brich information."""
        try:
            b = self.brick
            name, host, signal_strength, user_flash = b.get_device_info()
            prot_version, fw_version = b.get_firmware_version()
            millivolts = b.get_battery_level()
            return {"status": "ok",
                    "NXT brick name": name.rstrip(chr(0)),
                    "Host address": host,
                    "Bluetooth signal strength": signal_strength,
                    "Free user flash": user_flash,
                    "Protocol version": "%s.%s" % prot_version,
                    "Firmware version": "%s.%s" % fw_version,
                    "Battery level": "%s mV" % millivolts,
                    }
        except Exception, e:
            print "Error with brick:"
            traceback.print_tb(sys.exc_info()[2])
            print str(sys.exc_info()[1])
            return {"status": "error", 
                    "details": str(e)}
        
    def play_tone(self, frequency, duration, wait=True):
        """Play a tone at frequency (Hz) for duration (ms)"""
        self.brick.play_tone(frequency, duration)
        if wait:
            time.sleep(duration / 1000.0)

    def play_sound_file(self, fname, loop=False):
        """Play a sound file. 
        
        If loop=True, it will be repeated until stop_sound_file() is called.
        """
        if not "." in fname:
            fname += ".rso"
        self.brick.play_sound_file(loop, fname)
    
    def stop_sound_file(self):
        self.brick.stop_sound_playback()
    
#    def show_image_file(self, fname):
#        raise NotImplementedError
    
    def start_program(self, fname):
        self.brick.start_program(fname)
    
    def stop_program(self):
        self.brick.stop_program()
    
    def set_name(self, name):
        """Set brick name (truncated to 15 characters)."""
        return self.brick.set_brick_name(name)
    
    def get_name(self):
        """Return the brick name."""
        return self.get_brick_info().get("NXT brick name")
    
#    def reboot(self):
#        """Return the brick name."""
#        return self.brick.boot()
    
    def wait(self, duration):
        """Sleep for `duration` milliseconds."""
        time.sleep(duration / 1000.0)

    def find_files(self, pattern="*.*"):
        """Return all matching files as (name, size) tuples.
        
        Extension patterns:
        *.rdt:         Data files
        *.rxe, *.rtm   Executable files and try-me programs
        *.ric          Icon files
        *.rms          Hidden menu files
        *.rpg          Program files
        *.rso          Sound files
        *.sys          Hidden files
        *.tmp          Temporary hidden files
        """
        ff = FileFinder(self.brick, pattern)
        for f in ff:
            yield f

    def get_file(self, name):
        """Return files as (name, size) tuples."""
        for name, _size in self.find_files(name):
            return FileReader(self.brick, name)
        return None

    def find_modules(self, pattern="*.*"):
        """Return all matching modlues as (mname, mid, msize, miomap_size) tuples."""
        mf = ModuleFinder(self.brick, pattern)
        for m in mf:
            yield m

    def _set_pen(self, down):
        """Run motor A to move pen down or up."""
        if not self.brick:
            return self._brickDown
        if self._brickDown == down:
            self.debug("NXTurtle._set_pen(%s) -> ignored" % down)
            return self._brickDown
        self._pen_handler(self, down)
        self._brickDown = down
        self.debug("NXTurtle._set_pen(%s) -> %s" % (down, str(self)))

    def pendown(self):
        super(NXTurtle, self).pendown()
        self._set_pen(True)
        
    def penup(self):
        super(NXTurtle, self).penup()
        self._set_pen(False)
        
    def home(self):
        """Reset turtle to its initial values."""
        ofs =  - self._brickCoords
        headingToDest = math.atan2(ofs[1], ofs[0]) * _RTOD
        alpha = headingToDest - self._brickHeading
        # Turn max +/- 90° and go backwards, if that is faster
        alpha, revert = lazyAngle(alpha)
        self._turn(alpha)
        self._drive(revert * abs(ofs))
        # Turn to 0°
        self._turn(shortAngle(-self._brickHeading))
        self.debug("NXTurtle.home() -> %s" % str(self))

    def _go(self, distance):
        """Move turtle forward by specified distance."""
        # Called by forward, back
        # The default implementation calls _goto() which calls _drive()
        # Since backward moves don't change heading, we force lazy mode:
        prev = self.set_lazy_mode(distance < 0)
        super(NXTurtle, self)._go(distance)
        self.set_lazy_mode(prev)

    def _rotate(self, angle):
        """Turn turtle counterclockwise by specified angle if angle > 0."""
        super(NXTurtle, self)._rotate(angle)
        self._turn(angle)

    def _goto(self, end):
        """Move turtle to position end.
        
        This is called by 
        - turtle.goto(x, y):
          does not change current heading, so our Turtle must restore it
        - turtle.forward(d) -> _go(d)
          this should keep the heading
        - turtle.back(d) -> _go(-d)
          this should keep the heading, so we have to go reverse (i.e. 'lazy' mode)
        """
        ofs = end - self._brickCoords
        super(NXTurtle, self)._goto(end)
        # NXTurtle can't jump, so it has to turn - drive - turn
        if abs(ofs) < _EPS_UNITS:
            return
        headingToDest = math.atan2(ofs[1], ofs[0]) * _RTOD
        alpha = headingToDest - self._brickHeading
        if self._lazy:
            # Turn max +/- 90° and go backwards, if that is faster
            alpha, revert = lazyAngle(alpha)
            self._turn(alpha)
            self._drive(revert * abs(ofs))
        else:
            # Turn +/- 180°, always go forward
            alpha = shortAngle(alpha)
            self._turn(alpha)
            self._drive(abs(ofs))
        # Restore previous heading, so we stay in sync with base Turtle
        self._turn(-alpha)
        self.debug("NXTurtle._goto(%s) -> %s" % (end, str(self)))

    def circle(self, radius, extent = None, steps = None):
        """ Draw a circle with given radius.

        Arguments:
        radius -- a number
        extent (optional) -- a number
        steps (optional) -- an integer

        Draw a circle with given radius. The center is radius units left
        of the turtle; extent - an angle - determines which part of the
        circle is drawn. If extent is not given, draw the entire circle.
        If extent is not a full circle, one endpoint of the arc is the
        current pen position. Draw the arc in counterclockwise direction
        if radius is positive, otherwise in clockwise direction. Finally
        the direction of the turtle is changed by the amount of extent.

        As the circle is approximated by an inscribed regular polygon,
        steps determines the number of steps to use. If not given,
        it will be calculated automatically. Maybe used to draw regular
        polygons.

        call: circle(radius)                  # full circle
        --or: circle(radius, extent)          # arc
        --or: circle(radius, extent, steps)
        --or: circle(radius, steps=6)         # 6-sided polygon

        Example (for a Turtle instance named turtle):
        >>> turtle.circle(50)
        >>> turtle.circle(120, 180)  # semicircle
        """
        
        super(NXTurtle, self).circle(radius, extent, steps)
        self.debug("NXTurtle.circle(%s, %s, %s) -> %s" % (radius, extent, steps, str(self)))
        
## three dummy methods to be implemented by child class:

    def speed(self, s=0):
        """dummy method - to be overwritten by child class"""
        self.debug("speed(%s)" % s)
        super(NXTurtle, self).speed(s)
    def tracer(self, a=None, b=None):
        """dummy method - to be overwritten by child class"""
        self.debug("tracer(%s, %s)" % (a, b))
        super(NXTurtle, self).tracer(a, b)
    def _delay(self, n=None):
        """dummy method - to be overwritten by child class"""
        self.debug("_delay(%s)" % n)
        super(NXTurtle, self)._delay(n)


#===============================================================================
# 
#===============================================================================
def test():
    pass
    ### Create the turtle and connect to LEGO NXT brick
    print "NXTurtle %s" % __version__
    connect = True
#    connect = False
    t = NXTurtle(connect=connect)

    ### Calibrate
    AXIS_LENGTH = 12.5
    WHEEL_DIAMETER = 4.4

    tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER 
    t.set_tacho_units_per_degree(tachoPerDegree)

    tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)
    t.set_tacho_units_per_unit(tachoPerUnit)

    def pen_handler(turtle, on):
        power = 50
        tacho_units = 60
        if on:
            power *= -1
        turtle.penMotor.turn(power, tacho_units)

    t.set_pen_handler(pen_handler)

    ### Print some infos
#    t._autoHome = True
    print "mode", t.screen.mode()
    print "heading", t.heading()
    print "_orient", t._orient
    t.speed(1)
    # --------------------------------------------------------------------------
    t.verbose = 1
    t.fd(10)
    t.rt(90)
    t.fd(10)
    t.rt(90)
    t.fd(10)
    t.verbose = 2

    t.home()
    # --------------------------------------------------------------------------
    t.disconnect()
    return 

    t.play_tone_and_wait(440, 200)
    
#    b = t.brick
#    print "Touch:", Touch(b, PORT_1).get_sample()
#    print "Sound:", Sound(b, PORT_2).get_sample()
#    print "Light:", Light(b, PORT_3).get_sample()
#    print "Light:", Color20(b, PORT_3).get_sample()
#    print "Ultrasonic:", Ultrasonic(b, PORT_4).get_sample()
    
#    for name, size in t.find_files("*.rso"):
#        print "sound file", name.rstrip(chr(0)), size
#
#    for mname, mid, msize, miomap_size in t.find_modules():
#        print "module", mname, mid, msize, miomap_size
    
#    f = t.get_file("Unbenannt-1.rxe").read()
#    print "%r" % f
    
#    t._drive(5)
    t._turn(90)

#    t.leftMotor.turn(100, 60)
#    t.rightMotor.turn(-100, 60)
#    t.syncedMotor.turn(100, 45)

#    t.syncedMotor.turn(100, -45)
#    syncedMotor = SynchronizedMotors(t.leftMotor, t.rightMotor, turn_ratio=0)
#    syncedMotor.turn(100, 180)

if __name__ == "__main__":
    test()
