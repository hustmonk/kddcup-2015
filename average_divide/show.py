#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
from matplotlib import pyplot
import os
def read(filename):
    kv = {}
    for line in open("evals/" + filename):
        k,v = line.strip().split("\t")
        kv[k] = v
    #return [(float(i)-0.89)*100 for i in kv["eval"].split(",")]
    return [float(i) for i in kv["eval"].split(",")]

for filename in os.listdir("evals"):
    ls = read(filename)
    print filename,ls[-1], max(ls),ls[-100]
    pyplot.plot(ls, linewidth=3, label=filename)

pyplot.grid()
pyplot.legend()
pyplot.xlabel("epoch")
pyplot.ylabel("validation loss")
pyplot.xlim(0, 500)
pyplot.ylim(0.89, 0.9)
pyplot.show()
