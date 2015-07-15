#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
class Enrollment:
    def __init__(self, filename):
        fin = open(filename)
        fin.next()
        self.enrollment_info = {}
        self.user_info = {}
        self.user_enrollment_id = {}
        self.course_info = {}
        self.ids = []
        for line in fin:
            #enrollment_id,username,course_id
            enrollment_id,username,course_id = line.strip().split(",")
            self.ids.append(enrollment_id)
            self.enrollment_info[enrollment_id] = [username, course_id]
            if username not in self.user_info:
                self.user_info[username] = [course_id]
                self.user_enrollment_id[username] = [enrollment_id]
            else:
                self.user_info[username].append(course_id)
                self.user_enrollment_id[username].append(enrollment_id)

            if course_id not in self.course_info:
                self.course_info[course_id] = [username]
            else:
                self.course_info[course_id].append(username)
        print "load Enrollment info over!",len(self.course_info),len(self.enrollment_info)

if __name__ == "__main__":
    enrollment = Enrollment("../data/train1/enrollment_train.csv")
