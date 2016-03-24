"""
The Utility module contains individual methods that are useful to multiple others.
The value of having each of these pulled out is simply that they can be accessed from
a variety of modules, preventing code repetition.
"""
import math
from lxml import etree
import time

debug = 0

def timeMethod(method, *parameters):
    start = time.time()
    ret = method(*parameters)
    length = time.time() - start
    print method, "took", length, "seconds to complete. "
    return ret
