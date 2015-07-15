#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'

import sys
import math
from common import *

ps = []
ys = []
psd = {}
for line in open("valid.txt.1.debug"):
    id,p,y = line.split(",")
    ys.append(int(y))
    ps.append(float(p))
    #psd[id] = float(p) * 1.04
    psd[id] = float(p)
for line in open("valid.txt.2.debug"):
    id,p,y = line.split(",")
    ys.append(int(y))
    ps.append(float(p))
    psd[id] = float(p)
"""
for line in open("../tovw/train2.txt.pred"):
    p, id = line.strip().split(" ")
    p = (float(p) + 1 )/2.0
    psd[id] = psd[id] * p

for line in open("../xgboost/valid.txt.debug"):
    id,p,y = line.split(",")
    psd[id] = psd[id] * float(p)
    #psd[id] = float(p)
for line in open("../xgboost/valid.txt.debug.bak"):
    id,p,y = line.split(",")
    psd[id] = psd[id] * float(p)

for line in open("../xgboost/my_neural_net_submission.csv"):
    id,p,p1 = line.split(",")
    #psd[id] = psd[id] * float(p1)
    psd[id] = float(p1)

for line in open("../nn/my_neural_net_submission.csv"):
    id,p,p1 = line.split(",")
    #psd[id] = psd[id] * float(p1)
    psd[id] = float(p1)

for line in open("../reducelr/valid.txt.debug"):
    id,p,y = line.split(",")
    psd[id] = float(p) * psd[id]
"""
ps = []
ys = []
for line in open("valid.txt.debug"):
    id,p,y = line.split(",")
    ys.append(int(y))
    ps.append(float(p) * psd[id])
    #ps.append(psd[id])
    #ps.append(float(p))
from sklearn import metrics
roc_auc = metrics.roc_auc_score(ys, ps)
import logging
import logging.config
logging.config.fileConfig("log.conf")
logger = logging.getLogger("example")
print logger.info(roc_auc)
