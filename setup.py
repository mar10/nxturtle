# If true, then the svn revision won't be used to calculate the
# revision (set to True for real releases)
import os
RELEASE = False

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# Get version no. (without importing the package, which may fail due to missing 
# dependencies)
#from nxturtle import nxturtle
execfile("nxturtle/version.py")
print "Package version: '%s'" % __version__

long_description = """
Implementation of a Python turtle for LEGO Mindstorms NXT

NXTurtle is a mashup of the Python `Turtle graphics for TK` module 
(http://docs.python.org/library/turtle.html) and the LEGO Mindstorms driver 
NXT-Python (http://nxt-python.googlecode.com/). 

See http://nxturtle.googlecode.com/ for details.
""".strip()

# 'setup.py upload' fails on Vista, because .pypirc is searched on 'HOME' path
if not "HOME" in os.environ and  "HOMEPATH" in os.environ:
    os.environ.setdefault("HOME", os.environ.get("HOMEPATH", ""))
    print "Initializing HOME environment variable to '%s'" % os.environ["HOME"]

try:
    setup(name="nxturtle",
          version = __version__,
          author = "Martin Wendt",
          author_email = "nxturtle@wwwendt.de",
          maintainer = "Martin Wendt",
          maintainer_email = "nxturtle@wwwendt.de",
          url = "http://nxturtle.googlecode.com/",
          description = "Implementation of a Python turtle for LEGO Mindstorms NXT",
          long_description = long_description,
    
            #Development Status :: 2 - Pre-Alpha
            #Development Status :: 3 - Alpha
            #Development Status :: 4 - Beta
            #Development Status :: 5 - Production/Stable
    
          classifiers = ["Development Status :: 4 - Beta",
                         "Intended Audience :: Developers",
                         "Intended Audience :: Education",
                         "Intended Audience :: Science/Research",
                         "License :: OSI Approved :: MIT License",
                         "Operating System :: OS Independent",
                         "Programming Language :: Python",
                         "Topic :: Education",
                         "Topic :: Games/Entertainment",
                         "Topic :: Software Development :: Libraries :: Python Modules",
                         ],
          keywords = "python logo turtle nxt children", 
    #      platforms=["Unix", "Windows"],
          license = "The MIT License",
          install_requires = ["nxt-python", ],
          packages = find_packages(exclude=[]),
          py_modules = ["ez_setup", ],
    
    #      package_data={"": ["*.txt", "*.html", "*.conf"]},
    #      include_package_data = True,
          zip_safe = False,
          extras_require = {},
    #      test_suite = "tests.test_all.run",
          entry_points = {
    #          "console_scripts" : ["tabfix = tabfix.main:run"],
              },
          )
    print "OK!"
except Exception, e:
    print "ERROR: ", e
print "Done"
