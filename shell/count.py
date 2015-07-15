#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

fin = open("train2.txt")

header = fin.next().strip().split(",")
counts = []
drop = []
for i in range(len(header)):
    counts.append({})
    drop.append({})
cc = 0
for line in fin:
    arr = line.strip().split(",")
    cc += 1
    label = arr[0]
    for i in range(2, len(header)):
        key = arr[i]

        counts[i][key] = counts[i].get(key, 0) + 1
        if label == '1':
            drop[i][key] = drop[i].get(key, 0) + 1

for i in range(1, len(header)):
    print "TOTAL:",i,len(counts[i])
    for (k,v) in sorted(counts[i].items(), key=lambda x:x[1]):
        print i,k,v,v/float(cc),drop[i].get(k, 0) / float(v)
