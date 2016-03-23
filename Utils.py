"""
The Utility module contains individual methods that are useful to multiple others.
The value of having each of these pulled out is simply that they can be accessed from
a variety of modules, preventing code repetition.
"""
import math
from lxml import etree
import time

debug = 0

def elementPrint(element, bool=0):
    """
    `Author`: Bill Clark

    Version = 1.0
    Quick method to print an lxml element. For quicker writing.
    `element`: lxml element.

    `bool`: To pretty print or to compress to a single line.

    `return`: the tostring of the element.

    """

    if bool:
        return etree.tostring(element, pretty_print=False)
    else:
        return etree.tostring(element, pretty_print=True)

def timeMethod(method, *parameters):
    start = time.time()
    ret = method(*parameters)
    length = time.time() - start
    print method, "took", length, "seconds to complete. "
    return ret
