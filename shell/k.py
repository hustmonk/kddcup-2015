#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
def get_features(lastday, enrollment, lastdayinfo):
    f = [0] * 4
    if len(lastday) < 4:
        return f
    ids = enrollment.user_info.get(username, [])
    for id in ids:
        days = lastdayinfo.get_days(id)
        username, course_id = enrollment.enrollment_info.get(id)
        bf = False
        en = False
        for day in days:
            k = week.diff(lastday, day)
            if k > 0:
                bf = True
            if k < 0:
                en = True

        if bf and en:
            f[0] = 1
        elif bf and en == False:
            f[1] = 1
        elif bf == False and en:
            f[2] = 1
        else:
            f[3] = 1
    return f
