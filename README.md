# NXTurtle [![Powered by You](http://sapegin.github.io/powered-by-you/badge.svg)](http://sapegin.github.io/powered-by-you/)

>NXTurtle is a mashup of the [Python Turtle graphics for TK](http://docs.python.org/library/turtle.html) 
module and the LEGO Mindstorms driver [NXT-Python](https://github.com/eelviny/nxt-python).<br>
>It allows you to control a LEGO Mindstorms robot like the [turtle](http://en.wikipedia.org/wiki/Turtle_(robot)) 
known from the [Logo programming language](http://en.wikipedia.org/wiki/Logo_(programming_language)).


### Status

This is a holiday project and barely tested.

Just to remind you
```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

Having said that: Have fun!
Any feedback is welcome :-)


### Get Started

  1. This project builds on Python and the NXT-Python driver.<br>
     Read the [installation instructions](https://github.com/mar10/nxturtle/wiki/Installation) for details.
  2. Build your LEGO Mindstorms turtle. 
     The robot should meet some requirements:<br>
     Read the [build instructions](https://github.com/mar10/nxturtle/wiki/ConstructAndCalibrate) for details.
  3. Calibrate your turtle (also described in the build instructions).
  4. Read the [Tutorial](https://github.com/mar10/nxturtle/wiki/Tutorial).

After this, you are ready to use it:


### Example

```py
from nxturtle import NXTurtle
yertle = NXTurtle(connect=True)

# [... some initialization ...]

# standard turtle action
yertle.pendown()
yertle.forward(10)
yertle.left(90)
yertle.home()

# and some more bricky capabilities
yertle.play_tone(440, 500)
```

Read the [Tutorial](https://github.com/mar10/nxturtle/wiki/Tutorial) for more...


[![Demo Video](https://img.youtube.com/vi/5xIK6iFTDzM/0.jpg)](http://www.youtube.com/watch?v=5xIK6iFTDzM)
