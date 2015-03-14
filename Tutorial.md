

# Introduction #

NXTurtle is an _extension_ to the _Turtle graphics for Tk_ module that comes with Python. Therefore programming NXTurtle is very similar to programming the standard `turtle` module.

So, first you might want to read the [introduction to the turtle graphics module](http://docs.python.org/library/turtle.html).

Have you read it? Fine.

So you know how to use **common functions**, like

  * `turtle.forward()`, `turtle.back()`, `turtle.left()`, `turtle.right()`

There are some **differences** though:

  * Moving and turning commands are also sent to the connected LEGO brick
  * A LEGO brick can't jump, so `turtle.goto()`, `turtle.reset()`, etc. are automatically converted to turns and moves.
  * The turtle is probably not moving as precisely as we would hope, so don't expect perfect squares ;-)

These functions are **not** supported

  * `turtle.circle()` is not yet implemented.
  * Other drawing functions like `.stamp()`, `.pensize()`, `.color()`, `.fill()` , `.hideturtle()`, `.tilt()` are not available
  * Still working on the `turtle.clone()` function ;-)

But there is also some **additional functionality**:
<br>(Most of this just exposes functions that the NXT-Python brick driver provides.)<br>
<br>
<ul><li><code>turtle.play_tone(freq, ms)</code> plays a tone for the specified duration.<br>
</li><li><code>turtle.play_sound_file(fname)</code>
</li><li><code>turtle.set_name(name)</code>
</li><li><code>turtle.find_files(pattern)</code>
</li><li><code>turtle.wait(msec)</code>
</li><li><code>turtle.get_brick_info()</code>
</li><li><code>turtle.start_program(fname)</code>
</li><li>Plus everything that NXT-Python provides, using <code>turtle.brick.</code>,<br>for example <code>turtle.brick.get_firmware_version()</code>...</li></ul>

<h1>Examples</h1>

First, make sure that you have read the <a href='Installation.md'>installation instructions</a> and <a href='ConstructAndCalibrate.md'>build instructions</a>.<br>
<br>
<h2>Sample turtle drawing a square (sort of)</h2>

<pre><code>from nxturtle import NXTurtle<br>
import math<br>
<br>
### Create the turtle and connect to LEGO NXT brick<br>
turtle = NXTurtle(connect=True)<br>
<br>
### Calibrate<br>
# All turtles are not created equal, so we have to define how many motor turns<br>
# it takes to move it by one unit, or turn it by one degree.<br>
# Here we do this by a combination of calculation and empirical information ;-)<br>
#<br>
# We assume this preconditions:<br>
# - The left wheel is expected to be connected to motor B.<br>
# - The right wheel is at motor C.<br>
# - Motor A is used to control the pen.<br>
<br>
# Distance between left and right wheel in [cm] (measured from middle of treads)<br>
AXIS_LENGTH = 12.5<br>
# Wheel diameter in [cm]<br>
WHEEL_DIAMETER = 4.4<br>
<br>
# Now we can calculate the number of wheel turns it takes, to move the turtle <br>
# by one unit (i.e. one centimeter) <br>
tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)<br>
correction = 1.00 <br>
turtle.set_tacho_units_per_unit(correction * tachoPerUnit)<br>
<br>
# It should also be possible to calculate the number of wheel turns it takes, <br>
# to turn the turtle by one degree <br>
tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER<br>
# ... observation shows that Archimedes was wrong, or our turtle is not <br>
# perfect. Either way this correction factor will improve the results: <br>
correction = 0.90 <br>
turtle.set_tacho_units_per_degree(correction * tachoPerDegree)<br>
<br>
# This function is passed to our turtle. It will be called whenever the pen <br>
# should be raised or put down. <br>
def pen_handler(turtle, on):<br>
    power = 50<br>
    tacho_units = 150<br>
    if on:<br>
        power *= -1<br>
    turtle.penMotor.turn(power, tacho_units)<br>
<br>
turtle.set_pen_handler(pen_handler)<br>
<br>
<br>
### Go an try it<br>
# get set...<br>
turtle.pendown()<br>
# draw a square with 25 cm edge length<br>
turtle.fd(25)<br>
turtle.lt(90)<br>
turtle.fd(25)<br>
turtle.lt(90)<br>
turtle.fd(25)<br>
turtle.lt(90)<br>
turtle.fd(25)<br>
# walk to the center<br>
turtle.lt(135)<br>
turtle.fd(18)<br>
# wait for 5 seconds<br>
turtle.wait(5000)<br>
### Close connection (will also raise the pen)<br>
turtle.disconnect()<br>
</code></pre>

This is how it looks like in action<br>
<br>
<a href='http://www.youtube.com/watch?feature=player_embedded&v=5xIK6iFTDzM' target='_blank'><img src='http://img.youtube.com/vi/5xIK6iFTDzM/0.jpg' width='425' height=344 /></a><br>
<br>
<br>
<h2>Using brick commands</h2>

Here we are using some functions that separate NXTurtle from a plain <a href='http://en.wikipedia.org/wiki/Logo_%28programming_language%29'>Logo turtle</a> ;-)<br>
<br>
<pre><code>from nxturtle import NXTurtle<br>
turtle = NXTurtle(connect=True)<br>
<br>
[...] Calibrate and set pen handler as in the sample above<br>
<br>
### Access name and other info<br>
<br>
turtle.set_name("Yertle")<br>
print "Hello, my name is '%s'" % turtle.get_name()<br>
<br>
print "Info: "<br>
print turtle.get_brick_info()<br>
<br>
### Sounds<br>
<br>
# Play 'a' note for half a second<br>
turtle.play_tone(440, 500)<br>
<br>
print "I know these sounds:"<br>
for name in turtle.find_files("*.rso"):<br>
    print "sound", name<br>
<br>
# Play a sound file ('rso' extension is added by default)<br>
turtle.play_sound_file("Goodmorning")<br>
<br>
# starting a sound will stop the previous, so we wait a second<br>
turtle.wait(1000)<br>
<br>
turtle.play_sound_file("Alarm.rso")<br>
<br>
### Programs<br>
print "I know these programs:"<br>
for name in turtle.find_files("*.rxe"):<br>
    print "program", name<br>
<br>
turtle.start_program("Test.rxe")<br>
<br>
### Close connection (will also raise the pen)<br>
turtle.disconnect()<br>
</code></pre>


<h2>Attaching sensors</h2>

A very simple example. Please refer to NXT-Python for details.<br>
<br>
<pre><code>from nxturtle import NXTurtle<br>
turtle = NXTurtle(connect=True)<br>
<br>
[...] Calibrate and set pen handler as in the sample above<br>
<br>
# Attach sensor<br>
turtle.eyes = Ultrasonic(turtle.brick, PORT_4)<br>
<br>
# Read  sensor data<br>
print "I can see for %s miles..." % turtle.eyes.get_distance()<br>
<br>
### Close connection (will also raise the pen)<br>
turtle.disconnect()<br>
</code></pre>