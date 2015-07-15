#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
infos = []
for line in open("feature.description"):
    arr = line.strip().split(" ")
    info = " ".join(arr[1:])
    if arr[0].find("-") < 0:
        infos.append(info)
    else:
        start,end = arr[0][1:-1].split("-")
        for i in range(int(start), int(end) + 1):
            infos.append(info)

import cPickle as pickle
modelFileLoad = open('../shell/valid.model', 'rb')
clf = pickle.load(modelFileLoad)
print len(infos),clf.coef_.shape
for i in range(len(infos)):
    print i,infos[i], clf.coef_[0, i]
