#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
import math

psd = {}
for line in open("sub.csv.1"):
    id,p = line.split(",")
    psd[id] = float(p) * 1.02
for line in open("sub.csv.2"):
    id,p = line.split(",")
    psd[id] = float(p)
"""
for line in open("../tovw/test.txt.pred"):
    p, id = line.strip().split(" ")
    p = (float(p) + 1 )/2.0
    #psd[id] = psd[id] * p
"""

fout = open("sub01.csv", "w")
ps = []
for line in open("sub.csv"):
    id,p = line.split(",")
    p = float(p) * psd[id]
    if p > 1:
        p = 1
    fout.write("%s,%.4f\n" % (id, p))
