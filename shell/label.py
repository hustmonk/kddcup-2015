#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'

class Label:
    def __init__(self):
        self.label_info = {}
        for line in open("../data/truth_train.csv"):
            id, y = line.strip().split(",")
            self.label_info[id] = y

    def get(self, id):
        return self.label_info.get(id, "1")

    def contain(self,id):
        if id not in self.label_info:
            return False
        return True

if __name__ == "__main__":
    label = Label()
    print label.get("1")


