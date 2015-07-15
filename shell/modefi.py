#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from enrollment import *
from label import *
enrollment = Enrollment("../data/train/enrollment_train.csv")
label = Label()
ps = []
ys = []
for line in open("valid.txt.debug"):
    id,p,y = line.split(",")
    username, course_id = enrollment.enrollment_info.get(id)
    enr_ids = enrollment.user_enrollment_id.get(username, [])
    w = 0
    yx = []
    for _id in enr_ids:
        if _id == id:
            continue
        _y = label.get(_id)
        yx.append(_y)
        if int(_y) > 0: 
            w = w + 1
        else:
            w = w - 1
    up = 0
    if w > 0:
        up = 1
    elif w < 0:
        up = -1
    if up != 0:
        print w,up,p,yx
    ys.append(int(y))
    ps.append(float(p)  + up * 0.01)
from sklearn import metrics
roc_auc = metrics.roc_auc_score(ys, ps)
print roc_auc

