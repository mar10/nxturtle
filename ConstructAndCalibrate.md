# Build a robot turtle #

You can build your [LEGO Mindstorms NXT](http://mindstorms.lego.com/) turtle any way you like.

However, in order to run with NXTurtle it should meet some requirements:

  * It should have two wheels on motor B (left) and C (right) respectively.
  * It must be able to turn in-place, so when both wheels are spinned in opposite directions, the turtle should rotate about it's center.
  * It should have a pen that can be raised/lowered using motor C.
  * The pen should be centered between the wheels, so it will stay at it's position when the turtles turns.

**One example:**

http://lh3.ggpht.com/_KDHcEOm_Ou0/TMQnGo30GII/AAAAAAAABuc/p_ARX3LK_QE/s512/DSCF5377.JPG


# Calibration #

All turtles are not created equal, so we have to define how many motor turns
it takes to move it by one unit, or turn it by one degree.
Here we do this by a combination of calculation and empirical information ;-)

We set the calibration information after the turtle is initalized:
```
from nxturtle import NXTurtle
import math

### Create the turtle and connect to LEGO NXT brick
turtle = NXTurtle(connect=True)
```

## Calibrating movement ##

```
### Calibrate
# Distance between left and right wheel in [cm] (measured from middle of treads)
AXIS_LENGTH = 12.5
# Wheel diameter in [cm]
WHEEL_DIAMETER = 4.4

# Now we can calculate the number of wheel turns it takes, to move the turtle 
# by one unit (i.e. one centimeter) 
tachoPerUnit = 360.0 / (WHEEL_DIAMETER * math.pi)
correction = 1.00 
turtle.set_tacho_units_per_unit(correction * tachoPerUnit)
```

## Calibrating turns ##

```
# It should also be possible to calculate the number of wheel turns it takes, 
# to turn the turtle by one degree 
tachoPerDegree = AXIS_LENGTH / WHEEL_DIAMETER
# ... observation shows that Archimedes was wrong, or our turtle is not 
# perfect. Either way this correction factor will improve the results: 
correction = 0.90 
turtle.set_tacho_units_per_degree(correction * tachoPerDegree)
```


## Calibrating the pen ##

Because the pen may be controlled in many different ways, we have to define a litte control function and pass it to the turtle at startup.

The only assumption here is that the pen motor is attached to port C.

**Example:**
```
# This function is passed to our turtle. It will be called whenever the pen 
# should be raised or put down. 
def pen_handler(turtle, on):
    power = 50
    tacho_units = 150
    if on:
        power *= -1
    turtle.penMotor.turn(power, tacho_units)

turtle.set_pen_handler(pen_handler)
```

Now read the [Tutorial](Tutorial.md) for a complete example...