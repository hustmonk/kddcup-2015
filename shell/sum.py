#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from sklearn import metrics
def read(f):
    ps = []
    ys = []
    for line in open(f):
        id,p,y = line.strip().split(",")
        ps.append(float(p))
        ys.append(float(y))
    return ps,ys

ps1,ys1 = read("weight/valid.txt.debug")
ps2,ys2 = read("valid.txt.debug")
import math
ps = [math.sqrt(ps1[i]*ps2[i]) for i in range(len(ys1))]
roc_auc = metrics.roc_auc_score(ys1, ps)
print roc_auc
