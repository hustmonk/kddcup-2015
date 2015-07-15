#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
import math

ps = []
ys = []
for line in open("valid.txt"):
    id,p = line.strip().split(",")
    p = float(p)
    ps.append(p)
for line in open("train2.txt"):
    y = line.split(",")[0]
    ys.append(int(y))
from sklearn import metrics
roc_auc = metrics.roc_auc_score(ys, ps)
print roc_auc
