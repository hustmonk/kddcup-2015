#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
from log import *
from enrollment import *
from Object import *
from label import *
from weekend import *
from coursetime import *
from common import *
from highuser import *
import math
from module import *
from transfer import *
"""
week = Week()
coursetimeinfo = CourseTimeInfo()
log_filename = sys.argv[1]
enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]
log = Log(log_filename)
enrollment_train = Enrollment(enrollment_filename)
enrollment = Enrollment("../data/merge/enrollment.csv")
obj = Obj()
label = Label()
userinfo = Userinfo()
userinfo.load()
module = Module()
module.load()
transfer_day = Transfer()
transfer_day.load()
ids = enrollment_train.ids
import math

fout = open(featrue_filename,"w")
ccc = 0
gods = {}
for id in ids:
    ccc += 1
    if ccc % 5000 == 0:
        print ccc
    y = label.get(id)
    infos = log.enrollment_loginfo.get(id, [])
    username, course_id = enrollment.enrollment_info.get(id)
    days = set()
    for info in infos:
        day,timehms = info[0].split("T")
        days.add(day)
    days = sorted(days)
    alldays = userinfo.get_days(username)
    god = False
    for day in alldays:
        diff = week.diff(day,days[-1])
        if diff > 1 and diff < 10:
            gods[id] = gods.get(id,0) + 1
import pickle
modelFileSave = open('conf/gods', 'wb')
pickle.dump(gods, modelFileSave)
modelFileSave.close()
"""
modelFileLoad = open('conf/gods', 'rb')
gods = pickle.load(modelFileLoad)

ps = []
ys = []
for line in open("weight/valid.txt.debug"):
    id,p,y = line.strip().split(",")
    p = float(p)
    if id in gods:
        if  gods[id] < 4:
            p = float(p) - 0.01 * gods[id]
    ps.append(p)
    ys.append(int(y))
from sklearn import metrics
roc_auc = metrics.roc_auc_score(ys, ps)
print roc_auc
