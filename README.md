
>NXTurtle is a mashup of the [Python Turtle graphics for TK](http://docs.python.org/library/turtle.html) 
module and the LEGO Mindstorms driver [NXT-Python](http://code.google.com/p/nxt-python/).<br>
>It allows you to control a LEGO Mindstorms robot like the [turtle](http://en.wikipedia.org/wiki/Turtle_(robot)) 
known from the [Logo programming language](http://en.wikipedia.org/wiki/Logo_(programming_language)).


### Status
This is a hollyday project and barely tested.

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


### Requirements  and installation

  1. This project builds on Python and [http://code.google.com/p/nxt-python/ NXT-Python].<br>Read the [Installation installation instructions] for details.
  2. Build your LEGO Mindstorms turtle. The robot should meet some requirements.<br>Read the [ConstructAndCalibrate build instructions] for details.
  3. Calibrate your turtle (also described in the build instructions).

After this, you are ready to use it:


### Example

```python
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

Read the [Tutorial tutorial] for more...
<hr>
<wiki:video url="http://www.youtube.com/watch?v=5xIK6iFTDzM"/>
