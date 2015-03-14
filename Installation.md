# Prerequisites and installation #
This has been tested on Ubuntu 10 and Windows 7.

## 1. Python ##
Get [Python](http://python.org/download) version 2.6 or 2.7.
(I haven't tested with 2.5; let me know if you got it working.)

## 2. NXT-Python and additional drivers ##

Install [NXT-Python](http://code.google.com/p/nxt-python/wiki/Installation) driver by Marcus Wanner.

The installation instructions there will also describe how to install USB and/or bluetooth drivers ([PyUSB](http://sourceforge.net/projects/pyusb/) and/or [PyBluez](http://code.google.com/p/pybluez/)).


## 3. Install NXTurtle ##

If [EasyInstall](http://pypi.python.org/pypi/setuptools#using-setuptools-and-easyinstall) is available, then installation on Linux is as easy as:

```
$sudo easy_install -U nxturtle
```

or on Windows:
```
>easy_install -U nxturtle
```

and you are set.

Otherwise
  1. [Download the latest source package](DownloadTab.md) and extract it.
  1. Open a terminal and `cd nxturtle` (or whatever directory you put it in).
  1. Run `python setup.py install`.


## 4. Build and calibrate your turtle ##

Build your LEGO Mindstorms NXT turtle. It should meet some requirements.

Read the [build instructions](ConstructAndCalibrate.md) to learn how to build and calibrate your turtle.


## 5. Have fun ##

Read the [Tutorial](Tutorial.md) to learn how to command your turtle using Python...