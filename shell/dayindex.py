#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
class CAlldayIndex:
    def __init__(self):
        cdict = {}
        for line in open("conf/allday.log"):
            cdict[line.strip()] = len(cdict)
        self.cdict = cdict

    def get_features(self, days):
        f = [0] * len(self.cdict)
        for day in days:
            if len(day) > 1:
                idx = self.cdict[day]
                f[idx] = 1 + f[idx]
        return ",".join(["%d" % k for k in f])

if __name__ == "__main__":
    calldayindex = CAlldayIndex()
    print calldayindex.get_features(["2014-06-30"])

