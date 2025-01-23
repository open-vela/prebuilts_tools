"""check if two JSON objects are isomorphic"""

__author__ = "Phil Budne"
__revision__ = "$Revision: 1.4 $"

import sys

# For python3 portability
if sys.version_info[0] == 3:
    xrange = range

def jsonmatch(x, y):
    """check if two JSON objects are isomorphic"""

    if isinstance(x, dict) and isinstance(y, dict):
        if len(x) != len(y):
            return False
        for k in x:
            if k not in y:
                return False
            if not jsonmatch(x[k], y[k]):
                return False
        return True
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return False
        for i in xrange(0, len(x)):
            if not jsonmatch(x[i], y[i]):
                return False
        return True
    elif type(x) is type(y):
        return x == y

    return False

