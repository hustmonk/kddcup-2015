#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
fins = []
N = 10
for i in range(N):
    fin = open("merge/sub.csv"+str(i))
    fins.append(fin)
fout = open("merge.csv","w")
while fins[0]:
    ps = []
    for i in range(N):
        line = fins[i].readline()
        if len(line) == 0:
            break
        id,pred = line.strip().split(",")
        ps.append(float(pred))
    if len(line) == 0:
        break
    fout.write("%s,%f\n" % (id, sum(ps)/N))
